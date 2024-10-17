from component import login
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import os
from component.init import CSVFileSelector
from component.logincci import loginprocess
from component.logincci import decoder
import mylogger
import datetime

#LOG
log_file_name = 'output.log'
log_file, original_stdout = mylogger.setup_logger(log_file_name)

for _ in range(5) :
    log_file.write(f'\n')
log_file.write(f'Application started at {datetime.datetime.now()}\n')

#CSV SELECTOR
csv_selector = CSVFileSelector()
csv_selector.run()
print(csv_selector.file_path)
file_path_CSV = csv_selector.file_path

# Input the username and password in login process
decoded_username, decoded_password = '',''
decoded_username, decoded_password = decoder()
loginprocess(decoded_username, decoded_password)
decoded_username, decoded_password = decoder()

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
        wait = WebDriverWait(driver, 90)  # Adjust the timeout as needed

        # Wait for elements on the login page to be present
        username_input = wait.until(EC.presence_of_element_located((By.NAME, 'callback_0')))
        password_input = wait.until(EC.presence_of_element_located((By.NAME, 'callback_1')))
        login_button = wait.until(EC.presence_of_element_located((By.NAME, 'callback_2')))

        # Submit the login form
        username_input.send_keys(decoded_username)
        password_input.send_keys(decoded_password)
        login_button.click()

    except Exception as e:
        print('chrome driver error or user terminate')
        print(f"An error occurred: {str(e)}")
        

from component import pullBU
data = pullBU.pullBU_APP(file_path_CSV)
print("****************************")
print("Pulling Success :")
for row in data :
    print(row["BU"],row["APP"])
print("****************************")

for Data_NUM  in data:

    # Create the folder if it doesn't exist to list what we doing
    save_directory = "data"
    folder_name = f"{Data_NUM['BU']}.{Data_NUM['APP']}"
    folder_path = os.path.join(save_directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # BU Search
    wait = WebDriverWait(driver,90)  # Adjust the timeout as needed
    BU_search = wait.until(EC.presence_of_element_located((By.ID, 'typeahead')))         
    BU_search.send_keys(Data_NUM["BU"])
    time.sleep(5)

    try: 

        wait = WebDriverWait(driver, 10)

        try:
            BU_search_click = wait.until(EC.presence_of_element_located((By.ID, 'ngb-typeahead-2-0')))
            BU_search_click.click()
        except:
            BU_search_click = wait.until(EC.presence_of_element_located((By.ID, 'ngb-typeahead-1-0')))
            BU_search_click.click()

        try:

            #Wait for a specific element to be visible the pcr page to ensure it is fully loaded 
            wait = WebDriverWait(driver, 90) 
            specific_element = wait.until(EC.visibility_of_element_located((By.ID, 'coordinatesLatitude')))

            #Home Page Print
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            body_content = soup.body.prettify()  

            # Define the directory where you want to save the HTML file
            # Create the folder if it doesn't exist
            save_directory = "data"
            folder_name = f"{Data_NUM['BU']}.{Data_NUM['APP']}"
            folder_path = os.path.join(save_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_name = f"{Data_NUM['BU']}.{Data_NUM['APP']} HOME.html"
            file_path = os.path.join(folder_path, file_name)

            # Save the body content to the file inside the new folder
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(body_content)

            print(f"Homepage content saved as '{file_path}'")

            #PCR Page Click
            wait = WebDriverWait(driver, 8)
            switch = False

            for _ in range(5) :

                if switch:
                    break
                try :
                    time.sleep(5)
                    BU_search_click_PCR = wait.until(EC.presence_of_element_located((By.ID, 'pcrLink')))
                    BU_search_click_PCR.click()
                    switch = True
                except :
                    try :
                        BU_search_click_PCR = wait.until(EC.presence_of_element_located((By.ID, 'PCR')))
                        BU_search_click_PCR.click()
                        switch = True
                        pass
                        break
                    except:
                        pass # Handle the case where both attempts timeout
                          
            # Page Focus Switch
            window_before = driver.window_handles[0]
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)

            #Wait for a specific element to be visible the pcr page to ensure it is fully loaded 
            wait = WebDriverWait(driver, 90) 
            specific_element = wait.until(EC.visibility_of_element_located((By.ID, 'tsaReportsTable')))

            # Get the page source (HTML content) after the search and Use BeautifulSoup to parse the HTML content
            # Extract and save only the body of the HTML page
            # Use .prettify() for nicely formatted HTML
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            body_content = soup.body.prettify()  

            # Define the directory where you want to save the HTML file
            # Create the folder if it doesn't exist
            save_directory = "data"
            folder_name = f"{Data_NUM['BU']}.{Data_NUM['APP']}"
            folder_path = os.path.join(save_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_name = f"{Data_NUM['BU']}.{Data_NUM['APP']} PCR.html"
            file_path = os.path.join(folder_path, file_name)

            # Save the body content to the file inside the new folder
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(body_content)

            print(f"Body content saved as '{file_path}'")


            #_________________________________________________________________________APP BODY PULL

            # Locate an anchor (<a>) element by its data-appid attribute using a CSS selector
            print("Looking Application of : "+ f"{Data_NUM['BU']}.{Data_NUM['APP']}")
            element = driver.find_element(By.CSS_SELECTOR, f"[data-appid='{Data_NUM['APP']}']")
            # Click on the anchor element
            element.click()
            time.sleep(5)

            # Page Focus Switch
            window_before = driver.window_handles[1]
            window_after = driver.window_handles[2]
            driver.switch_to.window(window_after)

            #Wait for a specific element to be visible the App page to ensure it is fully loaded 
            wait = WebDriverWait(driver, 90) 
            specific_element = wait.until(EC.visibility_of_element_located((By.ID, 'originalSubmitDate')))

            # Get the page source (HTML content) after the search and Use BeautifulSoup to parse the HTML content
            # Extract and save only the body of the HTML page
            # Use .prettify() for nicely formatted HTML
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            body_content = soup.body.prettify()  

            # Define the directory where you want to save the HTML file
            # Create the folder if it doesn't exist
            save_directory = "data"
            folder_name = f"{Data_NUM['BU']}.{Data_NUM['APP']}"
            folder_path = os.path.join(save_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_name = f"{Data_NUM['BU']}.{Data_NUM['APP']} APP.html"
            file_path = os.path.join(folder_path, file_name)

            # Save the body content to the file inside the new folder
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(body_content)

            print(f"Application content saved as '{file_path}'")

            # Close the current window (the new one)
            driver.close()

            # Switch back to the previous window
            driver.switch_to.window(window_before)

            #_________________________________________________________________________WO BODY PULL

            # Locate an anchor (<a>) element by its data-appid attribute using a CSS selector
            print("Looking WO for : "+ f"{Data_NUM['BU']}.{Data_NUM['APP']}")
            
            try : 
                data_appid = Data_NUM['APP']
                xpath_appid = f"//a[@data-appid='{data_appid}']"
                appid_element = driver.find_element(By.XPATH, xpath_appid)
                xpath_work_order = "./preceding::a[contains(@class, 'tsaReportWorkOrderLink')][1]"
                work_order_element = appid_element.find_element(By.XPATH, xpath_work_order)
                work_order_element.click()
                time.sleep(5)
            except :
                element = driver.find_element(By.CSS_SELECTOR, f"[data-bu='{Data_NUM['BU']}']")
                # Click on the anchor element
                element.click()
                print('error : the latest WO has been downloaded please recheck')
                time.sleep(5)

            # Page Focus Switch
            window_before = driver.window_handles[1]
            window_after = driver.window_handles[2]
            driver.switch_to.window(window_after)

            #Wait for a specific element to be visible the App page to ensure it is fully loaded 
            wait = WebDriverWait(driver, 90) 
            specific_element = wait.until(EC.visibility_of_element_located((By.ID, 'commentsTextLabel')))

            # Get the page source (HTML content) after the search and Use BeautifulSoup to parse the HTML content
            # Extract and save only the body of the HTML page
            # Use .prettify() for nicely formatted HTML
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            body_content = soup.body.prettify()  

            # Define the directory where you want to save the HTML file
            # Create the folder if it doesn't exist
            save_directory = "data"
            folder_name = f"{Data_NUM['BU']}.{Data_NUM['APP']}"
            folder_path = os.path.join(save_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_name = f"{Data_NUM['BU']}.{Data_NUM['APP']} WO.html"
            file_path = os.path.join(folder_path, file_name)

            # Save the body content to the file inside the new folder
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(body_content)

            print(f"WO content saved as '{file_path}'")

            # Close the current window (the new one)
            driver.close()

            # Switch back to the previous window
            driver.switch_to.window(window_before)
            driver.close()
            window_before = driver.window_handles[0]
            driver.switch_to.window(window_before)

            print("----------Sub-Session-End----------")
            
            # Navigate to CCI's homepage
            url = 'https://www.ccisites.com/home/ui/'
            driver.get(url)
            
        except Exception as e :
            window_before = driver.window_handles[0]
            window_after = driver.window_handles[1]
            driver.close()
            driver.switch_to.window(window_before)
            print("Tower has Structure A & B - or - No WO for this APP")
            print("----------Sub-Session-End----------")
            url = 'https://www.ccisites.com/home/ui/'
            driver.get(url)
            continue
    
    except Exception as e:
        print("error searching at "+f"{Data_NUM['BU']}.{Data_NUM['APP']}")
        print("----------Sub-Session-End----------")
        # Navigate to CCI's homepage
        url = 'https://www.ccisites.com/home/ui/'
        driver.get(url)
        time.sleep(5)

print("----/////all input data collected/////----") 

# Call the data_check function to obtain valid_folders and invalid_folders
from component.data_check import data_check
valid_folders, invalid_folders_no_WO, invalid_folders_AB, invalid_folders_errorsearch, invalid_folders_Unknow, invalid_folders_storage = data_check()

#Call the combine_html function to process valid_folders
from component.combinator import combine_html
combine_html(valid_folders)

#Call the data_extract function to process data extraction
from component.data_extract import data_extract
data_extract(valid_folders,invalid_folders_storage)

#Call the CSV writer
from component.csv_summary import csv_summary
csv_summary()

print("##############      COMPLETED          ############## ") 
print("############## MANUAL COPY LOG AS NEED ############## ")
mylogger.close_logger(log_file, original_stdout) 

time.sleep(100)


