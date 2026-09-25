import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('MOODLE_TOKEN')
MOODLE_DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
ENDPOINT = f'{MOODLE_DOMAIN}/webservice/rest/server.php'

r = requests.post(ENDPOINT, data={
    'wstoken': TOKEN,
    'wsfunction': 'core_course_get_contents',
    'moodlewsrestformat': 'json',
    'courseid': 4837
})
contents = r.json()
sec = next(s for s in contents if s['id'] == 83635)
modules = sec.get('modules', [])

for i, mod in enumerate(modules, 1):
    name = mod['name']
    has_replacement = '\ufffd' in name
    print(f"{i:02d}. {name!r} {'<-- HAS REPLACEMENT CHAR' if has_replacement else ''}")
