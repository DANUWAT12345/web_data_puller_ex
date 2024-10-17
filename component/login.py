def login() :

    import tkinter as tk
    from tkinter import filedialog
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    import time

    # Create a simple tkinter window for file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask the user to select the Chrome WebDriver executable
    chromedriver_path = filedialog.askopenfilename(title="Select Chrome WebDriver")

    # Check if the user canceled the file dialog
    if not chromedriver_path:
        print("Chrome WebDriver selection canceled.")
    else:
        try:
            # Set the 'webdriver.chrome.driver' system property to the selected path
            webdriver.chrome.service.service_args = ['--webdriver.chrome.driver=' + chromedriver_path]

            # Create an instance of the Chrome WebDriver
            driver = webdriver.Chrome()

            # Navigate to CCI's homepage
            url = 'https://www.ccisites.com/home/ui/'
            driver.get(url)

            # Define a WebDriverWait with a timeout (in seconds)
            wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed

            # Wait for elements on the login page to be present
            username_input = wait.until(EC.presence_of_element_located((By.NAME, 'callback_0')))
            password_input = wait.until(EC.presence_of_element_located((By.NAME, 'callback_1')))
            login_button = wait.until(EC.presence_of_element_located((By.NAME, 'callback_2')))

            # Input the username and password
            username_input.send_keys("DMAOLEETHONG_EXT")
            password_input.send_keys("@1dev2xp7F")

            # Submit the login form
            login_button.click()

            time.sleep(10)

        except Exception as e:
            print(f"An error occurred: {str(e)}")