import ipaddress
from getpass import getpass
import paramiko


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

    # This checks if there is a duplicate server with the same IP in the inventory.
    if any(server.get("ip") == ip for server in inventory):
        print(f"Server with IP '{ip}' is already in the inventory.")
       # This tells the menu that nothing was added.
        return None
    # This keeps asking for the username until the user types something so it can not be empty.
    while True:
        username = input("SSH username: ").strip()
        if username:
            break
        print("A username is required.")
    password = password_prompt()

    # This attemps to connect to the server by using the IP, username, and password provided by the user.
    client = can_scan_server(ip, username, password)
    
    # If it failed then it can not proceed with adding the server and will return it failed.
    if client is None:
        return None

    # The server starts out with only the IP and then the disk and OS info get added to it.
    server = {"ip": ip}
    try:
        # Both server.update is used so that way it can collect information on disk info and os info before adding the server to the inventory.
        # The client has to be used before it is closed, so the closing happens in the finally block after the info is collected.
        
        # The curly braces are used to create a dictionary to update the server information with disk and OS info.
        # The reason why or {} is to ensure that if the function returns None it can not cause an error when updating the server dictionary.
        server.update(disk_info(client) or {})
        server.update(os_info(client) or {})
    finally:
        client.close()

    # This is where the server gets added to the inventory list, the menu is what saves it to the file after.
    inventory.append(server)
    print(f"Server with IP '{ip}' added to inventory.")
    return server



# Checking if can server work
def can_scan_server(ip, username, password):
    # This creates the SSH client that is used to connect to the server.
    client = paramiko.SSHClient()
    # The reason why paramiko reject policy is there to ensure that only known and trusted host keys are accepted, preventing man-in-the-middle attacks.
    client.load_system_host_keys()
    # This loads ssh host keys from the user's known hosts file. 
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    # This starts as False and only turns True when the connection works, the finally block uses it to know if it should close the client.
    connected = False

    # rule of try: run the code, if an error occurs run the except
    # rule of except Error: only run if a specified error occurs
    # rule of finally: runs after try and except have run
    # rule of function returns: 
    try:
        # The timeout=5 means it gives up after 5 seconds so the program does not hang on a server that is off.
        client.connect(ip, username=username, password=password or None, timeout=5)
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
    # This tells the user to neter the password for the server and if there isnt none they just press enter.
    return getpass("Password (press Enter if there is none): ").strip()

# This gets the operating system info from the server.
def os_info(client):
    # exec_command runs the command on the server, uname -a shows the kernel name, version and architecture.
    # Trick to remember this std(in will mean sending inputs into a command)
    # Trick to remember this std(out will mean outputs receiving normal output)
    # Trick to remember this std(err) will mean an error output 
    stdin, stdout, stderr = client.exec_command("uname -a")
    # The decode is used to convert bytes into actual text and it strips so it can be seperate removing the whitespace
    output = stdout.read().decode().strip()
    # If there is output it returns it as a dictionary and if there is none it returns None.
    return {"os": output} if output else None

# This gets the disk info from the server.
def disk_info(client):
    # The -h makes the sizes readable like 50G, the --total adds a total row, and the grep total only keeps that row.
    stdin, stdout, stderr = client.exec_command("df -h --total | grep total")
    # The .decode feature is used to convert bytes into an actual python string
    # The .strip part is used to remove the white spaces so it returns the output clean
    # The .read part is what get retrived from the terminal
    output = stdout.read().decode().strip()
    # If there is output it returns it as a dictionary and if there is none it returns None.
    return {"disk": output} if output else None




# This only runs when this file is ran directly and not when it is imported, so it is a quick way to test it.
if __name__ == "__main__":
    inventory = []
    add_or_discover_server(inventory)
    print(inventory)

