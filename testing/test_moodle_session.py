import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

s = requests.Session()
login_url = 'https://ecampus.usfx.bo/login/index.php'
r = s.get(login_url)

token_m = re.search(r'name="logintoken" value="([^"]+)"', r.text)
token_val = token_m.group(1) if token_m else None
print('Found login token:', token_val)

login_data = {
    'username': os.environ.get('MOODLE_USERNAME'),
    'password': os.environ.get('MOODLE_PASSWORD')
}
if token_val:
    login_data['logintoken'] = token_val

r_post = s.post(login_url, data=login_data)
print('Logged in url:', r_post.url)

course_url = 'https://ecampus.usfx.bo/course/view.php?id=4837&sectionid=83635'
r_course = s.get(course_url)
print('Course page status:', r_course.status_code)

sesskey_match = re.search(r'"sesskey":"([^"]+)"', r_course.text) or re.search(r'sesskey=([a-zA-Z0-9]+)', r_course.text)
sesskey = sesskey_match.group(1) if sesskey_match else None
print('Sesskey found:', sesskey)
