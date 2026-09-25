import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('MOODLE_TOKEN')
MOODLE_DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
ENDPOINT = f'{MOODLE_DOMAIN}/webservice/rest/server.php'

def call_moodle(function, params=None):
    if params is None:
        params = {}
    params.update({
        'wstoken': TOKEN,
        'wsfunction': function,
        'moodlewsrestformat': 'json'
    })
    response = requests.post(ENDPOINT, data=params)
    return response.json()

def main():
    course_id = 4837
    section_id = 83635
    print(f"Fetching contents for course {course_id}...")
    contents = call_moodle('core_course_get_contents', {'courseid': course_id})
    if not isinstance(contents, list):
        print("Error fetching contents:", contents)
        return
    
    target_sec = None
    for sec in contents:
        if sec.get('id') == section_id:
            target_sec = sec
            break
            
    if not target_sec:
        print(f"Section {section_id} not found!")
        return

    print(f"Found section: {target_sec.get('name')} (id: {target_sec.get('id')})")
    modules = target_sec.get('modules', [])
    print(f"Total modules: {len(modules)}")
    for i, mod in enumerate(modules, 1):
        print(f"{i:02d}. cmid={mod.get('id')} instance={mod.get('instance')} modname={mod.get('modname')} name={mod.get('name')}")

if __name__ == "__main__":
    main()
