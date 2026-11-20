import os
import json

def check_file(path, label):
    print("=" * 60)
    print(label, ":", path)
    if not os.path.exists(path):
        print("File does not exist!")
        return
    if path.endswith('.ipynb'):
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            nb = json.load(f)
        cells = nb.get('cells', [])
        print(f"Total cells: {len(cells)}")
        for i, c in enumerate(cells[:8]):
            src = "".join(c.get('source', []))
            print(f"Cell {i} ({c.get('cell_type')}): {src[:150]}")
        for i, c in enumerate(cells[-4:], start=max(0, len(cells)-4)):
            src = "".join(c.get('source', []))
            print(f"Cell {i} ({c.get('cell_type')}): {src[:150]}")

p_mayta_1 = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420907_inst_77380\User_199170_Mayta_Baltazar_Edemir\01_Tarea_MaytaBaltazarEdemir.ipynb"
p_mayta_2 = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381\User_199170_Mayta_Baltazar_Edemir\02_Tarea_MaytaBaltazarEdemir.ipynb"
p_clisman = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420907_inst_77380\User_192347_Aguilar_Choque_Clisman\05_Laboratorio_Evaluacion (1).ipynb"

check_file(p_mayta_1, "Mayta T01")
check_file(p_mayta_2, "Mayta T02")
check_file(p_clisman, "Clisman T01")

