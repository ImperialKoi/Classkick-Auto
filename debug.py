import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ===============================================================
# ===============  CONFIG: PLEASE EDIT THESE!  ==================
# ===============================================================
CLASSKICK_URL = "https://app.classkick.com/account/student-works/AZfDD7gdRe64GW0IbAOAUA/questions/AZeu2F_LSlW4uCdd-jxnDg"  # <--- PASTE YOUR ASSIGNMENT LINK HERE
CLASSKICK_USERNAME = "Daniel_Xu"  # <--- PUT YOUR USERNAME/EMAIL HERE
CLASSKICK_PASSWORD = "Daniel12345?"      # <--- PUT YOUR PASSWORD HERE
# ===============================================================

def find_the_uploader():
    """This script's only job is to find the input element."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print("\n--- Starting Debug Probe ---")
        
        # --- 1. Log In (This part works) ---
        # --- 1. Navigate and Login ---
        print(f"Navigating to Classkick assignment...")
        driver.get(CLASSKICK_URL)
        print("Waiting for login page to load...")
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="emailOrUsername"]')))
        print("Entering username and password...")
        username_input.send_keys(CLASSKICK_USERNAME)
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys(CLASSKICK_PASSWORD)
        print("Finding the 'Log In' button by its text...")
        login_button_xpath = "//button[contains(text(), 'Log In')]"
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
        login_button.click()
        print("Login submitted. Waiting for assignment to load...")
        time.sleep(3) 

        page_number = 1
            
        print(f"\n--- Processing Page {page_number} ---")

        # A. Navigate to the correct page (Working)
        print("Opening page selector dropdown...")
        page_dropdown_selector = "span.ck-select-icon"
        page_dropdown_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, page_dropdown_selector)))
        page_dropdown_button.click()
        time.sleep(0.5)
        print(f"Selecting 'Slide {page_number}' from the list...")
        slide_selector_xpath = f"//div[normalize-space() = 'Slide {page_number}']"
        slide_link = wait.until(EC.presence_of_element_located((By.XPATH, slide_selector_xpath)))
        driver.execute_script("arguments[0].click();", slide_link)
        time.sleep(1)

        # B. Click 'Add Image' button (Working)
        print("Waiting for 'Add Image' button...")
        add_image_selector = "//button[@aria-label='Add Image']"
        wait.until(EC.element_to_be_clickable((By.XPATH, add_image_selector)))
        add_image_button = driver.find_element(By.XPATH, add_image_selector)
        driver.execute_script("arguments[0].click();", add_image_button)
        
        # IMPORTANT: WE DO NOT CLICK THE FINAL BUTTON.
        # We stop just before the file dialog would open.
        print("[4/4] Stopped right before the final click. Now probing for the input element...")
        print("--------------------------------------------------\n")
        
        # --- 4. THE PROBE ---
        found_it = False
        
        # Probe 1: Look in the main document
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            print("✅ SUCCESS: Found <input type='file'> in the main document!")
            found_it = True
        except TimeoutException:
            print("❌ FAILED: Could not find <input type='file'> in the main document.")

        # Probe 2: Look inside all iframes
        print("\nNow checking for iframes...")
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        if not iframes:
            print("No iframes found on the page.")
        else:
            print(f"Found {len(iframes)} iframe(s). Probing inside each one...")
            for index, iframe in enumerate(iframes):
                try:
                    print(f"  --> Switching to iframe #{index}")
                    driver.switch_to.frame(iframe)
                    # Now search for the input element INSIDE this iframe
                    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                    print(f"  ✅✅✅ SUCCESS: Found <input type='file'> inside iframe #{index}!")
                    found_it = True
                    break # Stop searching once we find it
                except TimeoutException:
                    print(f"  ❌ FAILED: No <input type='file'> found in iframe #{index}.")
                finally:
                    # IMPORTANT: Always switch back to the main page
                    driver.switch_to.default_content()

        print("\n--------------------------------------------------")
        if found_it:
            print("PROBE SUCCESSFUL! The element exists. We can now modify the main script.")
        else:
            print("PROBE FAILED. The element is created in a way that is truly hidden from Selenium.")

    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred during the debug: {e}")
    finally:
        print("\nDebug finished. Closing browser in 20 seconds...")
        time.sleep(20)
        driver.quit()

if __name__ == "__main__":
    find_the_uploader()