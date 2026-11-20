import os
import json

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = sorted(os.listdir(sub_dir))

for uf in user_folders:
    uf_path = os.path.join(sub_dir, uf)
    files = [f for f in os.listdir(uf_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
    if not files:
        continue
    fpath = os.path.join(uf_path, files[0])
    with open(fpath, "r", encoding="utf-8") as fp:
        nb = json.load(fp)
    
    # check if any markdown cell has 'Respuesta' or student text
    answered_md = []
    for idx, c in enumerate(nb.get("cells", [])):
        if c.get("cell_type") == "markdown":
            src = "".join(c.get("source", []))
            if "Pregunta L" in src:
                # check if student added answers below the question
                # by seeing if lines after c) exist or if there's custom text
                lines = src.split("\n")
                # find if there's text after the question prompts
                if any(k in src.lower() for k in ["r:", "rta:", "respuesta:", "a)", "b)", "c)"]):
                    # let's see how long src is compared to original
                    pass
    # Let's check cell count and basic stats
    print(f"{uf}: total cells = {len(nb.get('cells', []))}")
