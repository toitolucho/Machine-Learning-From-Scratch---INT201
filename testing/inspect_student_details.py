import os
import json
import re

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

def analyze_student(uf):
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        return None
    fpath = os.path.join(uf_path, files[0])
    with open(fpath, "r", encoding="utf-8") as fp:
        nb = json.load(fp)
    
    cells = nb.get("cells", [])
    
    # Concatenate all code cells to search for implementations
    # and also inspect individual code cells
    code_cells = [c for c in cells if c.get("cell_type") == "code"]
    
    results = {}
    
    # 1.1: primer_nombre
    # Must have characters_raw[0] or primer_nombre assigned without ???
    c11 = any(re.search(r"primer_nombre\s*=\s*characters_raw\[0\]", "".join(c.get("source", []))) for c in code_cells)
    results["1.1"] = c11
    
    # 1.2: all_names comprehension
    c12 = any(re.search(r"all_names\s*=\s*\[.*c\[[\"']name[\"']\].*for\s+c\s+in\s+characters_raw.*\]", "".join(c.get("source", []))) for c in code_cells)
    results["1.2"] = c12
    
    # 1.3: missing_role, bad_fps, missing_fx, incomplete_palette
    c13 = any("missing_role" in "".join(c.get("source", [])) and "bad_fps" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["1.3"] = c13
    
    # 1.4: valid_frames, error_names with try/except
    c14 = any("valid_frames" in "".join(c.get("source", [])) and "TypeError" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["1.4"] = c14
    
    # 2.1: first_color and r, g, b unpacking
    c21 = any("first_color" in "".join(c.get("source", [])) and "palette_len" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["2.1"] = c21
    
    # 2.2: tuple unpacking in enumerate
    c22 = any("enumerate(palette_5" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["2.2"] = c22
    
    # 2.3: brightness calculation
    c23 = any("brightness_records" in "".join(c.get("source", [])) and "0.299" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["2.3"] = c23
    
    # 2.4: production_lookup
    c24 = any("production_lookup" in "".join(c.get("source", [])) and "production_hours" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["2.4"] = c24
    
    # 3.2: role_corrections
    c32 = any("role_corrections" in "".join(c.get("source", [])) and "Crux" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["3.2"] = c32
    
    # 3.3: int(c["fps"])
    c33 = any("isinstance" in "".join(c.get("source", [])) and "int(c" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["3.3"] = c33
    
    # 3.4: has_special_fx
    # Student must have uncommented `c["has_special_fx"] = 0` or similar
    c34 = any(re.search(r"^\s*c\[[\"']has_special_fx[\"']\]\s*=\s*0", "".join(c.get("source", [])), re.MULTILINE) for c in code_cells)
    results["3.4"] = bool(c34)
    
    # 3.5: palette_additions
    c35 = any("palette_additions" in "".join(c.get("source", [])) and "(240, 250, 255)" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["3.5"] = c35
    
    # 3.6: state_counts
    c36 = any("state_counts" in "".join(c.get("source", [])) and "len(c" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["3.6"] = c36
    
    # 4.1: num_colors, avg_brightness in loop
    c41 = any(re.search(r"^\s*c\[[\"']num_colors[\"']\]\s*=", "".join(c.get("source", [])), re.MULTILINE) for c in code_cells)
    results["4.1"] = bool(c41)
    
    # 4.3: top_frames, avg_hours
    c43 = any("top_frames" in "".join(c.get("source", [])) and "avg_hours" in "".join(c.get("source", [])) and "???" not in "".join(c.get("source", [])) for c in code_cells)
    results["4.3"] = c43
    
    # Check execution outputs in student notebook
    cells_with_output = sum(1 for c in code_cells if len(c.get("outputs", [])) > 0)
    
    # Check answered markdown questions
    md_answers = 0
    for c in cells:
        if c.get("cell_type") == "markdown":
            src = "".join(c.get("source", []))
            if any(k in src.lower() for k in ["**respuesta", "respuesta:", "rta:"]):
                md_answers += 1
                
    return {
        "results": results,
        "solved_count": sum(1 for v in results.values() if v),
        "cells_with_output": cells_with_output,
        "total_code_cells": len(code_cells),
        "md_answers": md_answers
    }

print(f"{'User':<12} | {'Solved/15':<10} | {'Outputs':<8} | {'MD Ans':<8} | Solved Exercises")
print("-" * 80)
for uf in user_folders:
    res = analyze_student(uf)
    if not res:
        print(f"{uf:<12} | NO FILES")
        continue
    solved_keys = [k for k, v in res['results'].items() if v]
    print(f"{uf:<12} | {res['solved_count']:<10} | {res['cells_with_output']:<8} | {res['md_answers']:<8} | {','.join(solved_keys) if solved_keys else 'Ninguno'}")
