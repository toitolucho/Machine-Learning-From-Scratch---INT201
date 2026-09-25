import os
import requests
import re
import json
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('MOODLE_TOKEN')
MOODLE_DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
ENDPOINT = f'{MOODLE_DOMAIN}/webservice/rest/server.php'

def get_moodle_session():
    s = requests.Session()
    login_url = f'{MOODLE_DOMAIN}/login/index.php'
    r = s.get(login_url)

    token_m = re.search(r'name="logintoken" value="([^"]+)"', r.text)
    token_val = token_m.group(1) if token_m else None

    login_data = {
        'username': os.environ.get('MOODLE_USERNAME'),
        'password': os.environ.get('MOODLE_PASSWORD')
    }
    if token_val:
        login_data['logintoken'] = token_val

    r_post = s.post(login_url, data=login_data)

    course_url = f'{MOODLE_DOMAIN}/course/view.php?id=4837&sectionid=83635'
    r_course = s.get(course_url)

    sesskey_match = re.search(r'"sesskey":"([^"]+)"', r_course.text) or re.search(r'sesskey=([a-zA-Z0-9]+)', r_course.text)
    sesskey = sesskey_match.group(1) if sesskey_match else None
    
    if not sesskey:
        raise ValueError("Failed to obtain Moodle sesskey after login.")
        
    return s, sesskey

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

def rename_module(session, sesskey, cmid, new_title):
    ajax_url = f'{MOODLE_DOMAIN}/lib/ajax/service.php?sesskey={sesskey}&info=core_update_inplace_editable'
    payload = [
        {
            "index": 0,
            "methodname": "core_update_inplace_editable",
            "args": {
                "component": "core_course",
                "itemtype": "activityname",
                "itemid": int(cmid),
                "value": new_title
            }
        }
    ]
    resp = session.post(ajax_url, json=payload)
    if resp.status_code == 200:
        res_json = resp.json()
        if isinstance(res_json, list) and len(res_json) > 0 and not res_json[0].get('error'):
            return True, res_json[0].get('data', {}).get('value', new_title)
        else:
            return False, f"API Error: {res_json}"
    return False, f"HTTP Error {resp.status_code}: {resp.text}"

def main():
    course_id = 4837
    section_id = 83635
    
    print("=== Moodle Assignment Renaming Workflow ===")
    print("1. Authenticating with Moodle...")
    session, sesskey = get_moodle_session()
    print(f"   Logged in successfully. Sesskey: {sesskey}")
    
    print("\n2. Fetching course section contents...")
    r = requests.post(ENDPOINT, data={
        'wstoken': TOKEN,
        'wsfunction': 'core_course_get_contents',
        'moodlewsrestformat': 'json',
        'courseid': course_id
    })
    contents = r.json()
    sec = next((s for s in contents if s['id'] == section_id), None)
    if not sec:
        print(f"Error: Section {section_id} not found.")
        return
        
    modules = sec.get('modules', [])
    print(f"   Section: {sec['name']} (Found {len(modules)} modules)")
    
    print("\n3. Processing and renaming assignments...")
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, mod in enumerate(modules, 1):
        cmid = mod['id']
        orig_name = mod['name']
        title = clean_title(orig_name)
        new_name = f"{i:02d}-02-2026-T-{title}"
        
        if orig_name == new_name:
            print(f"[{i:02d}/{len(modules)}] ALREADY UP TO DATE: cmid={cmid} -> {new_name}")
            skipped_count += 1
            continue
            
        print(f"[{i:02d}/{len(modules)}] RENAMING: cmid={cmid}")
        print(f"       FROM: {orig_name}")
        print(f"       TO  : {new_name}")
        
        success, res_val = rename_module(session, sesskey, cmid, new_name)
        if success:
            print(f"       [SUCCESS] Updated.")
            updated_count += 1
        else:
            print(f"       [FAILED] {res_val}")
            error_count += 1
            
        time.sleep(0.1) # Brief pause to avoid flooding the server
        
    print("\n=== Renaming Summary ===")
    print(f"Total modules: {len(modules)}")
    print(f"Updated:       {updated_count}")
    print(f"Skipped:       {skipped_count}")
    print(f"Errors:        {error_count}")
    
    print("\n4. Verifying updated course section...")
    r_verif = requests.post(ENDPOINT, data={
        'wstoken': TOKEN,
        'wsfunction': 'core_course_get_contents',
        'moodlewsrestformat': 'json',
        'courseid': course_id
    })
    sec_verif = next(s for s in r_verif.json() if s['id'] == section_id)
    print("Current state in Moodle:")
    for i, mod in enumerate(sec_verif.get('modules', []), 1):
        print(f"{i:02d}. [cmid={mod['id']}] {mod['name']}")

if __name__ == "__main__":
    main()
