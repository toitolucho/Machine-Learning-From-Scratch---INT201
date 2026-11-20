import os
import json
import re

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

def is_uncommented(pattern, code_cells):
    for c in code_cells:
        src = "".join(c.get("source", []))
        for line in src.split("\n"):
            line_str = line.strip()
            if line_str.startswith("#"):
                continue
            if re.search(pattern, line_str, re.IGNORECASE):
                if "???" not in line_str:
                    return True
    return False

def evaluate_student_strict(uf):
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        return None
    fpath = os.path.join(uf_path, files[0])
    with open(fpath, "r", encoding="utf-8") as fp:
        nb = json.load(fp)
    
    code_cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    
    tasks = {}
    
    # 1.1: primer_nombre
    tasks["1.1"] = is_uncommented(r"primer_nombre\s*=\s*characters_raw\[0\]|characters_raw\[0\]\[[\"']name[\"']\]", code_cells)
    
    # 1.2: list comprehension extracting names
    tasks["1.2"] = is_uncommented(r"\[.*c\[[\"']name[\"']\].*for\s+c\s+in\s+characters_raw.*\]", code_cells)
    
    # 1.3: missing_role
    tasks["1.3"] = is_uncommented(r"missing_role\s*=\s*\[.*c\[[\"']name[\"']\].*if\s+.*role", code_cells)
    
    # 1.4: valid_frames.append
    tasks["1.4"] = is_uncommented(r"valid_frames\.append|error_names\.append", code_cells)
    
    # 2.1: first_color
    tasks["2.1"] = is_uncommented(r"first_color\s*=\s*.*palette.*\[0\]|print\(.*first_color", code_cells)
    
    # 2.2: enumerate(char_5["palette"])
    tasks["2.2"] = is_uncommented(r"for\s+i\s*,\s*\(\s*r\s*,\s*g\s*,\s*b\s*\)\s+in\s+enumerate", code_cells)
    
    # 2.3: brightness_records.append
    tasks["2.3"] = is_uncommented(r"brightness_records\.append", code_cells)
    
    # 2.4: production_lookup =
    tasks["2.4"] = is_uncommented(r"production_lookup\s*=\s*\{", code_cells)
    
    # 3.2: role_corrections applied or Crux role updated
    tasks["3.2"] = is_uncommented(r"role_corrections|characters.*role.*=.*support|Crux.*support", code_cells)
    
    # 3.3: c["fps"] = int(...)
    tasks["3.3"] = is_uncommented(r"c\[[\"']fps[\"']\]\s*=\s*int\(", code_cells)
    
    # 3.4: c["has_special_fx"] = 0
    tasks["3.4"] = is_uncommented(r"c\[[\"']has_special_fx[\"']\]\s*=\s*0", code_cells)
    
    # 3.5: palette_additions applied
    tasks["3.5"] = is_uncommented(r"palette_additions|c\[[\"']palette[\"']\]\.append|palette\.append", code_cells)
    
    # 3.6: state_counts =
    tasks["3.6"] = is_uncommented(r"state_counts\s*=\s*\{", code_cells)
    
    # 4.1: c["num_colors"] =
    tasks["4.1"] = is_uncommented(r"c\[[\"']num_colors[\"']\]\s*=", code_cells)
    
    # 4.3: avg_hours or top_frames
    tasks["4.3"] = is_uncommented(r"avg_hours\s*=|top_frames\s*=|all_hours\s*=", code_cells)
    
    outs = sum(1 for c in code_cells if len(c.get("outputs", [])) > 0)
    cnt = sum(1 for v in tasks.values() if v)
    return tasks, cnt, outs, len(code_cells)

print(f"{'User':<12} | {'Strict Solved/15':<16} | {'Outputs/Total':<14} | Solved Tasks")
print("-" * 80)

for uf in user_folders:
    res = evaluate_student_strict(uf)
    tasks, cnt, outs, tot = res
    done = [k for k, v in tasks.items() if v]
    print(f"{uf:<12} | {cnt:<16} | {outs}/{tot:<12} | {','.join(done) if done else 'Ninguno'}")
