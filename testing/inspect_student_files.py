import os
import json
import glob

# Check submissions directory
sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
user_folders = os.listdir(sub_dir)
print(f"Found {len(user_folders)} user folders in {sub_dir}")

for uf in user_folders[:3]:
    uf_path = os.path.join(sub_dir, uf)
    files = os.listdir(uf_path)
    print(f"  {uf}: {files}")
    for f in files:
        fpath = os.path.join(uf_path, f)
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            print(f"    -> Valid JSON notebook! Total cells: {len(data.get('cells', []))}")
            # print cell types
            code_cells = [c for c in data.get('cells', []) if c.get('cell_type') == 'code']
            print(f"    -> Code cells: {len(code_cells)}")
        except Exception as e:
            print(f"    -> Error reading as JSON: {e}")
