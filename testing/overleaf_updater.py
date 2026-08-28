import os
import glob
import time
import getpass
import datetime
import re
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def get_credentials():
    email = os.environ.get('OVERLEAF_EMAIL')
    password = os.environ.get('OVERLEAF_PASSWORD')
    project_url = os.environ.get('OVERLEAF_PROJECT_URL')
    parent_folder = os.environ.get('OVERLEAF_PARENT_FOLDER')
    
    if not email:
        email = input("Enter your Overleaf Email: ")
    if not password:
        password = getpass.getpass("Enter your Overleaf Password: ")
    if not project_url:
        project_url = input("Enter your Overleaf Project URL: ")
        
    return email, password, project_url, parent_folder

def find_files_to_upload():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    weeks = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('Semana_')]
    
    files_by_week = {}
    for week in sorted(weeks):
        week_path = os.path.join(base_dir, week)
        tex_files = glob.glob(os.path.join(week_path, '*.tex'))
        img_extensions = ['*.png', '*.jpg', '*.jpeg']
        img_files = []
        for ext in img_extensions:
            img_files.extend(glob.glob(os.path.join(week_path, ext)))
            
        all_files = tex_files + img_files
        if all_files:
            files_by_week[week] = {
                'files': all_files,
                'path': week_path,
                'tex_files': tex_files
            }
    return files_by_week

def print_dom_debug(page):
    print("\n--- DEBUG: Dumping File Tree Header HTML ---")
    try:
        header = page.locator('*:has-text("File tree")').last
        if header.is_visible():
             parent = header.locator('..').locator('..')
             print(parent.inner_html())
        else:
             print("Could not find 'File tree' text.")
    except Exception as e:
        print(f"Debug failed: {e}")
    print("--------------------------------------------\n")

def get_folder_locator(page, folder_name):
    """Locator for checking if a folder text exists in the tree."""
    return page.locator('.file-tree').get_by_text(folder_name, exact=True).first

def click_folder(page, folder_name):
    """Intelligently expand and select a folder without accidentally collapsing it."""
    print(f"Attempting to select folder '{folder_name}'...")
    
    # 1. Check if it's explicitly collapsed by looking for the "Expand" button
    safe_name = re.escape(folder_name)
    expand_btn = page.locator('.file-tree').get_by_role("button", name=re.compile(f"Expand {safe_name}", re.IGNORECASE)).first
    if expand_btn.is_visible():
        print(f"Folder '{folder_name}' is collapsed. Clicking to expand it...")
        expand_btn.click()
        time.sleep(1.5)
        
    # 2. Select it by clicking its text label (avoids toggling the chevron)
    try:
        label = page.locator('.file-tree').get_by_text(folder_name, exact=True).first
        label.wait_for(state='visible', timeout=5000)
        label.click()
        time.sleep(2) # Give the UI time to register the selection
        return True
    except Exception as e:
        print(f"Warning: Could not select folder '{folder_name}' by text: {e}")
        return False

def run_automation():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"==================================================")
    print(f"Overleaf Automation Script Started at: {current_time}")
    print(f"==================================================")
    
    email, password, project_url, parent_folder = get_credentials()
    files_by_week = find_files_to_upload()
    
    if not files_by_week:
        print("No LaTeX or image files found in Semana_* folders.")
        return

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
            print("Login failed or took too long. Check credentials.")
            browser.close()
            return
            
        print(f"Navigating to Project: {project_url}")
        page.goto(project_url)
        page.wait_for_selector('.pdf-viewer, .editor', timeout=30000)
        
        # 1. PARENT FOLDER NAVIGATION
        if parent_folder:
            print(f"\nChecking for parent folder: {parent_folder}")
            # Ensure no other folder is selected by clicking the root "File tree" area if needed,
            # or we just try to click the parent folder if it exists.
            folder_locator = get_folder_locator(page, parent_folder)
            if folder_locator.is_visible():
                print(f"Found existing parent folder: {parent_folder}. Selecting it.")
                click_folder(page, parent_folder)
            else:
                print(f"Parent folder not found. Creating {parent_folder}...")
                new_folder_btn = page.locator('.file-tree-toolbar-action-buttons button:has-text("New folder"), button[aria-label="New folder" i], [uib-tooltip="New folder" i]').first
                if new_folder_btn.is_visible():
                    new_folder_btn.click()
                    page.wait_for_selector('.modal-dialog', timeout=5000)
                    page.fill('.modal-dialog input[type="text"]', parent_folder)
                    page.click('.modal-dialog button:has-text("Create")')
                    
                    # Wait for modal to either close or show an error
                    time.sleep(2) 
                    
                    if page.locator('.modal-dialog').is_visible():
                        if page.locator('.modal-dialog:has-text("already exists")').is_visible() or page.locator('.modal-dialog .text-danger').is_visible():
                            print(f"Parent folder '{parent_folder}' already exists message detected. Canceling...")
                            cancel_btn = page.locator('.modal-dialog button:has-text("Cancel")').first
                            if cancel_btn.is_visible():
                                cancel_btn.click()
                            try:
                                page.wait_for_selector('.modal-dialog', state='hidden', timeout=3000)
                            except:
                                pass
                            
                            click_folder(page, parent_folder)
                    else:
                        print(f"Clicking newly created parent folder '{parent_folder}' to gain focus...")
                        click_folder(page, parent_folder)
                else:
                    print("Warning: New folder button not found! Attempting DOM debug dump...")
                    print_dom_debug(page)
        
        for week, data in files_by_week.items():
            files = data['files']
            week_path = data['path']
            tex_files = data['tex_files']
            
            print(f"\nProcessing {week}...")
            
            try:
                # 2. SUBFOLDER NAVIGATION
                # First ensure we are in the parent folder before checking/creating subfolder
                if parent_folder:
                    print(f"Ensuring parent folder '{parent_folder}' is selected before working on '{week}'...")
                    click_folder(page, parent_folder)

                print(f"Checking for subfolder: {week}")
                week_locator = get_folder_locator(page, week)
                if week_locator.is_visible():
                    print(f"Found existing subfolder: {week}. Selecting it.")
                    click_folder(page, week)
                else:
                    print(f"Subfolder not found. Creating {week}...")
                    new_folder_btn = page.locator('.file-tree-toolbar-action-buttons button:has-text("New folder"), button[aria-label="New folder" i], [uib-tooltip="New folder" i]').first
                    if new_folder_btn.is_visible():
                        new_folder_btn.click()
                        page.wait_for_selector('.modal-dialog', timeout=5000)
                        page.fill('.modal-dialog input[type="text"]', week)
                        page.click('.modal-dialog button:has-text("Create")')
                        
                        time.sleep(2)
                        
                        # Check if the modal is still open and showing an error
                        if page.locator('.modal-dialog').is_visible():
                            if page.locator('.modal-dialog:has-text("already exists")').is_visible() or page.locator('.modal-dialog .text-danger').is_visible():
                                print(f"Folder '{week}' already exists message detected. Canceling...")
                                cancel_btn = page.locator('.modal-dialog button:has-text("Cancel")').first
                                if cancel_btn.is_visible():
                                    cancel_btn.click()
                                try:
                                    page.wait_for_selector('.modal-dialog', state='hidden', timeout=3000)
                                except:
                                    pass
                                
                                # We need to expand the parent to see it
                                print(f"Double-clicking parent folder to expand and reveal '{week}'...")
                                if parent_folder:
                                    parent_locator = get_folder_locator(page, parent_folder)
                                    if parent_locator.is_visible():
                                        parent_locator.dblclick() # dblclick toggles expansion in most file trees
                                        time.sleep(2)
                                
                                click_folder(page, week)
                        else:
                            print(f"Clicking newly created folder '{week}' to gain focus...")
                            click_folder(page, week)
                    else:
                        print("Warning: New folder button not found.")

                # 3. UPLOAD FILES
                print(f"Uploading files to {week}: {[os.path.basename(f) for f in files]}")
                upload_btn = page.locator('.file-tree-toolbar-action-buttons button:has-text("Upload"), button[aria-label="Upload" i], [uib-tooltip="Upload" i]').first
                if upload_btn.is_visible():
                    upload_btn.click()
                    page.wait_for_selector('.modal-dialog', timeout=5000)
                    file_input = page.locator('.modal-dialog input[type="file"]:not([webkitdirectory])').first
                    file_input.set_input_files(files)
                    time.sleep(3)
                    
                    # Handle possible file overwrite prompt
                    overwrite_prompt = page.locator('.modal-dialog:has-text("already exists"), .modal-dialog:has-text("overwrite"), .modal-dialog:has-text("replace")')
                    if overwrite_prompt.is_visible():
                        print("File overwrite prompt detected. Attempting to confirm...")
                        replace_btn = page.locator('.modal-dialog button:has-text("Replace"), .modal-dialog button:has-text("Overwrite"), .modal-dialog button:has-text("OK"), .modal-dialog button:has-text("Yes")').first
                        if replace_btn.is_visible():
                            replace_btn.click()
                            time.sleep(2)
                        else:
                            # if no confirm button, maybe it just wants us to cancel?
                            cancel_btn = page.locator('.modal-dialog button:has-text("Cancel")').first
                            if cancel_btn.is_visible():
                                cancel_btn.click()
                    
                    time.sleep(2)
                    close_btn = page.locator('.modal-dialog button.close, .modal-dialog [aria-label="Close"]').first
                    if close_btn.is_visible():
                        close_btn.click()
                        
                    # Wait a moment for the file tree to update after uploading
                    time.sleep(3)
                    print(f"Successfully uploaded files for {week}")
                else:
                    print("Error: Could not find Upload button.")
                    print_dom_debug(page)
                    continue
                
                # 4. MULTI-FILE COMPILATION
                for tex_file in tex_files:
                    main_tex_name = os.path.basename(tex_file)
                    print(f"\n>> Selecting {main_tex_name} to compile...")
                    # Find the file in the tree (the inspector recommended get_by_text)
                    tex_file_locator = page.locator('.file-tree').get_by_text(main_tex_name).first
                    if tex_file_locator.is_visible():
                        tex_file_locator.click()
                        time.sleep(3) # Wait longer for editor/preview to fully load
                        
                        print(f"Compiling {main_tex_name}...")
                        recompile_btn = page.locator('.btn-recompile, button:has-text("Recompile")').first
                        if recompile_btn.is_visible():
                            recompile_btn.click()
                            print("Waiting for compilation to finish (20 seconds)...")
                            time.sleep(20)
                            
                            print("Downloading PDF...")
                            download_btn = page.locator('[aria-label="Download PDF"], [uib-tooltip="Download PDF"], [title="Download PDF"], i.fa-download, button:has(svg[data-icon="download"])').first
                            if download_btn.is_visible():
                                with page.expect_download() as download_info:
                                    download_btn.click()
                                
                                download = download_info.value
                                pdf_name = main_tex_name.replace('.tex', '.pdf')
                                download_path = os.path.join(week_path, pdf_name)
                                
                                # 5. OVERWRITE LOCAL FILE IF IT EXISTS
                                if os.path.exists(download_path):
                                    print(f"Removing existing local file: {download_path}")
                                    os.remove(download_path)
                                    
                                download.save_as(download_path)
                                print(f"Successfully saved PDF to {download_path}")
                            else:
                                print("Warning: Download PDF button not found.")
                        else:
                             print("Warning: Recompile button not found.")
                    else:
                        print(f"Warning: Could not find {main_tex_name} in the file tree.")
                        
            except Exception as e:
                print(f"Error processing {week}: {e}")
                
        current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nAll tasks complete at {current_time_end}! Closing browser in 5 seconds...")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    run_automation()
