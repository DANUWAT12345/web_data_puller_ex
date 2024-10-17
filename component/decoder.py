def decoder() : 
    import base64

    # Define the path to the login.txt file
    file_path = 'info/login.txt'  # Adjust the path as needed

    # Initialize variables to store the decoded username and password
    decoded_username = ""
    decoded_password = ""

    # Open the file for reading
    with open(file_path, 'r') as file:
        # Read the lines from the file
        lines = file.readlines()

        # Extract the encoded username and password
        encoded_username = lines[0].split(': ')[1].strip()
        encoded_password = lines[1].split(': ')[1].strip()

        # Decode the values
        decoded_username = base64.b64decode(encoded_username).decode()
        decoded_password = base64.b64decode(encoded_password).decode()

    return decoded_username, decoded_password