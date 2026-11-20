import json
import glob
import os

t02_base = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381"
nbs = glob.glob(os.path.join(t02_base, "**", "*.ipynb"), recursive=True)

for p in nbs[:5]:
    print("\n" + "="*60)
    print("Notebook:", os.path.basename(p), "in", os.path.basename(os.path.dirname(p)))
    try:
        with open(p, "r", encoding="utf-8") as f:
            nb = json.load(f)
    except Exception as e:
        print("Error:", e)
        continue
        
    print(f"Total cells: {len(nb.get('cells', []))}")
    for i in range(max(0, len(nb['cells']) - 12), len(nb['cells'])):
        c = nb['cells'][i]
        src = "".join(c.get("source", []))
        print(f"--- Cell {i} ({c.get('cell_type')}) ---")
        print(src[:300] + ("..." if len(src) > 300 else ""))

