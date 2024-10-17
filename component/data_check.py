def data_check() :

    import os

    # Specify the path where you want to count files
    path = 'data'  # Update with your desired path

    # Initialize lists to store folder names with different file counts
    valid_folders = []
    invalid_folders_no_WO = []
    invalid_folders_AB = []
    invalid_folders_errorsearch = []
    invalid_folders_Unknow = []
    invalid_folders_storage = []
    
    # Iterate through the folders in the specified path
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        
        # Check if the item in the path is a directory
        if os.path.isdir(folder_path):
            # Count the number of files in the folder
            file_count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
            if file_count == 4 or file_count == 5 :
                if file_count == 4 :
                    valid_folders.append(folder_name)
                elif file_count == 5 :
                    invalid_folders_storage.append(folder_name)
            elif file_count == 2:
                invalid_folders_no_WO.append(folder_name)
            elif file_count == 1:
                invalid_folders_AB.append(folder_name)
            elif file_count == 0:
                invalid_folders_errorsearch.append(folder_name)
            else :
                invalid_folders_Unknow.append(folder_name)


    # Print the list of valid folder names
    print("***********************")
    print("SUMMARY REPORT FOR DATA VALIDATION")
    print("***********************")
    print("STATUS OK : BU.APP with WO:")
    for folder_name in valid_folders:
        print(folder_name)
    print("***********************")
    #for no WO
    print("STATUS ERROR-1 : BU.APP with no WO")
    for folder_name in invalid_folders_no_WO:
        print(folder_name)
    print("***********************")
    #for A&B Structure
    print("STATUS ERROR-2 : BU.APP with A&B Structure")
    for folder_name in invalid_folders_AB:
        print(folder_name)
    print("***********************")
    #for error search
    print("STATUS ERROR-3 : BU.APP with search error")
    if len(invalid_folders_errorsearch) > 0 :
        for folder_name in invalid_folders_errorsearch:
            print(folder_name)
        print("***********************")
    else :
        print("NOT FOUND")
        print("***********************")
    #for Unknow Error
    print("STATUS ERROR-4 : BU.APP with unknow problem")
    if len(invalid_folders_Unknow) > 0 :
        for folder_name in invalid_folders_Unknow:
            print(folder_name)
        print("***********************")
    else :
        print("NOT FOUND")
        print("***********************")
    print("<--BU.APPKeep from Previous-->")
    #for Previous Storage
    if len(invalid_folders_storage) > 0 :
        for folder_name in invalid_folders_storage:
            print(folder_name)
        print("<------------------------>")
    else :
        print("NOT FOUND")
        print("<------------------------>")

    return valid_folders, invalid_folders_no_WO, invalid_folders_AB, invalid_folders_errorsearch, invalid_folders_Unknow, invalid_folders_storage




