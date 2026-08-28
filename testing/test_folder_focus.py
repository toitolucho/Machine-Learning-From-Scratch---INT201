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

    test_folder = f"Test_Upload_{int(time.time())}"
    dummy_file_path = os.path.join(os.path.dirname(__file__), "dummy_test.tex")
    
    # Create a dummy tex file locally to upload
    with open(dummy_file_path, "w") as f:
        f.write("% Dummy test file for upload verification\n\\documentclass{article}\n\\begin{document}\nHello World!\n\\end{document}")

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
        print(f"\n--- 1. Creating and Focusing Folder: {test_folder} ---")
        new_folder_btn = page.locator('.file-tree-toolbar-action-buttons button:has-text("New folder"), button[aria-label="New folder" i], [uib-tooltip="New folder" i]').first
        if new_folder_btn.is_visible():
            new_folder_btn.click()
            page.wait_for_selector('.modal-dialog', timeout=5000)
            page.fill('.modal-dialog input[type="text"]', test_folder)
            page.click('.modal-dialog button:has-text("Create")')
            time.sleep(1.5)
            
            if page.locator('.modal-dialog').is_visible():
                page.click('.modal-dialog button:has-text("Cancel")')
                
            folder_button = page.get_by_role("button", name=re.compile(test_folder, re.IGNORECASE)).first
            if folder_button.is_visible():
                folder_button.click()
                print(f"✅ Clicked '{test_folder}' to gain focus.")
            else:
                print(f"❌ ERROR: Could not find '{test_folder}' to gain focus.")
                return

        # 2. Upload File
        print("\n--- 2. Uploading dummy_test.tex ---")
        upload_btn = page.locator('.file-tree-toolbar-action-buttons button:has-text("Upload"), button[aria-label="Upload" i], [uib-tooltip="Upload" i]').first
        
        if upload_btn.is_visible():
            upload_btn.click()
            page.wait_for_selector('.modal-dialog', timeout=5000)
            
            file_input = page.locator('.modal-dialog input[type="file"]:not([webkitdirectory])').first
            file_input.set_input_files([dummy_file_path])
            
            time.sleep(3)
            # Check for overwrite modal
            overwrite_prompt = page.locator('.modal-dialog:has-text("already exists"), .modal-dialog:has-text("overwrite"), .modal-dialog:has-text("replace")')
            if overwrite_prompt.is_visible():
                replace_btn = page.locator('.modal-dialog button:has-text("Replace"), .modal-dialog button:has-text("Overwrite"), .modal-dialog button:has-text("OK"), .modal-dialog button:has-text("Yes")').first
                if replace_btn.is_visible():
                    replace_btn.click()
                    time.sleep(2)
                else:
                    cancel_btn = page.locator('.modal-dialog button:has-text("Cancel")').first
                    if cancel_btn.is_visible():
                        cancel_btn.click()
            
            time.sleep(2)
            close_btn = page.locator('.modal-dialog button.close, .modal-dialog [aria-label="Close"]').first
            if close_btn.is_visible():
                close_btn.click()
                
            print("✅ Upload process completed.")
        else:
            print("❌ ERROR: Could not find Upload button.")
            return
            
        # 3. Verify File Selection
        print("\n--- 3. Verifying File is in the Tree ---")
        tex_file_locator = page.get_by_role("button", name=re.compile("dummy_test.tex", re.IGNORECASE)).first
        
        # Fallback to standard selector if get_by_role doesn't find the file
        if not tex_file_locator.is_visible():
             tex_file_locator = page.locator('.file-tree button[aria-label*="dummy_test.tex" i], .file-tree .name:has-text("dummy_test.tex")').first

        if tex_file_locator.is_visible():
            tex_file_locator.click()
            print("✅ SUCCESS! Found and clicked 'dummy_test.tex'. If it is inside the folder, the focus logic works perfectly!")
        else:
            print("❌ ERROR: Could not find 'dummy_test.tex' in the file tree.")
            print("\n========================================================")
            print("I am pausing the script. Please use the Playwright Inspector")
            print("to click 'Explore' and hover over 'dummy_test.tex'.")
            print("Tell me what Locator it recommends!")
            print("========================================================\n")
            page.pause()

        print("\nPausing for 5 seconds so you can visually verify the file is inside the folder...")
        time.sleep(5)
        browser.close()
        
        # Cleanup local file
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path)

if __name__ == "__main__":
    run_test()
