import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
TOKEN = os.environ.get('MOODLE_TOKEN')
ENDPOINT = f'{DOMAIN}/webservice/rest/server.php'

def call(fn, params={}):
    p = {'wstoken': TOKEN, 'wsfunction': fn, 'moodlewsrestformat': 'json'}
    p.update(params)
    r = requests.post(ENDPOINT, data=p)
    return r.json()

users = call('core_enrol_get_enrolled_users', {'courseid': 6582})
user_map = {u['id']: u for u in users}

sub_dir = r"d:\Documents\USFX\INT210\Machine-Learning-From-Scratch---INT210\testing\submissions_77028"
for uf in sorted(os.listdir(sub_dir)):
    uid = int(uf.replace('User_', ''))
    u = user_map.get(uid, {})
    fullname = u.get("fullname", "N/A")
    email = u.get("email", "N/A")
    print(f"{uid:8d} | {fullname:<35} | {email}")
