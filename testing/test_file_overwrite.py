import os
import time
import re
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def run_test():
    email = os.environ.get('OVERLEAF_EMAIL')
    password = os.environ.get('OVERLEAF_PASSWORD')
    project_url = os.environ.get('OVERLEAF_PROJECT_URL')

    if not all([email, password, project_url]):
        print("Missing credentials in .env file.")
        return

    test_folder = f"Test_Overwrite_{int(time.time())}"
    dummy_file_name = "dummy_test.tex"
    new_content = "% This content was PASTED by Playwright!\n\\documentclass{article}\n\\begin{document}\nHello World from the Editor!\n\\end{document}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        print("Logging in to Overleaf...")
        page.goto('https://www.overleaf.com/login')
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.click('button:has-text("Log in"), button[type="submit"]')
        
        try:
            page.wait_for_url('**/project**', timeout=15000)
            print("Login successful!")
        except Exception:
            print("Login failed.")
            return
            
        print(f"Navigating to Project: {project_url}")
        page.goto(project_url)
        page.wait_for_selector('.pdf-viewer, .editor', timeout=30000)
        
        # 1. Create Folder
        print(f"\n--- 1. Creating Folder: {test_folder} ---")
        new_folder_btn = page.locator('.file-tree-toolbar-action-buttons button:has-text("New folder"), button[aria-label="New folder" i], [uib-tooltip="New folder" i]').first
        if new_folder_btn.is_visible():
            new_folder_btn.click()
            page.wait_for_selector('.modal-dialog', timeout=5000)
            page.fill('.modal-dialog input[type="text"]', test_folder)
            page.click('.modal-dialog button:has-text("Create")')
            time.sleep(2)
            
            # Gain focus
            folder_button = page.get_by_role("button", name=re.compile(test_folder, re.IGNORECASE)).first
            if folder_button.is_visible():
                folder_button.click()
                time.sleep(1)

        # 2. Create an empty file in Overleaf (instead of uploading, we just create a new blank one to simulate it existing)
        print(f"\n--- 2. Creating an empty file '{dummy_file_name}' to simulate it existing ---")
        new_file_btn = page.locator('.file-tree-toolbar-action-buttons button:has-text("New file"), button[aria-label="New file" i], [uib-tooltip="New file" i]').first
        if new_file_btn.is_visible():
            new_file_btn.click()
            page.wait_for_selector('.modal-dialog', timeout=5000)
            page.fill('.modal-dialog input[type="text"]', dummy_file_name)
            page.click('.modal-dialog button:has-text("Create")')
            time.sleep(2)
            
        # 3. Select the file and overwrite its content via the editor!
        print(f"\n--- 3. Overwriting content inside the Editor ---")
        
        # Make sure the file is selected (it usually is automatically after creation)
        tex_file_locator = page.locator('.file-tree').get_by_text(dummy_file_name).first
        if tex_file_locator.is_visible():
            tex_file_locator.click()
            time.sleep(2) # Wait for editor to load
            
            print("Clicking inside the editor...")
            # Click inside the editor area to gain keyboard focus
            editor = page.locator('.editor, .cm-content, .ace_editor').first
            editor.click()
            
            print("Selecting all existing text (Ctrl+A)...")
            page.keyboard.press('Control+A')
            time.sleep(0.5)
            
            print("Deleting existing text (Backspace)...")
            page.keyboard.press('Backspace')
            time.sleep(0.5)
            
            print("Pasting new content from local file...")
            # insert_text is Playwright's robust way to type blocks of text instantly (like a paste)
            page.keyboard.insert_text(new_content)
            
            print("✅ SUCCESS! Content has been replaced via the editor.")
        else:
            print(f"❌ ERROR: Could not find '{dummy_file_name}' to click it.")

        print("\nPausing for 5 seconds so you can visually verify the editor has the new text...")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    run_test()
