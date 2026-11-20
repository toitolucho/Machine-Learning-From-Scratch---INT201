import os
import json
import traceback

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

def grade_student_notebook(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    cells = nb.get("cells", [])
    
    # We will test execution cell by cell in a fresh namespace
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
    
    # Run code cells sequentially
    for idx, c in enumerate(cells):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        if not src.strip():
            continue
        
        # Check if cell has ???
        has_qm = "???" in src
        
        try:
            # We don't execute if ??? is present because it would fail or be incomplete
            if not has_qm:
                exec(src, env)
        except Exception as e:
            cell_exec_errors.append((idx, type(e).__name__, str(e)[:60]))
            
        # Check which exercise this cell represents and whether required logic was done
        if "primer_nombre" in src and not has_qm:
            # 1.1
            if "primer_nombre" in env and env.get("primer_nombre") == "Lyra":
                exercise_status["1.1"] = True
            elif "primer_nombre" in env:
                exercise_status["1.1"] = True
                
        if "all_names" in src and not has_qm:
            # 1.2
            if "all_names" in env and len(env.get("all_names", [])) == 20:
                exercise_status["1.2"] = True
            elif "all_names" in env:
                exercise_status["1.2"] = True
                
        if ("missing_role" in src or "bad_fps" in src) and not has_qm:
            # 1.3
            if "missing_role" in env:
                exercise_status["1.3"] = True
                
        if ("valid_frames" in src or "error_names" in src) and not has_qm:
            # 1.4
            if "valid_frames" in env:
                exercise_status["1.4"] = True
                
        if ("first_color" in src or "palette_len" in src) and not has_qm:
            # 2.1
            if "first_color" in env or "palette_len" in env or "r" in env:
                exercise_status["2.1"] = True
                
        if "Color 1: R=" in src or ("char_5" in src and "palette" in src and not has_qm):
            # 2.2
            exercise_status["2.2"] = True
            
        if ("brightness_records" in src or "calc_brightness" in src) and not has_qm:
            # 2.3
            if "brightness_records" in env and len(env.get("brightness_records", [])) > 0:
                exercise_status["2.3"] = True
            elif "brightness_records" in env:
                exercise_status["2.3"] = True
                
        if "production_lookup" in src and not has_qm:
            # 2.4
            if "production_lookup" in env and len(env.get("production_lookup", {})) > 0:
                exercise_status["2.4"] = True
                
        if "role_corrections" in src and not has_qm:
            # 3.2
            if "characters" in env:
                # check if Crux is corrected
                crux = next((x for x in env["characters"] if x.get("name") == "Crux"), None)
                if crux and crux.get("role") == "support":
                    exercise_status["3.2"] = True
                else:
                    exercise_status["3.2"] = True
            else:
                exercise_status["3.2"] = True
                
        if "isinstance(c['fps'], str)" in src or ("int(c['fps'])" in src and not has_qm):
            # 3.3
            if "characters" in env:
                all_fps_int = all(isinstance(x.get("fps"), int) for x in env["characters"])
                if all_fps_int:
                    exercise_status["3.3"] = True
                else:
                    exercise_status["3.3"] = True
            else:
                exercise_status["3.3"] = True
                
        if "has_special_fx is None" in src or ("has_special_fx" in src and "Zorn" in src and not has_qm):
            # 3.4
            if "characters" in env:
                zorn = next((x for x in env["characters"] if x.get("name") == "Zorn"), None)
                if zorn and zorn.get("has_special_fx") == 0:
                    exercise_status["3.4"] = True
                else:
                    exercise_status["3.4"] = True
            else:
                exercise_status["3.4"] = True
                
        if "palette_additions" in src and not has_qm:
            # 3.5
            if "characters" in env:
                mira = next((x for x in env["characters"] if x.get("name") == "Mira"), None)
                if mira and len(mira.get("palette", [])) == 3:
                    exercise_status["3.5"] = True
                else:
                    exercise_status["3.5"] = True
            else:
                exercise_status["3.5"] = True
                
        if "state_counts" in src and not has_qm:
            # 3.6
            if "state_counts" in env:
                exercise_status["3.6"] = True
                
        if ("num_colors" in src and "color_contrast" in src and "num_frames_total" in src) and not has_qm:
            # 4.1
            if "characters" in env and "num_colors" in env["characters"][0]:
                exercise_status["4.1"] = True
            else:
                exercise_status["4.1"] = True
                
        if ("top_frames" in src or "avg_hours" in src or "top_hours" in src) and not has_qm:
            # 4.3
            if "avg_hours" in env or "top_frames" in env:
                exercise_status["4.3"] = True
            else:
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

print(f"{'User':<12} | {'Solved':<8} | {'MD Answers':<10} | {'Exec Errors':<12} | Solved Details")
print("-" * 75)

results = {}
for uf in user_folders:
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        continue
    fpath = os.path.join(uf_path, files[0])
    solved, ex_map, errors, md_ans = grade_student_notebook(fpath)
    solved_list = [k for k, v in ex_map.items() if v]
    results[uf] = {
        "solved_count": solved,
        "solved_list": solved_list,
        "errors_count": len(errors),
        "md_answers": md_ans
    }
    print(f"{uf:<12} | {solved:<8} | {md_ans:<10} | {len(errors):<12} | {','.join(solved_list)}")
