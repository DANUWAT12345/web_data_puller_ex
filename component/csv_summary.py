def csv_summary() :

    import os
    import csv
    import json

    # Load the JSON data
    with open('data/summary/metadata.json', 'r') as json_file:
        metadata = json.load(json_file)

    # Define the output CSV file path
    csv_file_path = 'data/summary/Metadata.csv'

    # Define the CSV headers
    csv_headers = ["BU", "APP", "Structure Type", "Vendor", "Pricing", "Application_Submitted_Date", "NTP_Date", "SA_Date", "Report Type", "ManualPricing", "Customer", "Status"]

    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader()

        # Write each row to the CSV file
        for key, data in metadata.items():
            # Split the key into BU and APP
            bu, app = key.split('.')
            
            writer.writerow({
                "BU": bu,
                "APP": app,
                "Structure Type": data["structure_type"],
                "Vendor": data["vendor"],
                "Pricing": data["pricing"],
                "Application_Submitted_Date": data["application_submited_date"],
                "NTP_Date": data["ntp_date"],
                "SA_Date": data["sa_date"],
                "Report Type": data["report_type"],
                "ManualPricing": data["manualPricing"],
                "Customer": data["customer"],
                "Status": data["status"]
            })
    print(f"********************************")
    print(f"Data saved to {csv_file_path}")
    print(f"********************************")

