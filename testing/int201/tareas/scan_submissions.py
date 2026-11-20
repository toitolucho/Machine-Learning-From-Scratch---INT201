import os
import sys
import json
import zipfile
import glob

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
t01_dir = os.path.join(script_dir, "tarea_420907_inst_77380")
t02_dir = os.path.join(script_dir, "tarea_420908_inst_77381")

def scan_assignment(assign_dir, label):
    print("=" * 70)
    print(f"SCANNING {label} ({assign_dir})")
    print("=" * 70)
    
    with open(os.path.join(assign_dir, "submissions_summary.json"), "r", encoding="utf-8") as f:
        subs = json.load(f)
        
    print(f"Total enrolled / summary records: {len(subs)}")
    
    for s in subs:
        uid = s['userid']
        name = s['fullname']
        status = s['status']
        files = s['files']
        
        folder = os.path.join(assign_dir, f"User_{uid}_{name.replace(' ', '_')}")
        all_files = []
        if os.path.exists(folder):
            for r, d, fs in os.walk(folder):
                for f in fs:
                    all_files.append(os.path.relpath(os.path.join(r, f), folder))
                    
        # Identify what type of content is present
        # Detect if student mistakenly uploaded the other homework
        content_type = "UNKNOWN"
        has_wbcd = False
        has_wine = False
        
        for f in all_files:
            lower = f.lower()
            if any(k in lower for k in ["02_", "wbcd", "laboratorio_evaluacion", "laboratorio_evalucion", "clinica"]):
                has_wbcd = True
            if any(k in lower for k in ["05_", "vino", "wine", "comparacion_clasificadores", "mapacalor", "correlacion"]):
                has_wine = True
                
        # If still unknown, inspect contents of .ipynb or .py
        for f in all_files:
            f_abs = os.path.join(folder, f)
            if f.endswith('.ipynb'):
                try:
                    with open(f_abs, "r", encoding="utf-8", errors="replace") as fp:
                        nb = json.load(fp)
                    full_text = " ".join("".join(c.get("source", [])) for c in nb.get("cells", []))
                    if "wbcd" in full_text.lower() or "breast" in full_text.lower() or "maligno" in full_text.lower():
                        has_wbcd = True
                    if "wine" in full_text.lower() or "vino" in full_text.lower() or "prolina" in full_text.lower() or "flavonoides" in full_text.lower():
                        has_wine = True
                except Exception:
                    pass
            elif f.endswith('.py'):
                try:
                    with open(f_abs, "r", encoding="utf-8", errors="replace") as fp:
                        txt = fp.read()
                    if "wbcd" in txt.lower() or "breast" in txt.lower() or "maligno" in txt.lower():
                        has_wbcd = True
                    if "wine" in txt.lower() or "vino" in txt.lower() or "prolina" in txt.lower() or "flavonoides" in txt.lower():
                        has_wine = True
                except Exception:
                    pass
                    
        notes = []
        if has_wbcd and has_wine:
            content_type = "BOTH (WBCD + Wine)"
        elif has_wbcd:
            content_type = "T01 (WBCD/Breast Cancer)"
        elif has_wine:
            content_type = "T02 (Wine Classifiers)"
        else:
            content_type = "EMPTY / NO SUBMISSION" if not all_files else "OTHER"
            
        print(f"User {uid:<8} | {name:<35} | Status: {status:<10} | Type: {content_type:<24} | Files: {', '.join(all_files[:3])}")

if __name__ == "__main__":
    scan_assignment(t01_dir, "T01 (Expected: WBCD)")
    scan_assignment(t02_dir, "T02 (Expected: Wine)")

