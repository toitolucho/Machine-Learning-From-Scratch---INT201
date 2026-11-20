import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
t02_dir = os.path.join(script_dir, "tarea_420908_inst_77381")
with open(os.path.join(t02_dir, "submissions_summary.json"), 'r', encoding='utf-8') as f:
    subs = json.load(f)

for s in subs:
    uid = s['userid']
    name = s['fullname']
    if s.get('status') != 'submitted':
        continue
    # handle swapped
    folder = os.path.join(script_dir, "tarea_420907_inst_77380" if uid in [189741, 193316] else "tarea_420908_inst_77381", f"User_{uid}_{name.replace(' ', '_')}")
    nb_files = []
    for r, d, fs in os.walk(folder):
        for f in fs:
            if f.endswith(('.ipynb', '.py')) and ('05_' in f or 'Comparacion' in f or 't2' in f or 'tarea_2' in f or 'tarea2' in f or 'MAPACALOR' in f or 'Modulo' in f or 'Módulo' in f):
                nb_files.append(os.path.join(r, f))
    if not nb_files:
        print(f"UID {uid} ({name}): NO T02 FILE FOUND!")
        continue
    fpath = nb_files[0]
    with open(fpath, 'r', encoding='utf-8', errors='replace') as fp:
        raw = fp.read().lower()
    
    has_corr_hw = "corr" in raw and ("heatmap" in raw or "prolina" in raw or "fenoles" in raw or "tercera" in raw or "3ra" in raw)
    has_logreg_hw = "logisticregression" in raw or "regresion logistica" in raw or "regresión logística" in raw
    has_pipeline_hw = "pipeline" in raw
    has_minmax_hw = "minmaxscaler" in raw
    
    status = "FULL HW" if (has_corr_hw or has_logreg_hw or has_pipeline_hw) else ("ALT HW" if has_minmax_hw else "ONLY CLASS TUTORIAL")
    print(f"UID {uid:<8} | {name:<35} | {status:<20} | File: {os.path.basename(fpath)}")

