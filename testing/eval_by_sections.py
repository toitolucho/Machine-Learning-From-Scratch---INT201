import os
import json
import re

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

TARGET_EXERCISES = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.2", "3.3", "3.4", "3.5", "3.6", "4.1", "4.3"]

def evaluate_student_by_sections(fpath):
    with open(fpath, "r", encoding="utf-8") as fp:
        nb = json.load(fp)
    
    current_ex = None
    task_cells = {}
    
    for idx, c in enumerate(nb.get("cells", [])):
        src = "".join(c.get("source", []))
        if c.get("cell_type") == "markdown":
            # Match Ejercicio X.Y
            m = re.search(r"Ejercicio\s+([0-9]+\.[0-9]+)", src)
            if m:
                ex_num = m.group(1)
                if ex_num in TARGET_EXERCISES:
                    current_ex = ex_num
        elif c.get("cell_type") == "code":
            if current_ex:
                # Check if this code cell is an example cell
                is_example = "# Ejemplo -- no modificar" in src or "# Ejemplo" in src
                if not is_example:
                    # This is the student task cell!
                    # If there are multiple code cells in this section, pick the one that has Completa or is not an assert
                    if current_ex not in task_cells or "# Completa" in src or "???" in src:
                        task_cells[current_ex] = (idx, c)
                        
    # Now evaluate each task cell
    eval_results = {}
    for ex in TARGET_EXERCISES:
        if ex not in task_cells:
            eval_results[ex] = False
            continue
            
        c_idx, cell = task_cells[ex]
        src = "".join(cell.get("source", []))
        has_qm = "???" in src
        
        # Check active code lines (not comments)
        active_lines = [l.strip() for l in src.split("\n") if l.strip() and not l.strip().startswith("#")]
        
        # Must have no ??? and at least one real active code line
        is_done = (not has_qm) and (len(active_lines) > 0)
        
        # Special check: if all active lines are just 'pass'
        if all(l == "pass" for l in active_lines):
            is_done = False
            
        eval_results[ex] = is_done
        
    return eval_results

print(f"{'User':<12} | {'Solved':<8} | Solved Exercises List")
print("-" * 75)

for uf in user_folders:
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        continue
    fpath = os.path.join(uf_path, files[0])
    res = evaluate_student_by_sections(fpath)
    solved = [k for k, v in res.items() if v]
    print(f"{uf:<12} | {len(solved):<8} | {','.join(solved) if solved else 'Ninguno'}")
