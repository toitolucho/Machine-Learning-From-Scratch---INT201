import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
t01_dir = os.path.join(script_dir, "tarea_420907_inst_77380")
t02_dir = os.path.join(script_dir, "tarea_420908_inst_77381")

def load_file_content(path):
    if not path or not os.path.exists(path):
        return "", ""
    code_text = []
    md_text = []
    if path.endswith('.ipynb'):
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as fp:
                nb = json.load(fp)
            for c in nb.get('cells', []):
                ctype = c.get('cell_type')
                src = "".join(c.get('source', []))
                if ctype == 'code':
                    code_text.append(src)
                elif ctype == 'markdown':
                    md_text.append(src)
        except Exception as e:
            code_text.append(f"Error: {e}")
    elif path.endswith('.py'):
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as fp:
                src = fp.read()
            code_text.append(src)
            docstrings = re.findall(r'"""(.*?)"""', src, re.DOTALL)
            md_text.extend(docstrings)
        except Exception as e:
            code_text.append(f"Error: {e}")
    return "\n\n".join(code_text), "\n\n".join(md_text)

print("=" * 70)
print("INSPECTING T02 DETAILS FOR ALL SUBMITTED STUDENTS")
print("=" * 70)

with open(os.path.join(t02_dir, "submissions_summary.json"), 'r', encoding='utf-8') as f:
    t02_subs = json.load(f)

for s in t02_subs:
    uid = s['userid']
    name = s['fullname']
    if s.get('status') != 'submitted':
        continue
        
    u1_folder = os.path.join(t01_dir, f"User_{uid}_{name.replace(' ', '_')}")
    u2_folder = os.path.join(t02_dir, f"User_{uid}_{name.replace(' ', '_')}")
    
    target_path = None
    if uid in [189741, 193316]:
        # Swapped: T02 was uploaded in T01 folder
        for r, d, fs in os.walk(u1_folder):
            for f in fs:
                if f.endswith('.ipynb') and ('05_' in f or 'Comparacion' in f):
                    target_path = os.path.join(r, f)
    else:
        for r, d, fs in os.walk(u2_folder):
            for f in fs:
                if f.endswith(('.ipynb', '.py')) and not f.startswith('.'):
                    target_path = os.path.join(r, f)
                    break
            if target_path:
                break
                
    code, md = load_file_content(target_path)
    combined = (code + "\n" + md).lower()
    
    # 1. Heatmap / Correlation
    has_corr = "corr(" in code.lower() or "heatmap" in code.lower()
    
    # 2. Third feature identified
    feat_detected = []
    for feat in ["prolina", "proline", "fenoles", "phenols", "od280", "matiz", "hue", "magnesio", "intensidad_color", "color_intensity", "alcalinidad"]:
        if feat in combined:
            feat_detected.append(feat)
            
    # 3. Decision boundaries
    has_boundaries = "decisionboundarydisplay" in code.lower() or "contourf" in code.lower() or "pcolormesh" in code.lower()
    
    # 4. Pair plotting / scatter
    has_pairs = "pairplot" in code.lower() or "scatter" in code.lower() or "subplots" in code.lower()
    
    # 5. Conclusions / written analysis
    has_concl = any(k in combined for k in ["conclusi", "ganador", "representacion", "representación", "curvas", "ortogonales", "escalamiento", "standardscaler"])
    
    print(f"\nStudent: {name:<32} (UID: {uid}) | File: {os.path.basename(target_path) if target_path else 'None'}")
    print(f"  Heatmap/Corr: {has_corr} | Boundaries: {has_boundaries} | Pairs/Scatter: {has_pairs}")
    print(f"  Features mentioned: {', '.join(feat_detected[:5])}")
    print(f"  Conclusions written: {has_concl}")

