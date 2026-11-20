import json
import os

sol_path = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\Avanzado\Practicas Notebooks Guiados\Primer Parcial\02-2026\Practica_01_Parte1_Estructuras_de_Datos_SOLUCIONES_ES.ipynb"
with open(sol_path, "r", encoding="utf-8") as f:
    sol_nb = json.load(f)

print(f"Solution notebook cells: {len(sol_nb['cells'])}")
task_cells = []
for idx, c in enumerate(sol_nb['cells']):
    src = "".join(c.get("source", []))
    if c['cell_type'] == 'code' and ("Completa este" in src or "all_names" in src or "characters" in src):
        # find preceding markdown header
        header = ""
        for prev in range(idx-1, -1, -1):
            if sol_nb['cells'][prev]['cell_type'] == 'markdown':
                header = "".join(sol_nb['cells'][prev].get('source', []))
                break
        task_cells.append((idx, header.split('\n')[0], src[:100].replace('\n', ' ')))

print(f"Found {len(task_cells)} candidate task cells:")
for idx, h, s in task_cells:
    print(f"  Cell {idx}: {h[:50]} | {s[:50]}")
