import os
import requests
import re
import json
from dotenv import load_dotenv

load_dotenv()

s = requests.Session()
login_url = 'https://ecampus.usfx.bo/login/index.php'
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

course_url = 'https://ecampus.usfx.bo/course/view.php?id=4837&sectionid=83635'
r_course = s.get(course_url)

sesskey_match = re.search(r'"sesskey":"([^"]+)"', r_course.text) or re.search(r'sesskey=([a-zA-Z0-9]+)', r_course.text)
sesskey = sesskey_match.group(1) if sesskey_match else None
print('Sesskey found:', sesskey)

# Test updating item 1 (cmid=416831) to its exact current title:
# "01-02-2026-T-Distribucion Monkey forma Piramide 4x4"
ajax_url = f'https://ecampus.usfx.bo/lib/ajax/service.php?sesskey={sesskey}&info=core_update_inplace_editable'
payload = [
    {
        "index": 0,
        "methodname": "core_update_inplace_editable",
        "args": {
            "component": "core_course",
            "itemtype": "activityname",
            "itemid": 416831,
            "value": "01-02-2026-T-Distribucion Monkey forma Piramide 4x4"
        }
    }
]

res = s.post(ajax_url, json=payload)
print('AJAX status:', res.status_code)
print('AJAX response:', res.text)
