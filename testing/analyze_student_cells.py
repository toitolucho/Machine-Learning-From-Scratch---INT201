import json

sub_file = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028\User_134221\PrimerParcial_Parte1_Estructuras_de_Datos.ipynb.txt"
with open(sub_file, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for idx, c in enumerate(nb['cells']):
    src = "".join(c.get("source", []))
    lines = [l.strip() for l in src.split("\n") if l.strip()]
    if c['cell_type'] == 'markdown':
        for l in lines:
            if any(l.startswith(prefix) for prefix in ["#", "##", "**Ejercicio", "**Exercise", "**Pregunta", "**Question"]):
                print(f"Cell {idx} [MD]: {l[:80]}")
    elif c['cell_type'] == 'code':
        has_question_marks = "???" in src
        has_completa = "Completa" in src or "complete" in src.lower()
        has_output = len(c.get("outputs", [])) > 0
        if has_completa or has_question_marks:
            print(f"Cell {idx} [CODE-TASK]: ??? present={has_question_marks}, outputs={has_output}, first line: {lines[0] if lines else 'empty'}")
