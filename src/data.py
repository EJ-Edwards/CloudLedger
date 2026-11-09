import json
from pathlib import Path


# Path to the JSON file where the inventory is stored
DATA_FILE = Path(__file__).resolve().parent.parent / "CloudLedger.json"


# This function is supposed to show the inventory
def show_inventory():
    # If the list is empty there is nothing to show so it prints a message and stops.
    if not inventory:
        print("Inventory is empty.")
        return
    print("\nServer inventory:")
    # The enumerate with start=1 numbers the servers starting at 1 instead of 0 so it looks normal to the user.
    for index, item in enumerate(inventory, start=1):
        # The .get is used so that way if the ip is missing it shows Unknown instead of crashing.
        print(f"{index}. IP: {item.get('ip', 'Unknown')}")
        # Older servers saved before the os and disk info was added do not have them so it skips the line if they are missing.
        if item.get("os"):
            print(f"   OS: {item['os']}")
        if item.get("disk"):
            print(f"   Disk: {item['disk']}")


# This is for removing the server from the inventory
def remove_server(servers):
    if not servers:
        print("Inventory is empty.")
        return False

    for index, server in enumerate(servers, start=1):
        print(f"{index}. {server.get('ip', 'Unknown')}")

    selection = input("Enter the number of the server to remove: ").strip()
    # This checks that it is a number first and then that it is in the range of the list so bad input can not crash int() or pop().
    if not selection.isdigit() or not 1 <= int(selection) <= len(servers):
        print("Invalid server number. No server was removed.")
        return False

    # The minus 1 is there because the user counts from 1 but the list counts from 0.
    removed = servers.pop(int(selection) - 1)
    print(f"Server '{removed.get('ip', 'Unknown')}' removed from inventory.")
    # This returns True so the menu knows something changed and it needs to save.
    return True

# This is to save a file and to save the IPs listed
def save_to_file(servers, filename=DATA_FILE):
    try:
        # The with closes the file automatically even if an error happens and the "w" means it overwrites the old file.
        with Path(filename).open("w", encoding="utf-8") as file:
            # The json.dump writes the list to the file and the indent=4 makes it easy to read.
            json.dump(servers, file, indent=4)
    except OSError as error:
        print(f"Could not save inventory: {error}")
    # The else only runs if the try worked so it never says saved after a failure.
    else:
        print("Inventory saved.")

# This is to load a file with all the servers listed
def load_from_file(filename=DATA_FILE):
    path = Path(filename)
    # The first time the program runs there is no file yet so it just starts with an empty inventory.
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            servers = json.load(file)
    # The JSONDecodeError happens when the file is broken or is not real json.
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load saved inventory: {error}")
        return []

    # This checks that the file is a list and that every item is a dictionary with an ip that is a string before trusting it.
    if not isinstance(servers, list) or not all(
        isinstance(server, dict) and isinstance(server.get("ip"), str)
        for server in servers
    ):
        print("Saved inventory has an invalid format. Starting with an empty inventory.")
        return []
    return servers


# This loads the saved servers one time when the file is imported, and menu.py and discovery.py share this same list.
inventory = load_from_file()