import json
import os

paths = [
    r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420907_inst_77380\User_141808_Condori_Berdeja_Juan_Jose\Laboratorio_Evaluado_WBCD_y_Evaluación_Multimodelo.ipynb",
    r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420908_inst_77381\User_193316_Casillas_Carasani_Brayan\02_Laboratorio_Evaluacion (1).ipynb",
    r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420907_inst_77380\User_201054_Arancibia_Leon_Diego_Esteban\02_Laboratorio_Evaluacion (1).ipynb",
    r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\int201\tareas\tarea_420907_inst_77380\User_207738_Nuñez_Del_Prado_Choque_Abril\02_Laboratorio_Evaluacion_abrilnuñezdelpradoo.ipynb"
]

for p in paths:
    print("=" * 60)
    print("File:", os.path.basename(p))
    with open(p, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for i, c in enumerate(nb['cells']):
        src = "".join(c.get('source', []))
        if any(k in src.lower() for k in ["map", "replace", "diagnosis", "iloc", "preprocesamiento", "target", "train_test_split", "scaler"]):
            print(f"Cell {i} ({c['cell_type']}):\n{src[:300]}\n")

