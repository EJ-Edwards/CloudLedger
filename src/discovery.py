import ipaddress
from getpass import getpass
import paramiko


# Adding the server and discovering potential servers
def add_or_discover_server(inventory):
    while True:
        ip = input("Please enter the IP address of the server: ").strip()
        try:
            ip = str(ipaddress.ip_address(ip))
            break
        except ValueError:
            print("Invalid IP address entered. Please try again.")
    if any(server.get("ip") == ip for server in inventory):
        print(f"Server with IP '{ip}' is already in the inventory.")
        return None
    while True:
        username = input("SSH username: ").strip()
        if username:
            break
        print("A username is required.")
    password = password_prompt()
    
    client = can_scan_server(ip, username, password)
    if client is None:
        return None

    server = {"ip": ip}
    try:
        # Both server.update is used so that way it can collect information on disk info and os info before adding the server to the inventory.
        # The client has to be used before it is closed, so the closing happens in the finally block after the info is collected.
        server.update(disk_info(client) or {})
        server.update(os_info(client) or {})
    finally:
        client.close()

    inventory.append(server)
    print(f"Server with IP '{ip}' added to inventory.")
    return server



# Checking if can server work
def can_scan_server(ip, username, password):
    client = paramiko.SSHClient()
    # The reason why paramiko reject policy is there to ensure that only known and trusted host keys are accepted, preventing man-in-the-middle attacks.
    client.load_system_host_keys()
    # This ensures that a host key is already loaded and there arent any duplicate entries.
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    connected = False

    # rule of try: run the code, if an error occurs run the except
    # rule of except Error: only run if a specified error occurs
    # rule of finally: runs after try and except have run
    # rule of function returns: 
    try:
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

    return None

def password_prompt():
    return getpass("Password (press Enter if there is none): ").strip()

def os_info(client):
    # Trick to remember this std(in will mean sending inputs into a command)
    # Trick to remember this std(out will mean outputs receiving normal output)
    # Trick to remember this std(err) will mean an error output 
    stdin, stdout, stderr = client.exec_command("uname -a")
    # The decode is used to convert bytes into actual text and it strips so it can be seperate removing the whitespace
    output = stdout.read().decode().strip()
    return {"os": output} if output else None

def disk_info(client):
    stdin, stdout, stderr = client.exec_command("df -h --total | grep total")
    # The .decode feature is used to convert bytes into an actual python string
    # The .strip part is used to remove the white spaces so it returns the output clean
    # The .read part is what get retrived from the terminal
    output = stdout.read().decode().strip()
    return {"disk": output} if output else None




if __name__ == "__main__":
    inventory = []
    add_or_discover_server(inventory)
    print(inventory)

