import time
import os
import glob
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ===============================================================
# ===============  CONFIG: PLEASE EDIT THESE!  ==================
# ===============================================================
# I have removed your credentials for your safety. Please re-enter them.
CLASSKICK_URL = "https://app.classkick.com/account/student-works/AZfDD7gdRe64GW0IbAOAUA/questions/AZeu2F_LSlW4uCdd-jxnDg"  # <--- PASTE YOUR ASSIGNMENT LINK HERE
CLASSKICK_USERNAME = "Daniel_Xu"  # <--- PUT YOUR USERNAME/EMAIL HERE
CLASSKICK_PASSWORD = "Daniel12345?"  # <--- PUT YOUR PASSWORD HERE
IMAGE_FOLDER = "homework_images"
# ===============================================================

def find_image_files(folder):
    """Finds image files in the specified folder and sorts them."""
    search_patterns = [
        os.path.join(folder, '*.jpg'),
        os.path.join(folder, '*.jpeg'),
        os.path.join(folder, '*.png')
    ]
    files = sorted([f for p in search_patterns for f in glob.glob(p)])
    print(f"Found {len(files)} image files: {[os.path.basename(f) for f in files]}")
    return files

def upload_to_classkick():
    """Automates uploading images to Classkick, bypassing overlays with JS clicks."""
    image_files = find_image_files(IMAGE_FOLDER)
    if not image_files:
        print("[ERROR] No image files found in the specified folder. Exiting.")
        return

    print("\n" + "="*60)
    print("⚠️  WARNING: THIS SCRIPT WILL TAKE CONTROL OF YOUR MOUSE/KEYBOARD. ⚠️")
    print("         >>> DO NOT TOUCH ANYTHING DURING THE PROCESS <<<")
    print("="*60 + "\n")
    time.sleep(4)

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    try:
        # --- Login ---
        print("Navigating to Classkick and logging in...")
        driver.get(CLASSKICK_URL)
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="emailOrUsername"]')))
        username_input.send_keys(CLASSKICK_USERNAME)
        driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(CLASSKICK_PASSWORD)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]"))).click()
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.ck-select-icon")))
        print("Login Successful.")

        # --- Main Upload Loop ---
        for i, image_path in enumerate(image_files):
            page_number = i + 1
            absolute_image_path = os.path.abspath(image_path)
            print(f"\n--- Processing Page {page_number}: {os.path.basename(image_path)} ---")
            
            # 1. Navigate to the correct slide
            print("Selecting slide...")
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.ck-select-icon"))).click()
            time.sleep(0.5)
            slide_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[normalize-space() = 'Slide {page_number}']")))
            driver.execute_script("arguments[0].click();", slide_link)
            time.sleep(1.5)

            # 2. Open the image menu
            print("Opening image upload dialog...")
            add_image_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add Image']")))
            driver.execute_script("arguments[0].click();", add_image_button)
            
            # =================== THIS IS THE CORRECTED LINE ===================
            # 3. Click the "Upload from file" button USING JAVASCRIPT to bypass the overlay
            print("Clicking 'Upload from File'...")
            upload_from_file_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Create an image by uploading a file']")))
            driver.execute_script("arguments[0].click();", upload_from_file_button)
            # =================================================================

            # 4. Use PyAutoGUI to handle the native OS file dialog
            print("Selecting file with PyAutoGUI...")
            time.sleep(2) # IMPORTANT: Wait for the OS file dialog to appear
            pyautogui.hotkey('command', 'shift', 'g')
            time.sleep(1)
            pyautogui.write(os.path.dirname(absolute_image_path))
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.write(os.path.basename(absolute_image_path))
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')

            # 5. Click "Next" and "Finish" in the Classkick UI
            print("Waiting for upload preview screen...")
            
            next_button_xpath = "//button[@aria-label='next']"
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            print("Bypassing overlay to click 'Next'...")
            driver.execute_script("arguments[0].click();", next_button)
            
            finish_button_xpath = "//button[@aria-label='finish']"
            finish_button = wait.until(EC.element_to_be_clickable((By.XPATH, finish_button_xpath)))
            print("Bypassing overlay to click 'Finish'...")
            driver.execute_script("arguments[0].click();", finish_button)
            
            # =================== THIS IS THE CRUCIAL FIX ===================
            # 5. Wait for the upload dialog box to completely disappear before continuing
            print("Confirming upload dialog has closed...")
            dialog_locator = (By.CSS_SELECTOR, "div.md-dialog-container")
            wait.until(EC.invisibility_of_element_located(dialog_locator))
            # ===============================================================

            print(f"✅ Successfully uploaded image to Page {page_number}!")

        print("\n\n🎉 All images have been uploaded successfully!")

    except TimeoutException as e:
        print(f"\n[ERROR] A timeout occurred. An element was not found in time. Check your selectors or increase the wait time.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nClosing the browser in 5 seconds...")
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    upload_to_classkick()