import os
import sys
import json
import zipfile

# Configure stdout
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
t01_dir = os.path.join(script_dir, "tarea_420907_inst_77380")
t02_dir = os.path.join(script_dir, "tarea_420908_inst_77381")

def inspect_folder(folder_path, label):
    print("=" * 70)
    print(f"INSPECTING {label}: {folder_path}")
    print("=" * 70)
    
    # Unpack any zip files first if any
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.endswith('.zip'):
                zpath = os.path.join(root, f)
                extract_to = os.path.join(root, "unzipped_" + os.path.splitext(f)[0])
                if not os.path.exists(extract_to):
                    try:
                        with zipfile.ZipFile(zpath, 'r') as zf:
                            zf.extractall(extract_to)
                        print(f"Extracted zip: {f} to {extract_to}")
                    except Exception as e:
                        print(f"Failed to extract {f}: {e}")

    # Find a clean .ipynb to see the assignment instructions
    sample_notebooks = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.endswith('.ipynb'):
                sample_notebooks.append(os.path.join(root, f))
                
    print(f"Found {len(sample_notebooks)} notebooks in {label}.")
    
    if not sample_notebooks:
        return
        
    # Let's inspect the first 3 notebooks to find section headers and instructions
    for sample_nb_path in sample_notebooks[:3]:
        print("\n" + "-" * 50)
        print(f"Sample Notebook: {os.path.basename(sample_nb_path)}")
        try:
            with open(sample_nb_path, "r", encoding="utf-8", errors="replace") as fp:
                nb = json.load(fp)
        except Exception as e:
            print(f"Error loading {sample_nb_path}: {e}")
            continue
            
        cells = nb.get("cells", [])
        print(f"Total cells: {len(cells)}")
        
        md_headers = []
        code_snippets = []
        
        for idx, cell in enumerate(cells):
            cell_type = cell.get("cell_type")
            source = "".join(cell.get("source", []))
            if cell_type == "markdown":
                for line in source.split("\n"):
                    line_s = line.strip()
                    if line_s.startswith("#") or "ejercicio" in line_s.lower() or "tarea" in line_s.lower() or "instruccion" in line_s.lower() or "evaluac" in line_s.lower() or "parte" in line_s.lower() or "objetivo" in line_s.lower():
                        md_headers.append(f"Cell {idx}: {line_s[:100]}")
            elif cell_type == "code":
                lines = [l.strip() for l in source.split("\n") if l.strip()]
                # check if comment has task description
                for l in lines:
                    if l.startswith("#") and any(k in l.lower() for k in ["ejercicio", "tarea", "completar", "todo", "paso", "instruccion", "tu codigo"]):
                        code_snippets.append(f"Cell {idx}: {l[:100]}")
                        
        print("\nMarkdown headers / tasks found:")
        for h in md_headers[:25]:
            print("  ", h)
            
        print("\nCode comments / TODOs found:")
        for c in code_snippets[:20]:
            print("  ", c)

if __name__ == "__main__":
    inspect_folder(t01_dir, "T01 (CMID 420907)")
    inspect_folder(t02_dir, "T02 (CMID 420908)")

