import os
import json

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

exercise_cells = [7, 12, 17, 22, 28, 33, 38, 43, 51, 56, 59, 64, 69, 73, 77]
exercise_names = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.2", "3.3", "3.4", "3.5", "3.6", "4.1", "4.3"]

print(f"{'User':<12} | {'Completed Cells':<16} | {'??? Left':<10} | {'Outputs Present':<16} | Details")
print("-" * 80)

for uf in user_folders:
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        print(f"{uf:<12} | NO FILES")
        continue
    fpath = os.path.join(uf_path, files[0])
    try:
        with open(fpath, "r", encoding="utf-8") as fp:
            nb = json.load(fp)
    except Exception as e:
        print(f"{uf:<12} | ERROR: {e}")
        continue
    
    cells = nb.get("cells", [])
    completed = []
    question_marks = []
    outputs = []
    
    # Check if student modified cell indices or if they match exercise_cells
    for i, ex_idx in enumerate(exercise_cells):
        if ex_idx < len(cells):
            src = "".join(cells[ex_idx].get("source", []))
            has_qm = "???" in src
            has_out = len(cells[ex_idx].get("outputs", [])) > 0
            if has_qm:
                question_marks.append(exercise_names[i])
            else:
                completed.append(exercise_names[i])
            if has_out:
                outputs.append(exercise_names[i])
        else:
            question_marks.append(exercise_names[i])
            
    print(f"{uf:<12} | {len(completed)} / {len(exercise_cells):<11} | {len(question_marks):<10} | {len(outputs):<16} | Done: {','.join(completed[:4])}...")
