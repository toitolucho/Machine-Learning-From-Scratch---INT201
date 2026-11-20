#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
grade_assignments_int210.py - Sistema Integral de Calificación para eCampus
Curso: Machine Learning (INT210 - Curso 6726)
Tareas:
  - T01 (CMID: 420907, Inst: 77380) - WBCD y Evaluación Multimodelo
  - T02 (CMID: 420908, Inst: 77381) - Taller Comparativo de Clasificadores
=============================================================================
"""

import os
import sys
import json
import csv
import re
import argparse
import datetime
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
load_dotenv(os.path.join(WORKSPACE_ROOT, ".env"))

DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo').rstrip('/')
TOKEN = os.environ.get('MOODLE_TOKEN')
USERNAME = os.environ.get('MOODLE_USERNAME')
PASSWORD = os.environ.get('MOODLE_PASSWORD')
ENDPOINT = f'{DOMAIN}/webservice/rest/server.php'

COURSE_ID = 6726
T01_CMID = 420907
T01_INST = 77380
T02_CMID = 420908
T02_INST = 77381

T01_DIR = os.path.join(SCRIPT_DIR, f"tarea_{T01_CMID}_inst_{T01_INST}")
T02_DIR = os.path.join(SCRIPT_DIR, f"tarea_{T02_CMID}_inst_{T02_INST}")

TZ = datetime.timezone(datetime.timedelta(hours=-4))
DUE_TS = 1792681200    # 2026-10-22 11:00:00 UTC-4

def renew_token():
    global TOKEN
    print("  [AUTH] Intentando renovar token...")
    token_url = f"{DOMAIN}/login/token.php"
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'service': 'moodle_mobile_app'
    }
    try:
        res = requests.post(token_url, data=data, timeout=30)
        res_json = res.json()
        if 'token' in res_json:
            TOKEN = res_json['token']
            print(f"  [AUTH] Token renovado exitosamente.")
            return TOKEN
    except Exception as e:
        print(f"  [AUTH ERROR] {e}")
    return None

def call_moodle(fn, params=None):
    global TOKEN
    if params is None:
        params = {}
    p = {'wstoken': TOKEN, 'wsfunction': fn, 'moodlewsrestformat': 'json'}
    p.update(params)
    try:
        r = requests.post(ENDPOINT, data=p, timeout=30)
        res = r.json()
        if isinstance(res, dict) and res.get('errorcode') in ['invalidtoken', 'accessexception']:
            if renew_token():
                p['wstoken'] = TOKEN
                r = requests.post(ENDPOINT, data=p, timeout=30)
                return r.json()
        return res
    except Exception as e:
        return {'error': str(e)}

def extract_code_and_md(fpath):
    code_cells = []
    md_cells = []
    if not fpath or not os.path.exists(fpath):
        return "", ""
        
    if fpath.endswith('.ipynb'):
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as fp:
                nb = json.load(fp)
            for c in nb.get('cells', []):
                ctype = c.get('cell_type')
                src = "".join(c.get('source', []))
                if ctype == 'code':
                    code_cells.append(src)
                elif ctype == 'markdown':
                    md_cells.append(src)
        except Exception as e:
            code_cells.append(f"# Error loading nb: {e}")
            
    elif fpath.endswith('.py'):
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as fp:
                src = fp.read()
            code_cells.append(src)
            docstrings = re.findall(r'"""(.*?)"""', src, re.DOTALL)
            md_cells.extend(docstrings)
        except Exception as e:
            code_cells.append(f"# Error reading py: {e}")
            
    return "\n\n".join(code_cells), "\n\n".join(md_cells)

def locate_student_file(uid, name, intended_task):
    """
    Locates the student's submission file for intended_task ('T01' or 'T02').
    Automatically detects if files were swapped by the student.
    """
    u1_folder = os.path.join(T01_DIR, f"User_{uid}_{name.replace(' ', '_')}")
    u2_folder = os.path.join(T02_DIR, f"User_{uid}_{name.replace(' ', '_')}")
    
    # Swapped students list detected during audit:
    swapped_uids = [189741, 193316]
    
    target_folder = u1_folder if intended_task == 'T01' else u2_folder
    other_folder  = u2_folder if intended_task == 'T01' else u1_folder
    
    is_swapped = (uid in swapped_uids)
    active_folder = other_folder if is_swapped else target_folder
    
    files = []
    if os.path.exists(active_folder):
        for r, d, fs in os.walk(active_folder):
            for f in fs:
                if f.endswith(('.ipynb', '.py')) and not f.startswith('.'):
                    files.append(os.path.join(r, f))
                    
    selected_file = files[0] if files else None
    return selected_file, is_swapped

def grade_t01_submission(uid, name, fpath, is_swapped):
    """
    Rubric for T01 (Breast Cancer WBCD & Multimodel Evaluation): Max 100 pts.
    """
    if not fpath or not os.path.exists(fpath):
        return {
            'nota': 0.0,
            'estado': 'No entregado',
            'detalles': 'No se encontró archivo de entrega.',
            'feedback_html': '<p><strong>Sin entrega registrada.</strong> Calificación: 0/100.</p>',
            'rubro_preproc': 0,
            'rubro_escalamiento': 0,
            'rubro_modelado': 0,
            'rubro_teorico': 0,
            'archivo': 'Ninguno'
        }
        
    code, md = extract_code_and_md(fpath)
    combined = (code + "\n" + md).lower()
    fname = os.path.basename(fpath)
    
    # Check for Banknote alternate homework (Mayta Baltazar)
    if "banknote" in combined or "variance" in combined:
        return {
            'nota': 80.0,
            'estado': 'Entregado (Tarea previa: Banknote)',
            'detalles': 'Entregó tarea guiada de Banknote Authentication en lugar de WBCD.',
            'feedback_html': (
                f"<p><strong>Estimado/a {name}:</strong></p>"
                f"<p>Se revisó su entrega (<em>{fname}</em>). Observación: Ha subido la guía práctica "
                f"correspondiente al dataset <strong>Banknote Authentication</strong> en lugar del "
                f"Laboratorio Evaluado de <strong>Cáncer de Mama WBCD</strong>. "
                f"Se reconoce la correcta resolución del análisis de correlación y clasificador de fraude asignando <strong>80/100</strong>.</p>"
            ),
            'rubro_preproc': 20,
            'rubro_escalamiento': 20,
            'rubro_modelado': 20,
            'rubro_teorico': 20,
            'archivo': fname
        }
        
    # Standard T01 Rubric:
    # 1. Preprocesamiento (25 pts)
    p_map = 0
    if any(k in code for k in ["['M']: 1", "map({'M': 1", "map({'M':1", "'M': 1", "'M':1", 'map({"M": 1', 'map({"M":1', 'lambda x: 1 if', "datos.target", "load_breast_cancer"]):
        p_map = 10
    elif "diagnosis" in code:
        p_map = 7
        
    p_split = 10 if "train_test_split" in code else 0
    p_xy = 5 if any(k in code for k in ["iloc[:, 2:]", "iloc[:,2:]", "drop(columns=", "drop(", "X =", "X="]) else 0
    preproc_score = p_map + p_split + p_xy
    
    # 2. Escalamiento (20 pts)
    p_scaler = 10 if ("StandardScaler" in code or "MinMaxScaler" in code) else 0
    p_leakage = 0
    if "fit_transform" in code:
        p_leakage += 5
    if any(k in code for k in ["transform(X_test", "transform(x_test", "transform(X_test_scaled", "transform(X_test_escalado"]):
        p_leakage += 5
    scaling_score = p_scaler + p_leakage
    
    # 3. Modelado y Matrices de Confusión (30 pts)
    p_knn = 10 if "KNeighborsClassifier" in code else 0
    p_tree = 10 if "DecisionTreeClassifier" in code else 0
    p_cm = 10 if "confusion_matrix" in code else (5 if "classification_report" in code else 0)
    modeling_score = p_knn + p_tree + p_cm
    
    # 4. Evaluación Teórica / Preguntas de Negocio (25 pts)
    p_q1 = 0
    if any(k in combined for k in ["falso negativo", "tipo ii", "error tipo 2", "error tipo ii", "tumor maligno", "paciente sano", "cáncer"]) and any(k in combined for k in ["vida", "muerte", "retras", "tratamiento", "metasta", "grave", "morir", "casa"]):
        p_q1 = 15
    elif any(k in combined for k in ["falso negativo", "tipo ii", "maligno"]):
        p_q1 = 10
        
    p_q2 = 0
    if any(k in combined for k in ["arbol", "árbol"]) and any(k in combined for k in ["distancia", "euclid", "escala", "umbral", "jerarqu", "regla", "particion", "corte"]):
        p_q2 = 10
    elif any(k in combined for k in ["arbol", "árbol", "escalar", "magnitud"]):
        p_q2 = 7
        
    theory_score = p_q1 + p_q2
    
    total_raw = preproc_score + scaling_score + modeling_score + theory_score
    total_grade = min(100.0, float(total_raw))
    
    feedback_parts = []
    feedback_parts.append(f"<p><strong>Estimado/a {name}:</strong></p>")
    if is_swapped:
        feedback_parts.append(
            f"<p><em>Nota administrativa:</em> Su archivo fue subido en el casillero de T02 por equivocación, "
            f"pero fue identificado y calificado aquí en T01 sin penalización.</p>"
        )
    feedback_parts.append(f"<p><strong>Calificación obtenida: {total_grade:g}/100</strong></p>")
    feedback_parts.append("<ul>")
    feedback_parts.append(f"<li><strong>Preprocesamiento ({preproc_score}/25):</strong> Mapeo binario de diagnóstico (M/B), separación limpia de features y target, y partición train/test.</li>")
    feedback_parts.append(f"<li><strong>Escalamiento ({scaling_score}/20):</strong> Uso adecuado de StandardScaler sin fuga de datos (.fit_transform en train y .transform en test).</li>")
    feedback_parts.append(f"<li><strong>Modelado ({modeling_score}/30):</strong> Entrenamiento de k-NN (n=5), Árbol de Decisión (max_depth=4) y generación de matrices de confusión.</li>")
    feedback_parts.append(f"<li><strong>Análisis Teórico ({theory_score}/25):</strong> Fundamentación clínica del riesgo del Error Tipo II (Falso Negativo) y explicación de la invarianza de escala en Árboles.</li>")
    feedback_parts.append("</ul>")
    
    feedback_html = "".join(feedback_parts)
    
    return {
        'nota': total_grade,
        'estado': 'Calificado',
        'detalles': f"Preproc: {preproc_score}/25, Escala: {scaling_score}/20, Modelos: {modeling_score}/30, Teorico: {theory_score}/25",
        'feedback_html': feedback_html,
        'rubro_preproc': preproc_score,
        'rubro_escalamiento': scaling_score,
        'rubro_modelado': modeling_score,
        'rubro_teorico': theory_score,
        'archivo': fname
    }

def grade_t02_submission(uid, name, fpath, is_swapped):
    """
    Rubric for T02 (Wine Classifiers Comparison Workshop): Max 100 pts.
    """
    if not fpath or not os.path.exists(fpath):
        return {
            'nota': 0.0,
            'estado': 'No entregado',
            'detalles': 'No se encontró archivo de entrega.',
            'feedback_html': '<p><strong>Sin entrega registrada.</strong> Calificación: 0/100.</p>',
            'rubro_base': 0,
            'rubro_reto': 0,
            'rubro_fronteras': 0,
            'rubro_conclusiones': 0,
            'archivo': 'Ninguno'
        }
        
    code, md = extract_code_and_md(fpath)
    combined = (code + "\n" + md).lower()
    fname = os.path.basename(fpath)
    
    # Check for MinMaxScaler alternate homework (Mayta Baltazar)
    if "minmaxscaler" in combined and "vino" not in combined and "wine" not in combined:
        return {
            'nota': 80.0,
            'estado': 'Entregado (Tarea previa: Escalado k-NN)',
            'detalles': 'Entregó guía de impacto de escalado en k-NN en lugar del Taller de Vinos.',
            'feedback_html': (
                f"<p><strong>Estimado/a {name}:</strong></p>"
                f"<p>Se revisó su entrega (<em>{fname}</em>). Observación: Ha subido la guía práctica "
                f"correspondiente al impacto del escalado en k-NN en lugar del "
                f"Taller Comparativo de Clasificadores con el dataset <strong>Wine</strong>. "
                f"Se reconoce la adecuada experimentación con MinMaxScaler asignando <strong>80/100</strong>.</p>"
            ),
            'rubro_base': 25,
            'rubro_reto': 20,
            'rubro_fronteras': 15,
            'rubro_conclusiones': 20,
            'archivo': fname
        }
        
    # Check if student ONLY submitted the class tutorial without completing the homework
    has_hw_corr = ("heatmap" in code.lower() or "corr(" in code.lower()) and any(k in combined for k in ["prolina", "fenoles", "matiz", "od280", "tercera", "3ra", "ranking"])
    has_hw_logreg = "logisticregression" in code.lower() or "regresion logistica" in combined or "regresión logística" in combined
    has_hw_pipeline = "pipeline" in code.lower()
    
    if not (has_hw_corr or has_hw_logreg or has_hw_pipeline):
        return {
            'nota': 50.0,
            'estado': 'Parcial (Solo código de clase)',
            'detalles': 'Solo incluye el tutorial de clase. No se realizó la sección de tarea / reto autónomo.',
            'feedback_html': (
                f"<p><strong>Estimado/a {name}:</strong></p>"
                f"<p>Se revisó su entrega (<em>{fname}</em>). Ha completado adecuadamente el código guiado "
                f"en clase (k-NN, Árbol y Naive Bayes con Alcohol y Flavonoides). "
                f"Sin embargo, <strong>no incluyó el reto / tarea asignada</strong> (mapa de calor y 3ra característica o modelo de regresión logística con fronteras). "
                f"Calificación de la sección completada: <strong>50/100</strong>.</p>"
            ),
            'rubro_base': 40,
            'rubro_reto': 0,
            'rubro_fronteras': 10,
            'rubro_conclusiones': 0,
            'archivo': fname
        }

    # 1. Base tutorial completion (40 pts)
    p_base_data = 15 if "load_wine" in code else 10
    p_base_models = 0
    if "KNeighborsClassifier" in code: p_base_models += 9
    if "DecisionTreeClassifier" in code: p_base_models += 8
    if ("GaussianNB" in code or "naive_bayes" in code): p_base_models += 8
    base_score = p_base_data + p_base_models
    
    # 2. Reto Autónomo: Variante A (Correlación / 3ra Característica) vs Variante B (Regresión Logística / 2x2)
    reto_score = 0
    tipo_tarea = "Variante A (Correlación y 3ra Variable)"
    
    if has_hw_logreg and not has_hw_corr:
        tipo_tarea = "Variante B (Regresión Logística y Comparación 2x2)"
        reto_score = 25
    elif has_hw_pipeline and not has_hw_corr:
        tipo_tarea = "Variante B (Pipeline y Comparación de Clasificadores)"
        reto_score = 25
    elif has_hw_corr:
        reto_score = 25
    else:
        reto_score = 15
        
    # 3. Representación Gráfica de Fronteras de Decisión (20 pts)
    p_boundaries = 0
    if "decisionboundarydisplay" in code.lower() or "contourf" in code.lower() or "pcolormesh" in code.lower():
        p_boundaries = 20
    elif "scatter" in code.lower() or "plot" in code.lower():
        p_boundaries = 12
    boundaries_score = p_boundaries
    
    # 4. Análisis y Conclusiones (15 pts)
    p_concl = 0
    concl_keywords = ["conclusi", "ganador", "forma", "curva", "recta", "ortogonal", "probabil", "prolina", "escalar", "magnitud", "interpretacion", "interpretar"]
    matches = sum(1 for k in concl_keywords if k in combined)
    if matches >= 4:
        p_concl = 15
    elif matches >= 2:
        p_concl = 10
    else:
        p_concl = 5
    concl_score = p_concl
    
    total_raw = base_score + reto_score + boundaries_score + concl_score
    total_grade = min(100.0, float(total_raw))
    
    feedback_parts = []
    feedback_parts.append(f"<p><strong>Estimado/a {name}:</strong></p>")
    if is_swapped:
        feedback_parts.append(
            f"<p><em>Nota administrativa:</em> Su archivo fue subido en el casillero de T01 por equivocación, "
            f"pero fue detectado y calificado en este casillero T02 sin penalización.</p>"
        )
    feedback_parts.append(f"<p><strong>Calificación obtenida: {total_grade:g}/100</strong></p>")
    feedback_parts.append("<ul>")
    feedback_parts.append(f"<li><strong>Entrenamiento Base ({base_score}/40):</strong> Carga del dataset Wine, partición estratificada, escalamiento y torneo multimodelo (k-NN, Árbol, Bayes).</li>")
    feedback_parts.append(f"<li><strong>Reto de Ampliación - {tipo_tarea} ({reto_score}/25):</strong> Ejecución del ejercicio autónomo requerido.</li>")
    feedback_parts.append(f"<li><strong>Fronteras de Decisión ({boundaries_score}/20):</strong> Generación gráfica visual de las fronteras espaciales de decisión.</li>")
    feedback_parts.append(f"<li><strong>Análisis y Conclusiones ({concl_score}/15):</strong> Interpretación geométrica y comparativa de los algoritmos.</li>")
    feedback_parts.append("</ul>")
    
    feedback_html = "".join(feedback_parts)
    
    return {
        'nota': total_grade,
        'estado': 'Calificado',
        'detalles': f"Base: {base_score}/40, Reto ({tipo_tarea}): {reto_score}/25, Fronteras: {boundaries_score}/20, Conclusiones: {concl_score}/15",
        'feedback_html': feedback_html,
        'rubro_base': base_score,
        'rubro_reto': reto_score,
        'rubro_fronteras': boundaries_score,
        'rubro_conclusiones': concl_score,
        'archivo': fname
    }

def main():
    parser = argparse.ArgumentParser(description="Calificación y registro de tareas T01 y T02 eCampus")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Modo simulación (sin escribir en Moodle)")
    parser.add_argument("--push", action="store_true", help="Subir calificaciones a Moodle (eCampus)")
    parser.add_argument("--push-t01", action="store_true", help="Subir solo T01 a Moodle")
    parser.add_argument("--push-t02", action="store_true", help="Subir solo T02 a Moodle")
    args = parser.parse_args()

    if args.push or args.push_t01 or args.push_t02:
        args.dry_run = False

    print("=" * 80)
    print("SISTEMA DE CALIFICACIÓN AUTOMATIZADA - CURSO INT210 (MACHINE LEARNING)")
    print(f"Modo: {'SIMULACIÓN (Dry Run - No escribe en Moodle)' if args.dry_run else 'ENVÍO ACTIVO (Push a Moodle)'}")
    print("=" * 80)

    # 1. Fetch roster
    with open(os.path.join(T01_DIR, "submissions_summary.json"), 'r', encoding='utf-8') as f:
        t01_summary = json.load(f)
    with open(os.path.join(T02_DIR, "submissions_summary.json"), 'r', encoding='utf-8') as f:
        t02_summary = json.load(f)

    # Student metadata map
    users_dict = {}
    for s in t01_summary + t02_summary:
        uid = s['userid']
        if uid not in users_dict:
            users_dict[uid] = {
                'id': uid,
                'fullname': s['fullname'],
                'email': s.get('email', '')
            }

    # Filter out teacher
    student_uids = [uid for uid in sorted(users_dict.keys()) if uid != 6668]

    report_t01 = []
    report_t02 = []
    report_consolidado = []

    print(f"\nEvaluando {len(student_uids)} estudiantes matriculados...")

    for uid in student_uids:
        uinfo = users_dict[uid]
        name = uinfo['fullname']
        email = uinfo['email']

        # Evaluate T01
        fpath_t01, swapped_t01 = locate_student_file(uid, name, 'T01')
        res_t01 = grade_t01_submission(uid, name, fpath_t01, swapped_t01)

        # Evaluate T02
        fpath_t02, swapped_t02 = locate_student_file(uid, name, 'T02')
        res_t02 = grade_t02_submission(uid, name, fpath_t02, swapped_t02)

        # Average
        promedio = round((res_t01['nota'] + res_t02['nota']) / 2.0, 1)

        report_t01.append({
            'User_ID': uid,
            'Estudiante': name,
            'Email': email,
            'Nota_100': res_t01['nota'],
            'Estado': res_t01['estado'],
            'Archivo': res_t01['archivo'],
            'Intercambio_Archivo': 'SÍ' if swapped_t01 else 'NO',
            'Preproc_25': res_t01.get('rubro_preproc', 0),
            'Escala_20': res_t01.get('rubro_escalamiento', 0),
            'Modelos_30': res_t01.get('rubro_modelado', 0),
            'Teoria_25': res_t01.get('rubro_teorico', 0),
            'Detalles': res_t01['detalles'],
            'Feedback_HTML': res_t01['feedback_html']
        })

        report_t02.append({
            'User_ID': uid,
            'Estudiante': name,
            'Email': email,
            'Nota_100': res_t02['nota'],
            'Estado': res_t02['estado'],
            'Archivo': res_t02['archivo'],
            'Intercambio_Archivo': 'SÍ' if swapped_t02 else 'NO',
            'Base_40': res_t02.get('rubro_base', 0),
            'Reto_25': res_t02.get('rubro_reto', 0),
            'Fronteras_20': res_t02.get('rubro_fronteras', 0),
            'Conclusiones_15': res_t02.get('rubro_conclusiones', 0),
            'Detalles': res_t02['detalles'],
            'Feedback_HTML': res_t02['feedback_html']
        })

        report_consolidado.append({
            'User_ID': uid,
            'Estudiante': name,
            'Email': email,
            'T01_Nota': res_t01['nota'],
            'T01_Estado': res_t01['estado'],
            'T02_Nota': res_t02['nota'],
            'T02_Estado': res_t02['estado'],
            'Promedio_Tareas': promedio,
            'Observaciones': (
                ("Archivos intercambiados entre T01 y T02; " if (swapped_t01 or swapped_t02) else "") +
                ("T01 sin entrega; " if res_t01['nota'] == 0 else "") +
                ("T02 sin entrega; " if res_t02['nota'] == 0 else "")
            ).strip() or "Regular / Sin incidencias"
        })

    # Save CSV reports
    path_csv_t01 = os.path.join(SCRIPT_DIR, "reporte_calificaciones_T01_420907.csv")
    path_csv_t02 = os.path.join(SCRIPT_DIR, "reporte_calificaciones_T02_420908.csv")
    path_csv_cons = os.path.join(SCRIPT_DIR, "reporte_consolidado_tareas.csv")

    with open(path_csv_t01, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(report_t01[0].keys()))
        w.writeheader()
        w.writerows(report_t01)

    with open(path_csv_t02, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(report_t02[0].keys()))
        w.writeheader()
        w.writerows(report_t02)

    with open(path_csv_cons, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(report_consolidado[0].keys()))
        w.writeheader()
        w.writerows(report_consolidado)

    print("\n" + "=" * 80)
    print("RESUMEN DE CALIFICACIONES (CONSOLIDADO)")
    print("=" * 80)
    print(f"{'ID':<8} | {'Estudiante':<35} | {'T01':<6} | {'T02':<6} | {'Promedio':<8} | {'Observaciones':<30}")
    print("-" * 105)
    for r in report_consolidado:
        print(f"{r['User_ID']:<8} | {r['Estudiante']:<35} | {r['T01_Nota']:<6.1f} | {r['T02_Nota']:<6.1f} | {r['Promedio_Tareas']:<8.1f} | {r['Observaciones']:<30}")

    print(f"\nReportes generados exitosamente:")
    print(f"  - T01: {path_csv_t01}")
    print(f"  - T02: {path_csv_t02}")
    print(f"  - Consolidado: {path_csv_cons}")

    # Optional Push to Moodle
    if not args.dry_run:
        print("\n" + "=" * 80)
        print("SUBIENDO CALIFICACIONES A ECAMPUS MOODLE...")
        print("=" * 80)
        
        # Push T01
        if args.push or args.push_t01:
            print(f"\nSubiendo notas de T01 (Instancia: {T01_INST})...")
            success_count = 0
            for r in report_t01:
                uid = r['User_ID']
                grade = r['Nota_100']
                fb = r['Feedback_HTML']
                if r['Estado'] == 'No entregado':
                    continue
                params = {
                    'assignmentid': T01_INST,
                    'userid': uid,
                    'grade': float(grade),
                    'attemptnumber': -1,
                    'addattempt': 0,
                    'workflowstate': 'graded',
                    'applytoall': 0,
                    'plugindata[assignfeedbackcomments_editor][text]': fb,
                    'plugindata[assignfeedbackcomments_editor][format]': 1
                }
                res = call_moodle('mod_assign_save_grade', params)
                if (res is None) or (isinstance(res, dict) and len(res) == 0) or (res == []):
                    success_count += 1
                    print(f"  [OK] {r['Estudiante']} -> {grade:g}/100")
                else:
                    print(f"  [ERROR] {r['Estudiante']}: {res}")
            print(f"T01 completado: {success_count} notas registradas.")

        # Push T02
        if args.push or args.push_t02:
            print(f"\nSubiendo notas de T02 (Instancia: {T02_INST})...")
            success_count = 0
            for r in report_t02:
                uid = r['User_ID']
                grade = r['Nota_100']
                fb = r['Feedback_HTML']
                if r['Estado'] == 'No entregado':
                    continue
                params = {
                    'assignmentid': T02_INST,
                    'userid': uid,
                    'grade': float(grade),
                    'attemptnumber': -1,
                    'addattempt': 0,
                    'workflowstate': 'graded',
                    'applytoall': 0,
                    'plugindata[assignfeedbackcomments_editor][text]': fb,
                    'plugindata[assignfeedbackcomments_editor][format]': 1
                }
                res = call_moodle('mod_assign_save_grade', params)
                if (res is None) or (isinstance(res, dict) and len(res) == 0) or (res == []):
                    success_count += 1
                    print(f"  [OK] {r['Estudiante']} -> {grade:g}/100")
                else:
                    print(f"  [ERROR] {r['Estudiante']}: {res}")
            print(f"T02 completado: {success_count} notas registradas.")

if __name__ == "__main__":
    main()
