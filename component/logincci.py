def decoder() : 
    
    import base64

    try :
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

    except Exception as e:
        return None, None  # Return None values to indicate failure

def loginprocess(decoded_username, decoded_password): 
     
    import tkinter as tk
    import os
    import base64

    #Generate GUI 
    def GUIcreate(decoded_username, decoded_password) :

        #FOR SUBMIT BOTTON
        def Submit():
                global global_username, global_password
                username = username_var.get()
                password = password_var.get()
                global_username = username
                global_password = password
                # Encode username and password in base64
                encoded_username = base64.b64encode(username.encode()).decode()
                encoded_password = base64.b64encode(password.encode()).decode()

                #save info in \info
                data_dir = 'info'
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                login_file_path = os.path.join(data_dir, 'login.txt')
                
                with open(login_file_path, 'w') as login_file:
                    login_file.write(f'Encoded Username: {encoded_username}\n')
                    login_file.write(f'Encoded Password: {encoded_password}\n')

                root.destroy()
                

        root = tk.Tk()
        root.title("Login")
        font = ('Helvetica', 14)

        welcome_label = tk.Label(root, text="Please input your username and password:", font=font)
        welcome_label.pack()

        username_label = tk.Label(root, text="Username:", font=font)
        username_label.pack()
        username_var = tk.StringVar()
        username_var.set(decoded_username)
        username_entry = tk.Entry(root, textvariable=username_var, font=font)
        username_entry.pack()

        password_label = tk.Label(root, text="Password:", font=font)
        password_label.pack()
        password_var = tk.StringVar()
        password_var.set(decoded_password)
        password_entry = tk.Entry(root,show='*' ,textvariable=password_var, font=font)
        password_entry.pack()

        submit_button = tk.Button(root, text="Submit", command=Submit, font=font)
        submit_button.pack()

        root.geometry("400x250")
        root.mainloop()


    #____________execute start here__________________________#

    # Define the path to the login.txt file
    login_file_path = os.path.join('info', 'login.txt')

    # Check if the file exists
    if os.path.exists(login_file_path):
        decoded_username, decoded_password = decoder()
        GUIcreate(decoded_username, decoded_password)
        decoded_username, decoded_password = decoder()
    else:
        GUIcreate('','')
        decoded_username, decoded_password = decoder()
    
    return decoded_username, decoded_password