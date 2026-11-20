import os, json

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
for uf in sorted(os.listdir(sub_dir)):
    p = os.path.join(sub_dir, uf)
    f = [x for x in os.listdir(p) if x.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))][0]
    with open(os.path.join(p, f), 'r', encoding='utf-8') as fp:
        nb = json.load(fp)
    print(f"{uf}: {len(nb.get('cells', []))} cells, filename: {f}")
