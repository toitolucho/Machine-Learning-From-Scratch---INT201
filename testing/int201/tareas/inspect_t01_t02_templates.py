import json
import os
import glob

def find_file(base_dir, pattern):
    files = glob.glob(os.path.join(base_dir, "**", pattern), recursive=True)
    return files[0] if files else None

t01_base = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420907_inst_77380"
t02_base = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381"

nb1_path = find_file(t01_base, "*Laboratorio_Evaluacion*.ipynb")
print(f"Loading T01 notebook: {nb1_path}")
with open(nb1_path, "r", encoding="utf-8") as f:
    nb1 = json.load(f)

print("\n" + "="*30 + " T01 CELLS " + "="*30)
for i, c in enumerate(nb1["cells"]):
    print(f"\n--- [T01 Cell {i}] ({c['cell_type']}) ---")
    print("".join(c["source"]))

nb2_path = find_file(t02_base, "*05_Comparacion_Clasificadores*.ipynb")
print(f"\nLoading T02 notebook: {nb2_path}")
with open(nb2_path, "r", encoding="utf-8") as f:
    nb2 = json.load(f)

print("\n" + "="*30 + " T02 CELLS " + "="*30)
for i, c in enumerate(nb2["cells"]):
    print(f"\n--- [T02 Cell {i}] ({c['cell_type']}) ---")
    print("".join(c["source"]))
