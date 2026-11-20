import json
import os

paths = [
    (141808, r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381\User_141808_Condori_Berdeja_Juan_Jose\Módulo_4_Aprendizaje_Automático_(Machine_Learning).ipynb"),
    (203220, r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381\User_203220_Bravo_Lopez_Mauricio_Aniceto\05_Comparacion_Clasificadores (1).ipynb"),
    (208954, r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381\User_208954_Aguilar_Choque_Herlan\05_Comparacion_Clasificadores (2) (1).ipynb"),
    (210608, r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381\User_210608_Zelaya_Chavarria_Rodrigo_Florindo\05_Comparacion_Clasificadores_TAREA.ipynb")
]

for uid, p in paths:
    print("=" * 60)
    print(f"UID {uid}: {os.path.basename(p)}")
    with open(p, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"Total cells: {len(nb['cells'])}")
    for i in range(max(0, len(nb['cells']) - 8), len(nb['cells'])):
        c = nb['cells'][i]
        src = "".join(c.get('source', []))
        print(f"Cell {i} ({c.get('cell_type')}): {src[:200]}...\n")

