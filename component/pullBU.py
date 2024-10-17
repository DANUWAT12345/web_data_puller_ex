def pullBU_APP(file_path_CSV) :

    import csv
    import tkinter as tk
    from tkinter import filedialog

    # Create a simple tkinter window for file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask the user to select a CSV file
    csv_file_path = file_path_CSV

    # Check if the user canceled the file dialog
    if not csv_file_path:
        print("File selection canceled.")
    else:
        try:
            # Open the selected CSV file for reading
            with open(csv_file_path, 'r', newline='') as csv_file:
                # Create a CSV reader
                csv_reader = csv.DictReader(csv_file)

                # Initialize an empty list to store dictionaries
                data = []

                # Iterate over each row in the CSV file
                for row in csv_reader:
                    # Append each row (as a dictionary) to the list
                    data.append(row)

            BU_APP = data

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return(BU_APP)