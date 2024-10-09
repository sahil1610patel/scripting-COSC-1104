# Author: Sahil Patel
# Date: 2024/10/08
# Description: creation of a simulated cloud storage tracking system.

# Lists to store user data
account_names = []
storage_capacity = []
occupied_storage = []

def register_account(name, capacity):
    # Check if username is unique and not blank, and if storage is positive
    if name == "" or name in account_names:
        print("Account name must be unique and non-blank.")
        return False
    if capacity <= 0:
        print("Storage capacity must be a positive number.")
        return False
    # Add user information to lists
    account_names.append(name)
    storage_capacity.append(capacity)
    occupied_storage.append(0)
    print(f"Account for {name} created with {capacity} MB of storage.")
    return True

def remove_account(name):
     # Check if the user exists
    if name not in account_names:
        print("Account not found.")
        return False
    # Remove user from lists
    idx = account_names.index(name)
    account_names.pop(idx)
    storage_capacity.pop(idx)
    occupied_storage.pop(idx)
    print(f"Account for {name} has been deleted.")
    return True

def upload_document(name, doc_name, doc_size):
    # Check if the user exists and has enough available storage
    if name not in account_names:
        print("Account not found.")
        return False
    idx = account_names.index(name)
    if occupied_storage[idx] + doc_size > storage_capacity[idx]:
        print("Not enough storage available.")
        return False
    # Update the used storage
    occupied_storage[idx] += doc_size
    print(f"Document '{doc_name}' uploaded. {doc_size} MB used.")
    return True

def show_accounts():
      # Display all current accounts and their storage usage
    if not account_names:
        print("No accounts to display.")
        return
    print("\n--- Current Accounts ---")
    for i in range(len(account_names)):
        print(f"Account Name: {account_names[i]}, Available: {storage_capacity[i]} MB, Used: {occupied_storage[i]} MB")
    print("------------------------")

def execute():
    # Main menu loop
    while True:
        print("\n--- Cloud Storage Management System ---")
        print("1. Register Account")
        print("2. Remove Account")
        print("3. Upload Document")
        print("4. Show Accounts")
        print("5. Exit")
         # Request user choice and validate input
        try:
            selection = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number between 1 and 5.")
            continue
        
        if selection == 1:
            # Create Account
            user_id = input("Enter account name: ")
            try:
                capacity = int(input("Enter storage size (in MB): "))
            except ValueError:
                print("Storage size must be a positive number.")
                continue
            register_account(user_id, capacity)
            
        elif selection == 2:
            # Delete Account
            user_id = input("Enter username to delete: ")
            remove_account(user_id)
        
        elif selection == 3:
            # Upload File
            user_id = input("Enter username: ")
            document_name = input("Enter filename: ")
            try:
                document_size = int(input("Enter file size (in MB): "))
            except ValueError:
                print("File size must be a positive number.")
                continue
            upload_document(user_id, document_name, document_size)
        
        elif selection == 4:
            # Display Accounts
            show_accounts()
        
        elif selection == 5:
            # Exit
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please select a number between 1 and 5.")

# Run the program
execute()