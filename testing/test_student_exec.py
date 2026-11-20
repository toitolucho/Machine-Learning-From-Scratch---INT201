import os
import json
import traceback

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"

# Let's test on User_178796 (who completed all cells)
user_path = os.path.join(sub_dir, "User_178796")
fnames = [f for f in os.listdir(user_path) if f.endswith(('.ipynb', '.ipynb.txt', '.txt', '.json'))]
nb_file = os.path.join(user_path, fnames[0])

with open(nb_file, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Testing execution for {user_path}")
global_env = {}

success_cells = 0
error_cells = 0

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = "".join(cell.get('source', []))
        if not src.strip():
            continue
        try:
            exec(src, global_env)
            success_cells += 1
        except Exception as e:
            error_cells += 1
            print(f"  Cell {i} Error: {type(e).__name__}: {e}")

print(f"Execution complete. Success: {success_cells}, Errors: {error_cells}")
print("Checking key variables in global_env:")
for k in ["characters_raw", "characters", "all_names", "brightness_records", "production_lookup", "role_corrections"]:
    if k in global_env:
        print(f"  {k}: found, type={type(global_env[k])}, len={len(global_env[k]) if hasattr(global_env[k], '__len__') else 'N/A'}")
    else:
        print(f"  {k}: NOT FOUND")
