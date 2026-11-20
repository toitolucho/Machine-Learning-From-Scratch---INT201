import os
import json
import csv
import datetime
import requests
import re
from dotenv import load_dotenv

load_dotenv()
DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
TOKEN = os.environ.get('MOODLE_TOKEN')
ENDPOINT = f'{DOMAIN}/webservice/rest/server.php'

def call_moodle(fn, params={}):
    p = {'wstoken': TOKEN, 'wsfunction': fn, 'moodlewsrestformat': 'json'}
    p.update(params)
    r = requests.post(ENDPOINT, data=p)
    return r.json()

tz = datetime.timezone(datetime.timedelta(hours=-4))

# 1. Fetch enrolled users and submission data from Moodle
print("Fetching enrolled users and submission data from Moodle...")
users_data = call_moodle('core_enrol_get_enrolled_users', {'courseid': 6582})
user_map = {u['id']: u for u in users_data} if isinstance(users_data, list) else {}

subs_data = call_moodle('mod_assign_get_submissions', {'assignmentids[0]': 77028})
assign_subs = subs_data['assignments'][0]['submissions']
sub_map = {s['userid']: s for s in assign_subs if s.get('status') == 'submitted'}

# 2. Setup paths
sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
report_csv_path = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\reporte_calificaciones_parte1.csv"
user_folders = sorted(os.listdir(sub_dir))

TARGET_EXERCISES = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.2", "3.3", "3.4", "3.5", "3.6", "4.1", "4.3"]
ALL_SECTIONS = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "4.1", "4.2", "4.3", "Final"]

def evaluate_notebook(fpath):
    with open(fpath, "r", encoding="utf-8") as fp:
        nb = json.load(fp)
        
    cells = nb.get("cells", [])
    sections = {ex: {"code": [], "md": []} for ex in ALL_SECTIONS}
    current_ex = None
    
    for idx, c in enumerate(cells):
        src = "".join(c.get("source", []))
        if c.get("cell_type") == "markdown":
            m = re.search(r"Ejercicio\s+([0-9]+\.[0-9]+)", src)
            if m and m.group(1) in ALL_SECTIONS:
                current_ex = m.group(1)
            elif "Paso Final" in src:
                current_ex = "Final"
            elif current_ex:
                sections[current_ex]["md"].append(src)
        elif c.get("cell_type") == "code":
            if current_ex:
                if "# Ejemplo -- no modificar" not in src and "# Ejemplo" not in src:
                    if "# Celda de verificación" not in src and "# Exportar el dataset" not in src:
                        sections[current_ex]["code"].append(c)
                    
    solved_exercises = {}
    
    for ex in TARGET_EXERCISES:
        code_cells = sections[ex]["code"]
        ex_solved = False
        
        for c in code_cells:
            src = "".join(c.get("source", []))
            has_qm = "???" in src
            lines = [l.strip() for l in src.split("\n") if l.strip()]
            active_lines = [l for l in lines if not l.startswith("#")]
            
            if not has_qm and len(active_lines) >= 1 and not all(l == "pass" for l in active_lines):
                if ex == "1.1" and any("characters_raw[0]" in l or "primer_nombre" in l for l in active_lines):
                    ex_solved = True
                elif ex == "1.2" and any("for" in l and "characters_raw" in l for l in active_lines):
                    ex_solved = True
                elif ex == "1.3" and any("None" in l or "isinstance" in l or "missing" in l or "fps" in l for l in active_lines):
                    ex_solved = True
                elif ex == "1.4" and any("valid_frames" in l or "error_names" in l or "TypeError" in l for l in active_lines):
                    ex_solved = True
                elif ex == "2.1" and any("palette" in l or "first_color" in l or "r" in l for l in active_lines):
                    ex_solved = True
                elif ex == "2.2" and any("enumerate" in l or "palette" in l for l in active_lines):
                    ex_solved = True
                elif ex == "2.3" and any("0.299" in l or "brightness" in l or "sum" in l for l in active_lines):
                    ex_solved = True
                elif ex == "2.4" and any("production_lookup" in l or "production_hours" in l for l in active_lines):
                    ex_solved = True
                elif ex == "3.2" and any("role" in l or "support" in l or "Crux" in l for l in active_lines):
                    ex_solved = True
                elif ex == "3.3" and any("int(" in l or "fps" in l for l in active_lines):
                    ex_solved = True
                elif ex == "3.4" and any("has_special_fx" in l for l in active_lines):
                    ex_solved = True
                elif ex == "3.5" and any("append" in l or "palette" in l or "240" in l for l in active_lines):
                    ex_solved = True
                elif ex == "3.6" and any("state_counts" in l or "states" in l for l in active_lines):
                    ex_solved = True
                elif ex == "4.1" and any("num_colors" in l or "num_frames_total" in l for l in active_lines):
                    ex_solved = True
                elif ex == "4.3" and any("avg_hours" in l or "top_frames" in l or "max(" in l for l in active_lines):
                    ex_solved = True
                    
            if ex_solved:
                break
                
        solved_exercises[ex] = ex_solved
        
    return solved_exercises

# Test time parameters
EXAM_START_TS = 1790683200  # 2026-09-29 08:00:00 UTC-4
DUE_DATE_TS   = 1790685000  # 2026-09-29 08:30:00 UTC-4
CUTOFF_TS     = 1790685300  # 2026-09-29 08:35:00 UTC-4

report_rows = []

for uf in user_folders:
    uid = int(uf.replace("User_", ""))
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        continue
    fpath = os.path.join(uf_path, files[0])
    
    # 1. User Info
    u = user_map.get(uid, {})
    fullname = u.get("fullname", f"User_{uid}")
    email = u.get("email", "")
    
    # 2. Submission Timestamps
    sub = sub_map.get(uid, {})
    tc = sub.get("timecreated")
    tm = sub.get("timemodified")
    
    dt_c = datetime.datetime.fromtimestamp(tc, tz) if tc else None
    dt_m = datetime.datetime.fromtimestamp(tm, tz) if tm else None
    
    str_c = dt_c.strftime("%Y-%m-%d %H:%M:%S") if dt_c else "N/A"
    str_m = dt_m.strftime("%Y-%m-%d %H:%M:%S") if dt_m else "N/A"
    
    # Duration in minutes
    duration_min = round((tm - tc) / 60, 2) if (tc and tm) else 0.0
    
    # Late arrival analysis (start after 08:15:00)
    delay_start_sec = max(0, tc - EXAM_START_TS) if tc else 0
    delay_start_min = round(delay_start_sec / 60, 2)
    is_late_arrival = delay_start_min > 15.0  # More than 15 minutes after 08:00
    is_very_late_arrival = delay_start_min > 20.0  # More than 20 minutes after 08:00
    
    # Tolerance usage (submitted after 08:30:00)
    delay_submit_sec = max(0, tm - DUE_DATE_TS) if tm else 0
    used_tolerance = delay_submit_sec > 0
    
    # 3. Notebook Grading
    solved_map = evaluate_notebook(fpath)
    solved_list = [k for k, v in solved_map.items() if v]
    solved_count = len(solved_list)
    
    # Base Grade out of 100
    raw_grade = round((solved_count / 15.0) * 100.0, 2)
    
    # 4. Penalty Rules
    # Rule A: Tolerance usage (-10 pts)
    penalty_tolerance = 10.0 if used_tolerance else 0.0
    
    # Rule B: Late arrival (-10 pts if > 15 min, -20 pts if > 20 min)
    if is_very_late_arrival:
        penalty_late = 20.0
    elif is_late_arrival:
        penalty_late = 10.0
    else:
        penalty_late = 0.0
        
    # Total Penalties
    total_penalties = penalty_tolerance + penalty_late
    final_grade = max(0.0, round(raw_grade - total_penalties, 2))
    
    # Penalty Flag and Reason
    needs_penalty = (total_penalties > 0)
    reasons = []
    if is_very_late_arrival:
        reasons.append(f"Ingreso muy tardio al examen (+{delay_start_min} min despues del inicio; penalizacion -20 pts)")
    elif is_late_arrival:
        reasons.append(f"Ingreso tardio al examen (+{delay_start_min} min despues del inicio; penalizacion -10 pts)")
        
    if used_tolerance:
        reasons.append(f"Entrega dentro de la ventana de tolerancia (+{delay_submit_sec}s despues de las 08:30; penalizacion -10 pts)")
        
    # Check suspicious rapid completion flag
    if delay_start_min > 20.0 and duration_min < 8.0 and solved_count > 0:
        reasons.append(f"ALERTA: Tiempo de resolucion sospechosamente bajo ({duration_min} min)")
        
    if not reasons:
        motivo = "Ninguno (Cumplio horario e inicio puntualmente)"
    else:
        motivo = "; ".join(reasons)
        
    report_rows.append({
        "User_ID": uid,
        "Estudiante": fullname,
        "Email": email,
        "Hora_Inicio": str_c,
        "Hora_Entrega": str_m,
        "Duracion_Min": duration_min,
        "Retraso_Inicio_Min": delay_start_min,
        "Llegada_Tardia": "SI" if is_late_arrival else "NO",
        "Uso_Tolerancia": "SI" if used_tolerance else "NO",
        "Segundos_Exceso_Tolerancia": delay_submit_sec,
        "Ejercicios_Resueltos": f"{solved_count}/15",
        "Lista_Ejercicios": ",".join(solved_list) if solved_list else "Ninguno",
        "Nota_Base_100": raw_grade,
        "Penalizacion_Llegada_Pts": penalty_late,
        "Penalizacion_Tolerancia_Pts": penalty_tolerance,
        "Total_Penalizaciones_Pts": total_penalties,
        "Nota_Final_100": final_grade,
        "Debe_Penalizarse": "SI" if needs_penalty else "NO",
        "Motivo_Penalizacion": motivo
    })

# Write CSV with utf-8-sig (for Excel compatibility with Spanish accents)
fieldnames = [
    "User_ID", "Estudiante", "Email", "Hora_Inicio", "Hora_Entrega",
    "Duracion_Min", "Retraso_Inicio_Min", "Llegada_Tardia", "Uso_Tolerancia",
    "Segundos_Exceso_Tolerancia", "Ejercicios_Resueltos", "Lista_Ejercicios",
    "Nota_Base_100", "Penalizacion_Llegada_Pts", "Penalizacion_Tolerancia_Pts",
    "Total_Penalizaciones_Pts", "Nota_Final_100", "Debe_Penalizarse", "Motivo_Penalizacion"
]

with open(report_csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(report_rows)

print(f"\nReport successfully generated: {report_csv_path}")
print(f"Total students evaluated: {len(report_rows)}")
