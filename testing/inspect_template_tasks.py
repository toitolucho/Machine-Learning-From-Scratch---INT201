import json

tpl_path = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\Avanzado\Practicas Notebooks Guiados\Primer Parcial\02-2026\Practica_01_Parte1_Estructuras_de_Datos_ES.ipynb"
with open(tpl_path, "r", encoding="utf-8") as f:
    tpl_nb = json.load(f)

tasks = []
for idx, c in enumerate(tpl_nb["cells"]):
    src = "".join(c.get("source", []))
    if c["cell_type"] == "code" and ("# Completa este código" in src or "???" in src):
        # find exercise name from previous markdown
        ex_name = f"Cell_{idx}"
        for prev in range(idx-1, -1, -1):
            if tpl_nb["cells"][prev]["cell_type"] == "markdown":
                prev_src = "".join(tpl_nb["cells"][prev].get("source", []))
                for line in prev_src.split("\n"):
                    if "Ejercicio" in line or "Exercise" in line:
                        ex_name = line.strip().replace("#", "").strip()
                        break
                if ex_name != f"Cell_{idx}":
                    break
        tasks.append((idx, ex_name, src))

print(f"Total template tasks: {len(tasks)}")
for idx, name, src in tasks:
    first_lines = [l for l in src.split("\n") if l.strip()][:3]
    print(f"Index {idx:2d} | {name:<45} | {' // '.join(first_lines)}")
