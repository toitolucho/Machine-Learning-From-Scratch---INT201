import os
import requests
import re
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('MOODLE_TOKEN')
MOODLE_DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
ENDPOINT = f'{MOODLE_DOMAIN}/webservice/rest/server.php'

def clean_title(name):
    clean = name.strip()
    
    # 1. Prefix with type letter, e.g. "01-02-2026-T-", "10-02-2025-T-", "03-01-2026-T-"
    clean = re.sub(r'^\d{2}-\d{2}-\d{4}-[A-Za-z]{1,3}[-–—\s]+', '', clean)
    
    # 2. Date prefix, e.g. "02-01-2024 Creacion", "05-01-2025 - ", "10-01-2025-"
    clean = re.sub(r'^\d{2}-\d{2}-\d{4}[-–—\s]*', '', clean)
    
    # 3. "Tarea 19 - "
    clean = re.sub(r'^Tarea\s+\d+\s*[-–—]?\s*', '', clean, flags=re.IGNORECASE)
    
    # Clean leading/trailing spaces and dashes
    clean = clean.lstrip('-–— ').rstrip()
    
    return clean

def main():
    course_id = 4837
    section_id = 83635
    
    r = requests.post(ENDPOINT, data={
        'wstoken': TOKEN,
        'wsfunction': 'core_course_get_contents',
        'moodlewsrestformat': 'json',
        'courseid': course_id
    })
    contents = r.json()
    sec = next(s for s in contents if s['id'] == section_id)
    modules = sec.get('modules', [])
    
    table = []
    for i, mod in enumerate(modules, 1):
        cmid = mod['id']
        orig = mod['name']
        title = clean_title(orig)
        prefix = f"{i:02d}-02-2026-T-"
        new_name = f"{prefix}{title}"
        table.append((i, cmid, orig, new_name))
        
    for i, cmid, orig, new_name in table:
        print(f"{i:02d} | cmid={cmid:<7} | {orig}  --->  {new_name}")

if __name__ == "__main__":
    main()
