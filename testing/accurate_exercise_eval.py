import os
import json
import re

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

# Identify each exercise by its unique signature in the template
# and find the corresponding cell in the student notebook
exercise_signatures = {
    "1.1": ["primer_nombre", "ultimo_nombre", "characters_raw[0]"],
    "1.2": ["all_names", "names = [c", "protagonists = [c"],
    "1.3": ["missing_role", "wrong_fps", "missing_fx", "short_palette", "bad_fps"],
    "1.4": ["valid_frames", "error_names", "TypeError"],
    "2.1": ["first_color", "palette_len", "char = characters_raw[0]"],
    "2.2": ["char_5", "palette_5", "enumerate("],
    "2.3": ["brightness_records", "0.299", "brightest = max("],
    "2.4": ["production_lookup", "('Lyra', 'cel_shaded')"],
    "3.2": ["role_corrections", '"Rex"'],
    "3.3": ['c["fps"]', "isinstance(c['fps'], str)", "int(c["],
    "3.4": ['has_special_fx', '"has_special_fx"] = 0'],
    "3.5": ["palette_additions", '"Mira"', '"Drak"'],
    "3.6": ["state_counts", 'len(c["states"])'],
    "4.1": ['num_colors', 'avg_brightness', 'color_contrast', 'num_frames_total'],
    "4.3": ["avg_hours", "top_frames", "top_screen", "top_hours"]
}

def evaluate_notebook_cells(fpath):
    with open(fpath, "r", encoding="utf-8") as fp:
        nb = json.load(fp)
    
    code_cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    
    exercise_eval = {}
    
    for ex_id, sigs in exercise_signatures.items():
        found_cell = None
        for c in code_cells:
            src = "".join(c.get("source", []))
            # must match at least 2 signatures or primary signature
            if any(s in src for s in sigs):
                # Avoid matching example cells (which have '# Ejemplo -- no modificar')
                if "# Ejemplo -- no modificar" in src or "# Ejemplo" in src:
                    continue
                found_cell = c
                break
                
        if not found_cell:
            exercise_eval[ex_id] = {
                "status": "NOT_FOUND",
                "completed": False,
                "has_qm": False,
                "has_output": False
            }
            continue
            
        src = "".join(found_cell.get("source", []))
        outputs = found_cell.get("outputs", [])
        has_qm = "???" in src
        has_out = len(outputs) > 0
        
        # Check if actual code lines are uncommented
        lines = [l.strip() for l in src.split("\n") if l.strip()]
        code_lines = [l for l in lines if not l.startswith("#")]
        
        # An exercise is completed if:
        # 1. No ??? in the code
        # 2. At least 2 active non-comment lines
        # 3. Solved specific logic
        is_completed = (not has_qm) and len(code_lines) >= 2
        
        # Specific sanity checks for tricky cells:
        if ex_id == "3.2":
            # Must not have ??? on Rex
            if '???' in src:
                is_completed = False
            # Must have uncommented for loop applying corrections
            if not any("role_corrections" in l and not l.startswith("#") for l in lines):
                is_completed = False
        elif ex_id == "3.4":
            if not any("has_special_fx" in l and "0" in l and not l.startswith("#") for l in lines):
                is_completed = False
        elif ex_id == "3.5":
            if '???' in src:
                is_completed = False
        elif ex_id == "4.1":
            if not any("num_colors" in l and not l.startswith("#") for l in lines):
                is_completed = False
        elif ex_id == "4.3":
            if not any("avg_hours" in l and not l.startswith("#") for l in lines):
                is_completed = False
                
        exercise_eval[ex_id] = {
            "status": "COMPLETED" if is_completed else "INCOMPLETE",
            "completed": is_completed,
            "has_qm": has_qm,
            "has_output": has_out,
            "code_lines_count": len(code_lines)
        }
        
    return exercise_eval

print(f"{'User':<12} | {'Solved/15':<10} | {'Outputs':<8} | Solved List")
print("-" * 75)

all_student_grades = {}

for uf in user_folders:
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        continue
    fpath = os.path.join(uf_path, files[0])
    eval_res = evaluate_notebook_cells(fpath)
    solved = [k for k, v in eval_res.items() if v["completed"]]
    outputs_count = sum(1 for v in eval_res.values() if v["has_output"])
    all_student_grades[uf] = {
        "solved_count": len(solved),
        "solved": solved,
        "outputs_count": outputs_count,
        "details": eval_res
    }
    print(f"{uf:<12} | {len(solved):<10} | {outputs_count:<8} | {','.join(solved) if solved else 'Ninguno'}")
