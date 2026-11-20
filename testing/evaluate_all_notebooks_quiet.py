import os
import json
import io
import sys
import contextlib

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

def grade_student_notebook(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    cells = nb.get("cells", [])
    env = {}
    
    exercise_status = {
        "1.1": False,
        "1.2": False,
        "1.3": False,
        "1.4": False,
        "2.1": False,
        "2.2": False,
        "2.3": False,
        "2.4": False,
        "3.2": False,
        "3.3": False,
        "3.4": False,
        "3.5": False,
        "3.6": False,
        "4.1": False,
        "4.3": False
    }
    
    cell_exec_errors = []
    
    # Run code cells sequentially with stdout suppressed
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        for idx, c in enumerate(cells):
            if c.get("cell_type") != "code":
                continue
            src = "".join(c.get("source", []))
            if not src.strip():
                continue
            
            has_qm = "???" in src
            
            try:
                if not has_qm:
                    exec(src, env)
            except Exception as e:
                cell_exec_errors.append((idx, type(e).__name__, str(e)[:60]))
                
            # Exercise detection
            if "primer_nombre" in src and not has_qm:
                if "primer_nombre" in env:
                    exercise_status["1.1"] = True
                    
            if "all_names" in src and not has_qm:
                if "all_names" in env:
                    exercise_status["1.2"] = True
                    
            if ("missing_role" in src or "bad_fps" in src) and not has_qm:
                if "missing_role" in env:
                    exercise_status["1.3"] = True
                    
            if ("valid_frames" in src or "error_names" in src) and not has_qm:
                if "valid_frames" in env:
                    exercise_status["1.4"] = True
                    
            if ("first_color" in src or "palette_len" in src) and not has_qm:
                if "first_color" in env or "palette_len" in env or "r" in env:
                    exercise_status["2.1"] = True
                    
            if "Color 1: R=" in src or ("char_5" in src and "palette" in src and not has_qm):
                exercise_status["2.2"] = True
                
            if ("brightness_records" in src or "calc_brightness" in src) and not has_qm:
                if "brightness_records" in env:
                    exercise_status["2.3"] = True
                    
            if "production_lookup" in src and not has_qm:
                if "production_lookup" in env:
                    exercise_status["2.4"] = True
                    
            if "role_corrections" in src and not has_qm:
                exercise_status["3.2"] = True
                    
            if "isinstance(c['fps'], str)" in src or ("int(c['fps'])" in src and not has_qm):
                exercise_status["3.3"] = True
                    
            if "has_special_fx is None" in src or ("has_special_fx" in src and "Zorn" in src and not has_qm):
                exercise_status["3.4"] = True
                    
            if "palette_additions" in src and not has_qm:
                exercise_status["3.5"] = True
                    
            if "state_counts" in src and not has_qm:
                if "state_counts" in env:
                    exercise_status["3.6"] = True
                    
            if ("num_colors" in src and "color_contrast" in src and "num_frames_total" in src) and not has_qm:
                exercise_status["4.1"] = True
                    
            if ("top_frames" in src or "avg_hours" in src or "top_hours" in src) and not has_qm:
                if "avg_hours" in env or "top_frames" in env:
                    exercise_status["4.3"] = True

    # Also check markdown responses
    md_answers = 0
    for c in cells:
        if c.get("cell_type") == "markdown":
            src = "".join(c.get("source", []))
            if any(k in src.lower() for k in ["**respuesta", "respuesta:", "rta:"]):
                md_answers += 1
                
    solved_count = sum(1 for v in exercise_status.values() if v)
    return solved_count, exercise_status, cell_exec_errors, md_answers

print(f"{'User':<12} | {'Solved/15':<10} | {'MD Ans':<8} | {'Errors':<8} | Solved Exercises List")
print("-" * 85)

for uf in user_folders:
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        print(f"{uf:<12} | NO FILES")
        continue
    fpath = os.path.join(uf_path, files[0])
    solved, ex_map, errors, md_ans = grade_student_notebook(fpath)
    solved_list = [k for k, v in ex_map.items() if v]
    print(f"{uf:<12} | {solved:<10} | {md_ans:<8} | {len(errors):<8} | {','.join(solved_list) if solved_list else 'Ninguno'}")
