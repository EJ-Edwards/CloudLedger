import ipaddress
from getpass import getpass
from pathlib import Path
import paramiko
from data import inventory


# Path to the known hosts file for storing SSH host keys.
HOST_KEYS_FILE = Path.home() / ".ssh" / "cloudledger_known_hosts"


# This is so the user can confirm the authenticity of their server host key before connection.
class ConfirmMissingHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    
    # This method is called when the host key is missing. It asks the user to confirm the authenticity of the host key.
    def missing_host_key(self, client, hostname, key):
        print(f"Missing host key for {hostname}")
        fingerprint = key.get_fingerprint().hex(":").upper()

        # This prints a message to inform the user that the host key is missing and needs confirmation.
        print(f"\nThe authenticity of host '{hostname}' can't be established.")
        print(f"SSH key type: {key.get_name()}")
        print(f"SSH fingerprint (MD5): {fingerprint}")
        
        # This asks the user whether they want to trust the server.
        answer = input("Are you sure you want to continue connecting (yes/no)? ").strip().lower()

        # If the user says yes then the host key is added to known hosts.
        if answer == "yes":
            client.get_host_keys().add(hostname, key.get_name(), key)
            # This ensures that the directory for the known hosts file exists before saving the host key.
            HOST_KEYS_FILE.parent.mkdir(parents=True, exist_ok=True)
            client.save_host_keys(str(HOST_KEYS_FILE))
            print("Host key accepted.")
        else:
            raise paramiko.SSHException("Host key was not accepted.")
        
        
# Adding the server and discovering potential servers
def add_or_discover_server(inventory):
    while True:
        ip = input("Please enter the IP address of the server: ").strip()
        try:
            # This checks if the IP address is valid by attempting to create an IP address object.
            ip = str(ipaddress.ip_address(ip))
            break
        except ValueError:
            print("Invalid IP address entered. Please try again.")

    # This keeps asking for the username until the user types something so it can not be empty.
    while True:
        username = input("SSH username: ").strip()
        if username:
            break
        print("A username is required.")

    # This function is for the user to enter the SSH port number for the server, with a default of 22 if left blank.
    while True:
        try:
            port = int(input("Enter the port number (default 22): ").strip() or 22)

            if 1 <= port <= 65535:
                break

            print("Port number must be between 1 and 65535.")

        except ValueError:
            print("Invalid port number. Please enter a valid integer.")

    # This checks if there is a duplicate server with the same IP and port in the inventory.
    if any(
        server.get("ip") == ip and server.get("port", 22) == port
        for server in inventory
    ):
        print(f"Server with IP '{ip}' and port '{port}' is already in the inventory.")
        # This tells the menu that nothing was added.
        return None

    password = password_prompt()

    # This attempts to connect to the server by using the IP, username, password, and port provided by the user.
    client = can_scan_server(ip, username, password, port)

    # If it failed then it can not proceed with adding the server and will return it failed.
    if client is None:
        return None

    # The server starts out with only the IP and port, and then the disk and OS info get added to it.
    server = {"ip": ip, "port": port}

    try:
        # Both server.update is used so that way it can collect information on disk info and os info before adding the server to the inventory.
        # The client has to be used before it is closed, so the closing happens in the finally block after the info is collected.

        disk = disk_info(client)
        os = os_info(client)

        # The functions are only called once, and their returned dictionaries are reused here.
        if disk:
            server.update(disk)
        else:
            print("No disk info found.")

        if os:
            server.update(os)
        else:
            print("No OS info found.")

    finally:
        client.close()

    # This is where the server gets added to the inventory list, the menu is what saves it to the file after.
    inventory.append(server)
    print(f"Server with IP '{ip}' added to inventory.")
    return server


# Checking if can server work
def can_scan_server(ip, username, password, port):
    # This creates the SSH client that is used to connect to the server.
    client = paramiko.SSHClient()

    # This line is responsible for loading known host keys from the user's system.
    client.load_system_host_keys()

    # This loads host keys that were previously accepted by CloudLedger.
    if HOST_KEYS_FILE.exists():
        client.load_host_keys(str(HOST_KEYS_FILE))

    # This tells paramiko what to do when the server's host key is not already known, it calls my ConfirmMissingHostKeyPolicy class so the user can confirm it.
    client.set_missing_host_key_policy(ConfirmMissingHostKeyPolicy())

    # This starts as False and only turns True when the connection works, the finally block uses it to know if it should close the client.
    connected = False

    # rule of try: run the code, if an error occurs run the except
    # rule of except Error: only run if a specified error occurs
    # rule of finally: runs after try and except have run
    # rule of function returns:
    try:
        # The timeout=5 means it gives up after 5 seconds so the program does not hang on a server that is off.
        client.connect(
            hostname=ip,
            username=username,
            password=password or None,
            port=port,
            timeout=5,
        )
        
        print(f"Connected to {ip}.")
        connected = True
        return client

    except paramiko.AuthenticationException:
        print("Wrong username or password.")

    except paramiko.SSHException as error:
        print(f"SSH connection failed: {error}")

    except OSError:
        print("Could not reach the server (is SSH turned on?).")

    finally:
        # On success the caller still needs the open connection, so only close it when the connection failed.
        if not connected:
            client.close()

    # If it got here the connection failed so it returns None.
    return None


# getpass is used so the password does not show on the screen and it never gets saved to the json file.
def password_prompt():
    # This tells the user to enter the password for the server and if there isnt one they just press Enter.
    return getpass("Password (press Enter if there is none): ").strip()


# This gets the operating system info from the server.
def os_info(client):
    # exec_command runs the command on the server, uname -a shows the kernel name, version and architecture.
    # Trick to remember this stdin will mean sending inputs into a command
    # Trick to remember this stdout will mean outputs receiving normal output
    # Trick to remember this stderr will mean error output
    stdin, stdout, stderr = client.exec_command("uname -a")

    # The decode is used to convert bytes into actual text and it strips so it can be separated, removing the whitespace.
    output = stdout.read().decode().strip()

    # If there is output it returns it as a dictionary and if there is none it returns None.
    return {"os": output} if output else None


# This gets the disk info from the server.
def disk_info(client):
    # The -h makes the sizes readable like 50G, the --total adds a total row, and the grep total only keeps that row.
    stdin, stdout, stderr = client.exec_command("df -h --total | grep total")

    # The .decode feature is used to convert bytes into an actual Python string.
    # The .strip part is used to remove the white spaces so it returns the output clean.
    # The .read part is what gets retrieved from the terminal.
    output = stdout.read().decode().strip()

    # If there is output it returns it as a dictionary and if there is none it returns None.
    return {"disk": output} if output else None


# This only runs when this file is run directly and not when it is imported, so it is a quick way to test it.
if __name__ == "__main__":
    inventory = []
    add_or_discover_server(inventory)
    print(inventory)
