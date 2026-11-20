import os
import json
import re

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

def evaluate_student(uf):
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        return None
    fpath = os.path.join(uf_path, files[0])
    with open(fpath, "r", encoding="utf-8") as fp:
        nb = json.load(fp)
    
    code_cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    
    # We will check each task by looking across all code cells
    tasks_done = {}
    
    def cell_has(pattern, require_no_qm=True):
        for c in code_cells:
            src = "".join(c.get("source", []))
            if require_no_qm and "???" in src:
                # check if the specific pattern is present outside ???
                pass
            if re.search(pattern, src, re.IGNORECASE | re.MULTILINE):
                if not require_no_qm or "???" not in src:
                    return True
        return False

    # 1.1: characters_raw[0] and characters_raw[-1]
    # Check if student accessed first and last
    tasks_done["1.1"] = cell_has(r"characters_raw\[0\].*\[[\"']name[\"']\]|primer_nombre\s*=\s*characters_raw\[0\]")
    
    # 1.2: list comprehension extracting names/roles
    tasks_done["1.2"] = cell_has(r"\[.*c\[[\"']name[\"']\].*for\s+c\s+in\s+characters_raw.*\]")
    
    # 1.3: detection of quality issues (missing role, bad fps, missing fx, short palette)
    tasks_done["1.3"] = cell_has(r"missing_role|c\[[\"']role[\"']\]\s+is\s+None|wrong_fps|isinstance\(c\[[\"']fps[\"']\],\s*str\)")
    
    # 1.4: frames multiplication with try/except TypeError
    tasks_done["1.4"] = cell_has(r"valid_frames.*error_names|except\s+TypeError")
    
    # 2.1: accessing first color and unpacking
    tasks_done["2.1"] = cell_has(r"char.*\[[\"']palette[\"']\]\[0\]|first_color|palette_len")
    
    # 2.2: tuple unpacking in enumerate
    tasks_done["2.2"] = cell_has(r"enumerate\(.*palette.*\)|for\s+i,\s*\(\s*r\s*,\s*g\s*,\s*b\s*\)\s+in")
    
    # 2.3: brightness calculation formula
    tasks_done["2.3"] = cell_has(r"0\.299\s*\*|brightness_records|\(\s*r\s*\+\s*g\s*\+\s*b\s*\)\s*/\s*3")
    
    # 2.4: production_lookup with tuple key
    tasks_done["2.4"] = cell_has(r"production_lookup\s*=\s*\{.*\(c\[[\"']name[\"']\],\s*c\[[\"']style[\"']\]\)")
    
    # 3.2: role_corrections
    tasks_done["3.2"] = cell_has(r"role_corrections|c\[[\"']name[\"']\]\s*==\s*[\"']Crux[\"']|[\"']Crux[\"']:\s*[\"']support[\"']")
    
    # 3.3: fps type correction
    tasks_done["3.3"] = cell_has(r"int\(c\[[\"']fps[\"']\]\)|c\[[\"']fps[\"']\]\s*=\s*int\(")
    
    # 3.4: has_special_fx = 0 correction
    tasks_done["3.4"] = cell_has(r"c\[[\"']has_special_fx[\"']\]\s*=\s*0")
    
    # 3.5: palette additions
    tasks_done["3.5"] = cell_has(r"palette_additions|c\[[\"']palette[\"']\]\.append\(\s*\(240,\s*250,\s*255\)\s*\)|240,\s*250,\s*255")
    
    # 3.6: state counts dict comprehension
    tasks_done["3.6"] = cell_has(r"state_counts\s*=\s*\{.*len\(c\[[\"']states[\"']\]\)")
    
    # 4.1: num_colors, avg_brightness, color_contrast derived fields
    tasks_done["4.1"] = cell_has(r"c\[[\"']num_colors[\"']\]\s*=|c\[[\"']color_contrast[\"']\]\s*=")
    
    # 4.3: summary stats (avg_hours, top_frames, top_screen, top_hours)
    tasks_done["4.3"] = cell_has(r"top_frames|avg_hours|top_screen|top_hours")
    
    executed_cells = sum(1 for c in code_cells if len(c.get("outputs", [])) > 0)
    solved_count = sum(1 for v in tasks_done.values() if v)
    
    return tasks_done, solved_count, executed_cells, len(code_cells)

print(f"{'User':<12} | {'Solved/15':<10} | {'Outputs/Total':<15} | Solved Tasks")
print("-" * 80)

for uf in user_folders:
    td, cnt, outs, tot = evaluate_student(uf)
    done_list = [k for k, v in td.items() if v]
    print(f"{uf:<12} | {cnt:<10} | {outs}/{tot:<13} | {','.join(done_list) if done_list else 'Ninguno'}")
