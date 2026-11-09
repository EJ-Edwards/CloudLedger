import discovery
import data
import credits


def show():
    print("Welcome to CloudLedger")

    while True:
        print("\n===== CloudLedger =====")
        print("1. View Inventory")
        print("2. Add / Discover Server")
        print("3. Remove Server")
        print("4. Credits")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print("\nViewing server inventory...")
            data.show_inventory()

        elif choice == "2":
            print("\nOpening server registration...")
            server = discovery.add_or_discover_server(data.inventory)
            if server:
                data.save_to_file(data.inventory)
    
        elif choice == "3":
            if data.remove_server(data.inventory):
                data.save_to_file(data.inventory)

        elif choice == "4":
            print("\nShowing credits...")
            credits.show()

        elif choice == "5":
            print("\nExiting CloudLedger. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select an option from 1-5.")
