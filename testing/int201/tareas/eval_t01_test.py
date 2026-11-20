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
print("INSPECTING T01 DETAILS FOR ALL SUBMITTED STUDENTS")
print("=" * 70)

with open(os.path.join(t01_dir, "submissions_summary.json"), 'r', encoding='utf-8') as f:
    t01_subs = json.load(f)

for s in t01_subs:
    uid = s['userid']
    name = s['fullname']
    if s.get('status') != 'submitted':
        continue
        
    u1_folder = os.path.join(t01_dir, f"User_{uid}_{name.replace(' ', '_')}")
    u2_folder = os.path.join(t02_dir, f"User_{uid}_{name.replace(' ', '_')}")
    
    target_path = None
    if uid in [189741, 193316]:
        # Swapped: T01 was uploaded in T02 folder
        for r, d, fs in os.walk(u2_folder):
            for f in fs:
                if f.endswith('.ipynb') and ('02_' in f or 'Laboratorio_Evaluacion' in f):
                    target_path = os.path.join(r, f)
    else:
        for r, d, fs in os.walk(u1_folder):
            for f in fs:
                if f.endswith(('.ipynb', '.py')) and not f.startswith('.'):
                    target_path = os.path.join(r, f)
                    break
            if target_path:
                break
                
    code, md = load_file_content(target_path)
    combined = code + "\n" + md
    
    # 1. Preprocessing
    has_map = any(k in code for k in ["['M']: 1", "map({'M': 1", "map({'M':1", "'M': 1", "'M':1", "load_breast_cancer"])
    has_split = "train_test_split" in code
    has_xy = any(k in code for k in ["iloc[:, 2:]", "iloc[:,2:]", "drop(", "X =", "X="])
    
    # 2. Scaling
    has_scaler = "StandardScaler" in code
    has_fit_trans = "fit_transform" in code
    has_trans_test = any(k in code for k in ["transform(X_test", "transform(X_test_scaled", "transform(X_test)"])
    
    # 3. Modeling
    has_knn = "KNeighborsClassifier" in code
    has_tree = "DecisionTreeClassifier" in code
    has_cm = "confusion_matrix" in code
    
    # 4. Answers
    q1_found = any(k in combined.lower() for k in ["falso negativo", "tipo ii", "error tipo 2", "error tipo ii", "vida", "maligno"])
    q2_found = any(k in combined.lower() for k in ["escalar", "escala", "arbol", "árbol", "distancia", "umbral", "jerarquic", "particion", "reglas"])
    
    # Check answers text
    # Let's extract what student wrote for questions
    ans_text = ""
    for piece in md.split("\n\n"):
        if any(k in piece.lower() for k in ["evaluación teórica", "decisión de negocios", "1.", "2.", "error tipo ii", "r:", "r.-"]):
            ans_text += piece + "\n"
            
    print(f"\nStudent: {name:<32} (UID: {uid}) | File: {os.path.basename(target_path) if target_path else 'None'}")
    print(f"  Preproc: Map={has_map}, Split={has_split}, XY={has_xy}")
    print(f"  Scaling: Scaler={has_scaler}, FitTrain={has_fit_trans}, TransTest={has_trans_test}")
    print(f"  Modeling: KNN={has_knn}, Tree={has_tree}, CM={has_cm}")
    print(f"  Answers detected: Q1={q1_found}, Q2={q2_found}")
    if ans_text:
        lines = [l.strip() for l in ans_text.split("\n") if l.strip()]
        sample_ans = " | ".join(lines[-4:]) if len(lines) >= 4 else " | ".join(lines)
        print(f"  Sample text: {sample_ans[:140]}")
