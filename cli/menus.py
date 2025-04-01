# menus.py
# cli/menus.py (update your existing menu)
def display_main_menu():
    print("\n=== INVENTORY MANAGEMENT SYSTEM ===")
    print("1. Product Management")
    print("2. Category Management")
    print("3. Transaction Management")  # New option
    print("4. Supplier Management")     # Will add later
    print("5. Stock Alerts")            # Will add later
    print("0. Exit")
    return input("Select an option: ")

def transaction_menu(session):
    while True:
        print("\n=== TRANSACTION MANAGEMENT ===")
        print("1. List All Transactions")
        print("2. Add New Transaction")
        print("3. Delete Transaction")
        print("0. Back to Main Menu")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            list_transactions(session)
        elif choice == "2":
            add_transaction(session)
        elif choice == "3":
            delete_transaction(session)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")

# Update your main menu handler to include the transaction menu
def handle_main_menu(choice, session):
    if choice == "1":
        product_menu(session)
    elif choice == "2":
        category_menu(session)
    elif choice == "3":
        transaction_menu(session)  # New option
    elif choice == "4":
        # Will implement supplier_menu later
        print("Supplier Management coming soon!")
    elif choice == "5":
        # Will implement alerts_menu later
        print("Stock Alerts coming soon!")
    elif choice == "0":
        print("Exiting program. Goodbye!")
        return False
    else:
        print("Invalid option. Please try again.")
    
    return True