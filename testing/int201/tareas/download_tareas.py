import os
import sys
import requests
import json
from dotenv import load_dotenv

# Reconfigure stdout for Windows console UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Load .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
if not os.path.exists(env_path):
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo').rstrip('/')
TOKEN = os.environ.get('MOODLE_TOKEN')
USERNAME = os.environ.get('MOODLE_USERNAME')
PASSWORD = os.environ.get('MOODLE_PASSWORD')
ENDPOINT = f'{DOMAIN}/webservice/rest/server.php'

COURSE_ID = 6726
CMIDS = [420907, 420908]

def renew_token():
    global TOKEN
    print("Obtaining new token via credentials...")
    token_url = f"{DOMAIN}/login/token.php"
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'service': 'moodle_mobile_app'
    }
    res = requests.post(token_url, data=data)
    res_json = res.json()
    if 'token' in res_json:
        TOKEN = res_json['token']
        print(f"Token obtained successfully: {TOKEN[:6]}...")
        return TOKEN
    else:
        print(f"Error obtaining token: {res_json}")
        return None

def call_moodle(function, params=None):
    global TOKEN
    if params is None:
        params = {}
    data = {
        'wstoken': TOKEN,
        'wsfunction': function,
        'moodlewsrestformat': 'json'
    }
    data.update(params)
    r = requests.post(ENDPOINT, data=data)
    res = r.json()
    if isinstance(res, dict) and res.get('errorcode') in ['invalidtoken', 'accessexception']:
        print(f"Token error ({res.get('message')}), attempting renewal...")
        if renew_token():
            data['wstoken'] = TOKEN
            r = requests.post(ENDPOINT, data=data)
            return r.json()
    return res

def main():
    print("=" * 60)
    print("Connecting to eCampus Moodle API...")
    print(f"Domain: {DOMAIN}")
    site_info = call_moodle('core_webservice_get_site_info')
    if not site_info or 'exception' in site_info:
        print(f"Failed to connect. Response: {site_info}")
        if renew_token():
            site_info = call_moodle('core_webservice_get_site_info')
    
    print(f"Logged in as: {site_info.get('fullname')} (ID: {site_info.get('userid')})")
    
    # Get enrolled users in course
    print(f"\nFetching enrolled students for course {COURSE_ID}...")
    enrolled = call_moodle('core_enrol_get_enrolled_users', {'courseid': COURSE_ID})
    user_map = {}
    if isinstance(enrolled, list):
        for u in enrolled:
            user_map[u['id']] = u
        print(f"Found {len(user_map)} enrolled users.")
    else:
        print("Warning: Could not fetch enrolled users:", enrolled)
        
    # Get course contents to find assignment details
    print(f"\nSearching for modules {CMIDS} in course {COURSE_ID}...")
    contents = call_moodle('core_course_get_contents', {'courseid': COURSE_ID})
    
    target_modules = {}
    if isinstance(contents, list):
        for sec in contents:
            for mod in sec.get('modules', []):
                if mod.get('id') in CMIDS:
                    target_modules[mod['id']] = mod
                    print(f"Found CMID {mod['id']}: Instance={mod.get('instance')}, Name='{mod.get('name')}', ModName='{mod.get('modname')}'")
    
    # Process each assignment
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    for cmid in CMIDS:
        mod = target_modules.get(cmid)
        if not mod:
            print(f"\nError: Module {cmid} not found in course content.")
            continue
            
        instance_id = mod.get('instance')
        assign_name = mod.get('name')
        folder_name = f"tarea_{cmid}_inst_{instance_id}"
        target_dir = os.path.join(script_dir, folder_name)
        os.makedirs(target_dir, exist_ok=True)
        
        print("\n" + "=" * 60)
        print(f"Processing: '{assign_name}' (CMID: {cmid}, Instance: {instance_id})")
        print(f"Target directory: {target_dir}")
        
        # Save module info
        with open(os.path.join(target_dir, "module_info.json"), "w", encoding="utf-8") as f:
            json.dump(mod, f, indent=2, ensure_ascii=False)
            
        # Get assignment details via mod_assign_get_assignments
        assign_details = call_moodle('mod_assign_get_assignments', {'courseids[0]': COURSE_ID})
        assign_info = None
        if assign_details and 'courses' in assign_details:
            for c in assign_details['courses']:
                for a in c.get('assignments', []):
                    if a.get('id') == instance_id:
                        assign_info = a
                        with open(os.path.join(target_dir, "assignment_details.json"), "w", encoding="utf-8") as f:
                            json.dump(a, f, indent=2, ensure_ascii=False)
                        print(f"Assignment Intro/Description:")
                        print(f"  Intro: {a.get('intro')[:200] if a.get('intro') else 'None'}...")
                        print(f"  Due date: {a.get('duedate')}, Cutoff: {a.get('cutoffdate')}")
                        break
        
        # Get submissions
        print(f"\nFetching submissions for instance {instance_id}...")
        subs_data = call_moodle('mod_assign_get_submissions', {'assignmentids[0]': instance_id})
        
        with open(os.path.join(target_dir, "submissions_raw.json"), "w", encoding="utf-8") as f:
            json.dump(subs_data, f, indent=2, ensure_ascii=False)
            
        if not subs_data or 'assignments' not in subs_data or not subs_data['assignments']:
            print("No submissions found or error:", subs_data)
            continue
            
        submissions = subs_data['assignments'][0]['submissions']
        print(f"Total submission records: {len(submissions)}")
        
        submitted_count = 0
        downloaded_count = 0
        text_submission_count = 0
        
        submissions_summary = []
        
        for sub in submissions:
            uid = sub['userid']
            u = user_map.get(uid, {})
            fullname = u.get('fullname', f"User_{uid}")
            email = u.get('email', '')
            status = sub.get('status')
            
            sub_info = {
                'userid': uid,
                'fullname': fullname,
                'email': email,
                'status': status,
                'timecreated': sub.get('timecreated'),
                'timemodified': sub.get('timemodified'),
                'files': [],
                'onlinetext': []
            }
            
            if status == 'submitted' or sub.get('plugins'):
                submitted_count += 1
                user_folder = os.path.join(target_dir, f"User_{uid}_{fullname.replace(' ', '_')}")
                
                for plugin in sub.get('plugins', []):
                    ptype = plugin.get('type')
                    # File submissions
                    if ptype == 'file':
                        for fa in plugin.get('fileareas', []):
                            for fi in fa.get('files', []):
                                f_url = fi.get('fileurl')
                                f_name = fi.get('filename')
                                if not f_url or not f_name:
                                    continue
                                os.makedirs(user_folder, exist_ok=True)
                                dest_file = os.path.join(user_folder, f_name)
                                sub_info['files'].append({
                                    'filename': f_name,
                                    'filesize': fi.get('filesize'),
                                    'path': dest_file,
                                    'url': f_url
                                })
                                
                                dl_url = f"{f_url}&token={TOKEN}" if '?' in f_url else f"{f_url}?token={TOKEN}"
                                try:
                                    r = requests.get(dl_url, timeout=30)
                                    with open(dest_file, "wb") as fp:
                                        fp.write(r.content)
                                    downloaded_count += 1
                                    print(f"  [FILE] Downloaded for {fullname}: {f_name}")
                                except Exception as ex:
                                    print(f"  [ERROR] Failed to download {f_name} for {fullname}: {ex}")
                                    
                    # Online text submissions (e.g. Google Colab links or answers)
                    elif ptype == 'onlinetext':
                        for field in plugin.get('editorfields', []):
                            text = field.get('text', '')
                            if text:
                                os.makedirs(user_folder, exist_ok=True)
                                text_file = os.path.join(user_folder, "onlinetext.html")
                                with open(text_file, "w", encoding="utf-8") as fp:
                                    fp.write(text)
                                sub_info['onlinetext'].append(text)
                                text_submission_count += 1
                                print(f"  [TEXT] Saved online text for {fullname}")
                                
            submissions_summary.append(sub_info)
            
        with open(os.path.join(target_dir, "submissions_summary.json"), "w", encoding="utf-8") as f:
            json.dump(submissions_summary, f, indent=2, ensure_ascii=False)
            
        print(f"\nAssignment {cmid} Summary:")
        print(f"  Submitted: {submitted_count}")
        print(f"  Downloaded files: {downloaded_count}")
        print(f"  Online texts: {text_submission_count}")

if __name__ == "__main__":
    main()

