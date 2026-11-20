import os
import sys
import requests
import json
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

load_dotenv()

# ================= CONFIGURATION =================
# 1. Paste your key from "Claves de seguridad" here
# TOKEN = '179539aa8205ed0a428a0977cf6ea032' --usfx

TOKEN = os.environ.get('MOODLE_TOKEN')

#TOKEN = '7a2e06de3d20b346658ba9e75a919e34'  # postgrado

# 2. Configuration based on your links
MOODLE_DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
#MOODLE_DOMAIN = 'https://aulasvirtuales.usfx.bo/tecnologia'
COURSE_ID = 6582          # From your course link
CM_ID_FROM_URL = 419643   # From your assignment link (view.php?id=XXXX)
DOWNLOAD_FILES = True     # Set to True to download submission files

# ================= THE SCRIPT =================
ENDPOINT = f'{MOODLE_DOMAIN}/webservice/rest/server.php'

def call_moodle(function, params={}):
    """Helper to send requests to Moodle"""
    params.update({
        'wstoken': TOKEN,
        'wsfunction': function,
        'moodlewsrestformat': 'json'
    })
    try:
        response = requests.post(ENDPOINT, data=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def main():
    print("--- 🕵️‍♂️ MOODLE API DIAGNOSTIC ---")

    # STEP 1: Test the Token
    print(f"\n1. Testing Token on {MOODLE_DOMAIN}...")
    user_info = call_moodle('core_webservice_get_site_info')
    
    if not user_info or 'exception' in user_info:
        print("❌ Failed. The token might be invalid or lacks permissions.")
        if user_info: print(f"   Moodle says: {user_info.get('message')}")
        return

    print(f"✅ Success! Logged in as: {user_info.get('fullname')} (User ID: {user_info.get('userid')})")

    # STEP 2: Find the Real Assignment ID
    # The ID in the URL (401975) is the "Course Module ID". 
    # The API needs the "Instance ID". We have to find it.
    print(f"\n2. Searching for Assignment details in Course {COURSE_ID}...")
    course_content = call_moodle('core_course_get_contents', {'courseid': COURSE_ID})
    
    real_assign_id = None
    assign_name = None
    mod_type = None

    if course_content and 'exception' not in course_content:
        # Loop through all sections and modules to find our assignment
        for section in course_content:
            for module in section.get('modules', []):
                if module.get('id') == CM_ID_FROM_URL:
                    real_assign_id = module.get('instance')
                    assign_name = module.get('name')
                    mod_type = module.get('modname')
                    print(f"✅ Found it! Module '{assign_name}' (Type: {mod_type})")
                    print(f"   - URL ID (CMID): {CM_ID_FROM_URL}")
                    print(f"   - Real DB ID (Instance): {real_assign_id}")
                    break
            if real_assign_id: break
    
    if not real_assign_id:
        print("❌ Could not find the module in the course content. Check the IDs.")
        if course_content and 'exception' in course_content:
            print(f"   Error: {course_content.get('message')}")
        return

    if mod_type != 'assign':
        print(f"\n⚠️ WARNING: Module '{assign_name}' is of type '{mod_type}' (Quiz / Cuestionario), NOT 'assign' (Tarea)!")
        print("   The function 'mod_assign_get_submissions' only works for Assignment activities.")
        # Check if there is an assignment with matching or similar name
        assign_alternatives = []
        for section in course_content:
            for module in section.get('modules', []):
                if module.get('modname') == 'assign' and (
                    assign_name.strip().lower() in module.get('name', '').strip().lower() or
                    module.get('name', '').strip().lower() in assign_name.strip().lower()
                ):
                    assign_alternatives.append((module.get('id'), module.get('instance'), module.get('name')))
        if assign_alternatives:
            print(f"\n   💡 Did you mean the Assignment counterpart?")
            for cmid, inst, name in assign_alternatives:
                print(f"      - CM_ID_FROM_URL = {cmid} (Instance: {inst}) -> '{name}'")
        return

    # STEP 3: Try to Fetch Submissions
    print(f"\n3. Testing permission to read submissions for '{assign_name}'...")
    submissions_data = call_moodle('mod_assign_get_submissions', {'assignmentids[0]': real_assign_id})

    if submissions_data and submissions_data.get('assignments'):
        submissions = submissions_data['assignments'][0]['submissions']
        count = len(submissions)
        print(f"✅ SUCCESS! Access granted.")
        print(f"   Found {count} submissions for this assignment.")
        
        if count > 0:
            print("   First student submission status:", submissions[0].get('status'))
            
            # STEP 4: Download Submissions
            if DOWNLOAD_FILES:
                output_dir = os.path.join(os.path.dirname(__file__), f"submissions_{real_assign_id}")
                os.makedirs(output_dir, exist_ok=True)
                print(f"\n4. Downloading submission files to: {output_dir}")
                downloaded = 0
                
                for sub in submissions:
                    user_id = sub['userid']
                    for plugin in sub.get('plugins', []):
                        if plugin.get('type') == 'file':
                            for fa in plugin.get('fileareas', []):
                                for file_info in fa.get('files', []):
                                    file_url = file_info.get('fileurl')
                                    filename = file_info.get('filename')
                                    if not file_url or not filename:
                                        continue
                                    
                                    user_dir = os.path.join(output_dir, f"User_{user_id}")
                                    os.makedirs(user_dir, exist_ok=True)
                                    dest_path = os.path.join(user_dir, filename)
                                    
                                    if not os.path.exists(dest_path):
                                        dl_url = f"{file_url}&token={TOKEN}" if '?' in file_url else f"{file_url}?token={TOKEN}"
                                        r = requests.get(dl_url)
                                        with open(dest_path, "wb") as f:
                                            f.write(r.content)
                                        downloaded += 1
                                        print(f"   📥 Downloaded: User_{user_id}/{filename}")
                                    else:
                                        print(f"   ⏩ Already exists: User_{user_id}/{filename}")
                                        
                print(f"\n✅ All set! Downloaded {downloaded} new submission files.")
    else:
        print("❌ Failed to fetch submissions.")
        if submissions_data:
            if submissions_data.get('warnings'):
                print(f"   Moodle warnings: {submissions_data.get('warnings')}")
            if submissions_data.get('message'):
                print(f"   Moodle says: {submissions_data.get('message')}")
        print("   (This usually means the Token exists but doesn't have 'Teacher' rights or the specific capability)")

if __name__ == "__main__":
    main()