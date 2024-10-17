def data_extract(valid_folders,invalid_folders_storage):

    import os
    from bs4 import BeautifulSoup
    from datetime import datetime
    import json
    import re
    import time

    # List of folder names
    valid_folders = valid_folders 
    valid_folders.extend(invalid_folders_storage)

    # Create dictionaries to store the information for each folder
    structure_types = {}
    vendors = {}
    prices = {}
    Application_Submited_Dates = {}
    NTP_Date = {}
    SA_Completed_Dates = {}
    Manual_Pricings = {}
    Customer = {}
    Report_Types = {}
    Statuses = {}
    MetaData = {}

    # Directory where HTML files are located
    data_directory = 'data'

    # Process each folder
    for folder in valid_folders:
        # Construct the path to the HTML file for the folder
        html_file_path = os.path.join(data_directory, folder, f'{folder} combined.html')

        # Check if the HTML file exists
        if os.path.exists(html_file_path):
            # Read the HTML content from the HTML file
            with open(html_file_path, 'r',encoding='utf-8') as file:
                html_content = file.read()

            # Parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the div with the id "structureType" and extract its text
            try:
                structure_type = soup.find('div', id='structureType').text.strip()
                structure_types[folder] = structure_type
            except:
                structure_types[folder] = "Not Found"

            # Find the span with id "vendorSelectLink" and extract its text for vendor
            try:
                vendor = soup.find('span', id='vendorSelectLink').text.strip()
                vendors[folder] = vendor
            except:
                vendors[folder] = "Not Found"

            # Find the input element by its id "purchaseOrderAmountValue" and extract its value
            input_element = soup.find('input', id='purchaseOrderAmountValue')
            if input_element and 'value' in input_element.attrs:
                value = input_element['value']
                prices[folder] = value
            else:
                prices[folder] = "Not Found"
            
            # Find Original Submit Date
            submit_date = soup.find('div', id='originalSubmitDate').text.strip()
            input_date = submit_date
            try:
                date_obj = datetime.strptime(input_date, "%b %d %Y")
                formatted_date = date_obj.strftime("%Y/%m/%d")
                Application_Submited_Dates[folder] = formatted_date
            except:
                Application_Submited_Dates[folder] = "Not Found"

            # Find NTP Date
            # Find the third "Modified Date" value (Sep 14 2023 10:11 AM)
            date_elements = soup.find_all("td", class_="formLabels", nowrap="nowrap")
            if len(date_elements) >= 3:
                ntp_date = date_elements[7].text.strip()
                date_obj = datetime.strptime(ntp_date, '%b %d %Y %I:%M %p')
                formatted_date = date_obj.strftime("%Y/%m/%d")
                ntp_date = formatted_date
                NTP_Date[folder] = ntp_date
            else:
                ntp_date = "Not Found"

            # Find SA Date
            if len(date_elements) >= 4:
                sa_date = date_elements[9].text.strip()
                date_obj = datetime.strptime(sa_date, '%b %d %Y %I:%M %p')
                formatted_date = date_obj.strftime("%Y/%m/%d")
                sa_date = formatted_date
                SA_Completed_Dates[folder] = sa_date
            else:
                sa_date = "Not Found"
            
            # Check "manualPricing
            try:
                manual_pricing_yes = soup.find('input', {'id': 'manualPricingYes'})
                if manual_pricing_yes and manual_pricing_yes.has_attr('checked'):
                    manualPricing = 'Yes'
                else:
                    manualPricing = 'No'
            except:
                manualPricing = "Not Found"
        
            Manual_Pricings[folder] = manualPricing

            # Find Structure Type Report
            # Define regular expressions for the possible patterns
            # Iterate through <td> elements and check if text matches any of the patterns
            try : 
                td_elements = soup.find_all("td")
                found_text = None
                patterns = [re.compile(r'^SA - S'), re.compile(r'^SL - S'), re.compile(r'^MOD')]
                for td in td_elements:
                    text = td.get_text(strip=True)
                    for pattern in patterns:
                        if pattern.search(text):
                            found_text = text
                            break
                    if found_text:
                        break
                if found_text:
                    Report_Types[folder] = found_text
                    
            except :
                Report_Types[folder] = "Not Found"


            #Find Customer   
            try :
                customer = soup.find('div', id='reviewCustomerHighLevelOrg').text.strip()
            except :
                customer = "Not Found"
            Customer[folder] = customer
            
            #Find Status
            try :
                status = soup.find('span', id='presubmittalStatusAppStatus').text.strip()
            except :
                status = "Not Found"
            Statuses[folder] = status

            try :
                # Create a dictionary for the current folder and store its data
                folder_data = {
                    'structure_type': structure_types[folder],
                    'vendor': vendors[folder],
                    'pricing': prices[folder],
                    'application_submited_date': Application_Submited_Dates[folder],
                    'ntp_date': NTP_Date[folder],
                    'sa_date': SA_Completed_Dates[folder],
                    'manualPricing': Manual_Pricings[folder],
                    'report_type' : Report_Types[folder],
                    'customer': Customer[folder],
                    'status': Statuses[folder]
                }

                # Store the folder data in the MetaData dictionary
                MetaData[folder] = folder_data
            except :
                pass

    # Print the MetaData for each folder
    print("--------------------------------------------")
    for folder in valid_folders:
        data = MetaData.get(folder)
        print(f'Folder: {folder}, Structure Type: {data["structure_type"]}, Vendor: {data["vendor"]}, Price: {data["pricing"]}, Application Submit Date: {data["application_submited_date"]}, NTP DATE: {data["ntp_date"]}, SA DATE: {data["sa_date"]}, Manual Pricing: {data["manualPricing"]},Report Type: {data["report_type"]}, Customer: {data["customer"]}, Status: {data["status"]}')
        print("--------------------------------------------")
        time.sleep(0.25)

    # Define the path for saving the JSON file in the "data/summary" folder
    output_dir = 'data/summary'
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    output_path = os.path.join(output_dir, 'metadata.json')

    # Write MetaData to a JSON file in the "data/summary" folder
    with open(output_path, 'w') as json_file:
        json.dump(MetaData, json_file, indent=4)
    print(f"Metadata saved to {output_path}")

    return MetaData


