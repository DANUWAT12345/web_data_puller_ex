def combine_html(valid_folder):

    import os

    # Directory where the folders are located
    html_directory = 'data'  # Update with the correct directory path

    # List of folder names
    folder_names = valid_folder  # Update with the correct folder names

    # Loop through the folder names
    for folder_name in folder_names:
        folder_path = os.path.join(html_directory, folder_name)
        
        # Create a list to store HTML file names within the folder
        html_file_names = os.listdir(folder_path)
        
        # Create an empty string to store the combined HTML content
        combined_html = ""
        
        # Loop through the first 3 HTML files in the folder and concatenate their content
        for html_file_name in html_file_names[:4]:
            file_path = os.path.join(folder_path, html_file_name)
            with open(file_path, 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()
                combined_html += html_content
        
        # Specify the filename for the combined HTML file within the folder
        combined_html_filename = os.path.join(folder_path, f"{folder_name} combined.html")
        
        # Write the combined HTML content to the new HTML file within the folder
        with open(combined_html_filename, 'w', encoding='utf-8') as combined_html_file:
            combined_html_file.write(combined_html)

    print(f"All HTML files  folder have been combined.")
