import os
import json
import re

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

TARGET_EXERCISES = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.2", "3.3", "3.4", "3.5", "3.6", "4.1", "4.3"]
ALL_SECTIONS = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "4.1", "4.2", "4.3", "Final"]

def evaluate_student_precise(fpath):
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
                # check if example cell
                if "# Ejemplo -- no modificar" not in src and "# Ejemplo" not in src:
                    # also exclude verification cell 4.2
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
                # Verify exercise logic
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

print(f"{'User':<12} | {'Solved/15':<10} | Solved Exercises")
print("-" * 75)

for uf in user_folders:
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        continue
    fpath = os.path.join(uf_path, files[0])
    s_ex = evaluate_student_precise(fpath)
    solved = [k for k, v in s_ex.items() if v]
    print(f"{uf:<12} | {len(solved):<10} | {','.join(solved) if solved else 'Ninguno'}")
