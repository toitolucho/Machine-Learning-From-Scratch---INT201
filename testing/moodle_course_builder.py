import os
import json
import time
import getpass
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

MOODLE_DOMAIN = os.environ.get('MOODLE_DOMAIN', 'https://ecampus.usfx.bo')
LOGIN_URL = f'{MOODLE_DOMAIN}/login/index.php'
COURSE_ID = 6726

def get_credentials():
    username = os.environ.get('MOODLE_USERNAME')
    password = os.environ.get('MOODLE_PASSWORD')
    
    if not username:
        username = input("Enter your Moodle Username: ")
    if not password:
        password = getpass.getpass("Enter your Moodle Password: ")
        
    return username, password

def fill_atto_editor(page, content):
    # Try atto editor first
    editor_locator = page.locator('.editor_atto_content')
    if editor_locator.is_visible():
        editor_locator.fill("")
        editor_locator.evaluate(f"el => el.innerHTML = `{content}`")
    else:
        # Fallback to standard textarea
        page.fill('textarea[name="introeditor[text]"]', content)

def build_course():
    try:
        with open('course_structure.json', 'r', encoding='utf-8') as f:
            course_structure = json.load(f)
    except FileNotFoundError:
        print("Error: course_structure.json not found!")
        return

    username, password = get_credentials()

    with sync_playwright() as p:
        # Launch browser in non-headless mode
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()

        print(f"Logging in to {LOGIN_URL}...")
        page.goto(LOGIN_URL)
        
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        
        if "login/index.php" in page.url:
            submit_btn = page.locator('button[type="submit"]')
            if submit_btn.is_visible():
                submit_btn.first.click()

        page.wait_for_load_state('networkidle')
        if "login/index.php" in page.url:
             print("Login failed. Please check your credentials.")
             browser.close()
             return
             
        print("Login successful!")

        for chapter in course_structure:
            section_id = chapter['chapter_id']
            chapter_title = chapter['title']
            
            print(f"\n=======================================================")
            print(f"--- Processing {chapter_title} (Section {section_id}) ---")
            print(f"=======================================================\n")
            
            for week_data in chapter['weeks']:
                week_title = week_data['title']
                resources = week_data['resources']
                print(f"\n--- Adding resources for {week_title} ---")
                
                for res in resources:
                    res_type = res['type']
                    title = res['title']
                    url = res['url']
                    description = res['description']
                    
                    print(f"Adding {res_type}: {title}")
                    
                    if res_type == "URL":
                        add_url = f"{MOODLE_DOMAIN}/course/modedit.php?add=url&type=&course={COURSE_ID}&section={section_id}&return=0&sr=0"
                        page.goto(add_url)
                        page.wait_for_load_state('networkidle')
                        
                        page.fill('input[name="name"]', title)
                        page.fill('input[name="externalurl"]', url)
                        fill_atto_editor(page, description)
                        
                    elif res_type == "Assignment":
                        add_url = f"{MOODLE_DOMAIN}/course/modedit.php?add=assign&type=&course={COURSE_ID}&section={section_id}&return=0&sr=0"
                        page.goto(add_url)
                        page.wait_for_load_state('networkidle')
                        
                        page.fill('input[name="name"]', title)
                        fill_atto_editor(page, description)
                    
                    # Save and return to course
                    page.click('#id_submitbutton2')
                    page.wait_for_load_state('networkidle')
                    print(f"Successfully added {title}")

        print("\nAll tasks complete! Closing browser in 5 seconds...")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    build_course()
