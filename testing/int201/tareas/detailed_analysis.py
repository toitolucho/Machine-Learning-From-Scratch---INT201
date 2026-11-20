import os
import sys
import json
import glob
import re

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
t01_dir = os.path.join(script_dir, "tarea_420907_inst_77380")
t02_dir = os.path.join(script_dir, "tarea_420908_inst_77381")

def get_notebook_or_code(folder):
    """Finds all code/notebook files in a folder, including unzipped ones."""
    items = []
    for r, d, fs in os.walk(folder):
        for f in fs:
            if f.endswith('.ipynb') or f.endswith('.py'):
                items.append(os.path.join(r, f))
    return items

def read_code_and_md(filepath):
    code_cells = []
    md_cells = []
    if filepath.endswith('.ipynb'):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as fp:
                nb = json.load(fp)
            for c in nb.get('cells', []):
                ctype = c.get('cell_type')
                src = "".join(c.get('source', []))
                if ctype == 'code':
                    code_cells.append(src)
                elif ctype == 'markdown':
                    md_cells.append(src)
        except Exception as e:
            code_cells.append(f"# Error reading: {e}")
    elif filepath.endswith('.py'):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as fp:
                content = fp.read()
            code_cells.append(content)
            # Check docstrings for markdown-like text
            docstrings = re.findall(r'"""(.*?)"""', content, re.DOTALL)
            md_cells.extend(docstrings)
        except Exception as e:
            code_cells.append(f"# Error reading: {e}")
    return code_cells, md_cells

print("Analyzing all submissions...")
# Let's list all students in Course 6726
with open(os.path.join(t01_dir, "submissions_summary.json"), 'r', encoding='utf-8') as f:
    t01_summary = json.load(f)
with open(os.path.join(t02_dir, "submissions_summary.json"), 'r', encoding='utf-8') as f:
    t02_summary = json.load(f)

t01_by_user = {s['userid']: s for s in t01_summary}
t02_by_user = {s['userid']: s for s in t02_summary}

all_uids = sorted(list(set(list(t01_by_user.keys()) + list(t02_by_user.keys()))))

print(f"Total unique users across both summaries: {len(all_uids)}")

overview = []
for uid in all_uids:
    u1 = t01_by_user.get(uid, {})
    u2 = t02_by_user.get(uid, {})
    name = u1.get('fullname') or u2.get('fullname')
    
    # Check folder contents
    f1_dir = os.path.join(t01_dir, f"User_{uid}_{name.replace(' ', '_')}")
    f2_dir = os.path.join(t02_dir, f"User_{uid}_{name.replace(' ', '_')}")
    
    files1 = get_notebook_or_code(f1_dir) if os.path.exists(f1_dir) else []
    files2 = get_notebook_or_code(f2_dir) if os.path.exists(f2_dir) else []
    
    overview.append({
        'uid': uid,
        'name': name,
        't01_status': u1.get('status', 'not_enrolled'),
        't02_status': u2.get('status', 'not_enrolled'),
        't01_files': [os.path.basename(x) for x in files1],
        't02_files': [os.path.basename(x) for x in files2],
        't01_paths': files1,
        't02_paths': files2
    })

print(f"\n{'UID':<8} | {'Student':<35} | {'T01 Status':<12} | {'T02 Status':<12} | {'T01 Files':<30} | {'T02 Files':<30}")
print("-" * 135)
for o in overview:
    t1_f = ", ".join(o['t01_files']) if o['t01_files'] else "NONE"
    t2_f = ", ".join(o['t02_files']) if o['t02_files'] else "NONE"
    print(f"{o['uid']:<8} | {o['name']:<35} | {o['t01_status']:<12} | {o['t02_status']:<12} | {t1_f[:28]:<30} | {t2_f[:28]:<30}")

