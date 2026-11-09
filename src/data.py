import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "CloudLedger.json"


# This function is supposed to show the inventory
def show_inventory():
    if not inventory:
        print("Inventory is empty.")
        return
    print("\nServer inventory:")
    for index, item in enumerate(inventory, start=1):
        print(f"{index}. IP: {item.get('ip', 'Unknown')}")
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
    if not selection.isdigit() or not 1 <= int(selection) <= len(servers):
        print("Invalid server number. No server was removed.")
        return False

    removed = servers.pop(int(selection) - 1)
    print(f"Server '{removed.get('ip', 'Unknown')}' removed from inventory.")
    return True

# This is to save a file and to save the IPs listed
def save_to_file(servers, filename=DATA_FILE):
    try:
        with Path(filename).open("w", encoding="utf-8") as file:
            json.dump(servers, file, indent=4)
    except OSError as error:
        print(f"Could not save inventory: {error}")
    else:
        print("Inventory saved.")

# This is to load a file with all the servers listed
def load_from_file(filename=DATA_FILE):
    path = Path(filename)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            servers = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load saved inventory: {error}")
        return []

    if not isinstance(servers, list) or not all(
        isinstance(server, dict) and isinstance(server.get("ip"), str)
        for server in servers
    ):
        print("Saved inventory has an invalid format. Starting with an empty inventory.")
        return []
    return servers


inventory = load_from_file()