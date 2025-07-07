# Classkick Automatic Uploader

This Python script automates the tedious process of uploading images to a multi-page Classkick assignment. It logs into your Classkick account, navigates to the specified assignment, and uploads a series of images from a local folder to the corresponding slides.

The script uses a combination of **Selenium** for browser automation and **PyAutoGUI** to handle the native OS file upload dialog, which cannot be controlled by Selenium directly.

<br>

## ⚠️ Important Warning ⚠️

This script will take **full control of your mouse and keyboard** during its operation to handle the file upload dialog.

> **DO NOT touch your mouse or keyboard while the script is running.**

You will be given a 4-second countdown before it begins.

<br>

## Features

-   ✅ Automatically logs into your Classkick account.
-   ✅ Navigates directly to the assignment link you provide.
-   ✅ Finds all images (`.png`, `.jpg`, `.jpeg`) in a specified folder.
-   ✅ Uploads images sequentially to the corresponding slides (e.g., `01.png` -> Slide 1, `02.png` -> Slide 2).
-   ✅ Uses robust JavaScript clicks to bypass potential UI overlays that can block interaction.
-   ✅ Provides real-time progress updates in the console.

<br>

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3:** [Download Python](https://www.python.org/downloads/)
2.  **Google Chrome:** The script is written for Chrome. [Download Chrome](https://www.google.com/chrome/)
3.  **ChromeDriver:** The version of ChromeDriver **must** match your version of Google Chrome.
    -   [Download ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)
    -   After downloading, make sure the `chromedriver` executable is in your system's PATH. (Or place it in the same directory as the script).

<br>

## 🛠️ Installation & Setup

1.  **Clone or Download the Repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
    Or simply download the Python script to a new folder on your computer.

2.  **Install Required Python Libraries:**
    Create a `requirements.txt` file with the following content:
    ```
    selenium
    pyautogui
    ```
    Then, install them using pip:
    ```bash
    pip install -r requirements.txt
    ```
    Alternatively, install them one by one:
    ```bash
    pip install selenium pyautogui
    ```

3.  **Prepare Your Images:**
    -   Create a folder named `homework_images` in the same directory as the script.
    -   Place all your assignment images inside this folder.
    -   **Crucially, name your files so they sort alphabetically in the correct order.** The script uploads them in this sorted order. A good naming convention is:
        -   `01_page.png`
        -   `02_page.png`
        -   `03_page.png`
        -   ...
        -   `10_page.png`

4.  **Configure the Script:**
    Open the script file (e.g., `upload_to_classkick.py`) in a text editor and fill in your details in the `CONFIG` section at the top of the file:

    ```python
    # ===============================================================
    # ===============  CONFIG: PLEASE EDIT THESE!  ==================
    # ===============================================================
    CLASSKICK_URL = "https://app.classkick.com/#/assignments/..."  # <--- PASTE YOUR ASSIGNMENT LINK HERE
    CLASSKICK_USERNAME = "your_email@example.com"                # <--- PUT YOUR USERNAME/EMAIL HERE
    CLASSKICK_PASSWORD = "your_secret_password"                  # <--- PUT YOUR PASSWORD HERE
    IMAGE_FOLDER = "homework_images"                             # Default is 'homework_images'
    # ===============================================================
    ```

<br>

## ▶️ How to Run

1.  Make sure you have completed all the steps in the **Installation & Setup** section.
2.  Open your terminal or command prompt.
3.  Navigate to the directory where you saved the script.
4.  Run the script using Python:
    ```bash
    python upload_to_classkick.py
    ```
5.  The script will print a warning and start after a short delay. **Do not interfere with your computer until the script prints that it is finished.**

<br>

## 💻 OS Compatibility Note

This script uses `pyautogui.hotkey('command', 'shift', 'g')` to open the "Go to Folder" dialog. **This is a macOS-specific shortcut.**

-   **On macOS:** The script should work as is.
-   **On Windows/Linux:** You will need to modify the `pyautogui` section of the code to work with your operating system's file dialog. A common approach for Windows is to directly type the full file path into the file name input box.

    **Potential modification for Windows/Linux:**
    Replace this block:
    ```python
    print("Selecting file with PyAutoGUI...")
    time.sleep(2)
    pyautogui.hotkey('command', 'shift', 'g')
    time.sleep(1)
    pyautogui.write(os.path.dirname(absolute_image_path))
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write(os.path.basename(absolute_image_path))
    pyautogui.press('enter')
    ```
    With something like this, which types the full path directly:
    ```python
    print("Selecting file with PyAutoGUI...")
    time.sleep(2)
    # For Windows/Linux, you can often just type the full path
    pyautogui.write(absolute_image_path)
    time.sleep(1)
    pyautogui.press('enter')
    ```

<br>

## Disclaimer

This script is for educational and personal use only. The functionality depends on the Classkick website's structure, which can change at any time. If the script stops working, it's likely because Classkick updated its UI. Use this script at your own risk.
