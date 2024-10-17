import os
import tkinter as tk
from tkinter import messagebox, filedialog
import shutil

class CSVFileSelector:

    csv_file_selected = False  # Define csv_file_selected as a class attribute

    def __init__(self):
        self.file_path = None  # Initialize the file_path attribute

        # Create the main window
        self.root = tk.Tk()
        self.root.title("CCI Puller")

        # Create a label with a more aesthetic style
        label = tk.Label(self.root, text="Please select .csv input file.", font=("Helvetica", 14))
        label.pack(padx=20, pady=10)

        # Create a button to select a CSV file
        csv_button = tk.Button(self.root, text="Select CSV File", command=self.select_csv_file, font=("Helvetica", 12))
        csv_button.pack(padx=20, pady=10)

        # Create a frame for csv_path_label to add a border
        csv_path_frame = tk.Frame(self.root, borderwidth=2, relief="solid")
        csv_path_frame.pack(padx=20, pady=10)
        self.csv_path_label = tk.Label(csv_path_frame, text="", font=("Helvetica", 12))
        self.csv_path_label.pack(padx=10, pady=5)

        # Create a label with a more aesthetic style
        label = tk.Label(self.root, text="Before starting the program, would you like to clear all folders in /data?", font=("Helvetica", 14))
        label.pack(padx=20, pady=10)

        # Create a frame for the delete and start buttons to be on the same line
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        # Create a button to trigger deletion
        delete_button = tk.Button(button_frame, text="Delete Folders", command=self.confirm_delete, bg="red", fg="white", font=("Helvetica", 12))
        delete_button.pack(side="left", padx=10, pady=10)

        # Create a button to start the program without deletion
        start_button = tk.Button(button_frame, text="No & Keep All", command=self.start, bg="green", fg="white", font=("Helvetica", 12))
        start_button.pack(side="left", padx=10, pady=10)

    # Function to select a CSV file
    def select_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_path_label.config(text=f"Selected CSV File: {file_path}")
            self.csv_file_selected = True
            self.file_path = file_path

    # Function to delete folders
    def delete_folders(self):
        if not self.csv_file_selected:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return

        try:
            for root, dirs, files in os.walk('data'):
                for dir in dirs:
                    folder_path = os.path.join(root, dir)
                    shutil.rmtree(folder_path)
            print("All folders have been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to confirm deletion
    def confirm_delete(self):
        if not self.csv_file_selected:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return
        user_response = messagebox.askyesno("Confirmation", "Do you want to delete all folders in /data before starting the program?")
        if user_response:
            self.delete_folders()
            self.root.destroy()  # Close the main window
        else:
            print("Cancelled", "No folders in /data were deleted. Program execution continues.")

    # Function to start the program without deletion
    def start(self):
        if not self.csv_file_selected:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return
        print("Continuing", "No folders in /data were deleted. The program will start without deletion.")
        self.root.destroy()  # Close the main window

    # Function to run the GUI
    def run(self):
        self.root.mainloop()
