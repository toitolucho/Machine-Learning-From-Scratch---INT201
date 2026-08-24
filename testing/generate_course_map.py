import os
import json
import glob

# Constants
REPO_PATH = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210"
GITHUB_REPO_URL = "https://github.com/toitolucho/Machine-Learning-From-Scratch---INT201/blob/main"
COLAB_BASE_URL = "https://colab.research.google.com/github/toitolucho/Machine-Learning-From-Scratch---INT201/blob/main"

def get_chapter_info(week_num):
    if week_num <= 2:
        return 1, "Bloque 1: Fundamentos y Flujo de Trabajo"
    elif week_num <= 4:
        return 2, "Bloque 2: Preprocesamiento y Limpieza de Datos"
    elif week_num <= 7:
        return 3, "Bloque 3: Modelos Supervisados - Clasificación"
    elif week_num <= 10:
        return 4, "Bloque 4: Modelos Supervisados - Regresión y Regularización"
    elif week_num <= 13:
        return 5, "Bloque 5: Modelos No Supervisados y Reducción de Dimensiones"
    elif week_num <= 16:
        return 6, "Bloque 6: Deep Learning y Redes Neuronales"
    else:
        return 7, "Bloque 7: Evaluación Final, Overfitting e Interpretabilidad"

def generate_map():
    chapters = {}
    
    # Find all Semana_XX directories
    weeks = sorted([d for d in os.listdir(REPO_PATH) if d.startswith("Semana_") and os.path.isdir(os.path.join(REPO_PATH, d))])
    
    for week in weeks:
        week_num = int(week.split("_")[1])
        chapter_id, chapter_title = get_chapter_info(week_num)
        
        if chapter_id not in chapters:
            chapters[chapter_id] = {
                "chapter_id": chapter_id,
                "title": chapter_title,
                "weeks": []
            }
            
        week_path = os.path.join(REPO_PATH, week)
        files = sorted(os.listdir(week_path))
        
        resources = []
        for file in files:
            if file == "README.md" or file == "generar_graficas.py" or file.endswith(".png") or file.endswith(".md"):
                continue # Skip internal readme/scripts/images/md
                
            file_path = os.path.join(week_path, file)
            if not os.path.isfile(file_path):
                continue
                
            title = file.replace("_", " ").rsplit(".", 1)[0]
            
            # Determine type and URL
            if file.endswith(".ipynb"):
                url = f"{COLAB_BASE_URL}/{week}/{file}"
                # If it's a Tarea or Laboratorio, it should be an assignment
                if "Tarea" in file or "Laboratorio" in file:
                    res_type = "Assignment"
                    description = f"<p>Por favor completa el cuaderno de Jupyter: <a href='{url}' target='_blank'>{title}</a> en Google Colab.</p>"
                else:
                    res_type = "URL"
                    description = f"<p>Material guiado: <a href='{url}' target='_blank'>{title}</a></p>"
            else:
                url = f"{GITHUB_REPO_URL}/{week}/{file}"
                res_type = "URL"
                description = f"<p>Recurso del curso: <a href='{url}' target='_blank'>{title}</a></p>"
                
            resources.append({
                "type": res_type,
                "title": title,
                "description": description,
                "url": url,
                "filename": file
            })
            
        chapters[chapter_id]["weeks"].append({
            "week": week,
            "title": week.replace("_", " "),
            "resources": resources
        })
        
    # Convert dict to list sorted by chapter_id
    course_structure = [chapters[k] for k in sorted(chapters.keys())]
    
    output_path = os.path.join(REPO_PATH, "testing", "course_structure.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(course_structure, f, indent=4, ensure_ascii=False)
        
    print(f"Course map generated successfully at {output_path}")

if __name__ == "__main__":
    generate_map()
