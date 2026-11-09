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
    
    if not can_scan_server(ip, username, password):
        return None
    
    server = {"ip": ip}
    inventory.append(server)
    print(f"Server with IP '{ip}' added to inventory.")
    return server



# Checking if can server work
def can_scan_server(ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # rule of try: run the code, if an error occurs run the except
    # rule of except Error: only run if a specified error occurs
    # rule of finally: runs after try and except have run
    # rule of function returns: 

    try:
        client.connect(ip, username=username, password=password or None, timeout=5)
        print(f"Connected to {ip}.")
        return True
    except paramiko.AuthenticationException:
        print("Wrong username or password.")
    except paramiko.SSHException as error:
        print(f"SSH connection failed: {error}")
    except OSError:
        print("Could not reach the server (is SSH turned on?).")
    finally:
        client.close()

    return False

def password_prompt():
    return getpass("Password (press Enter if there is none): ").strip()

# Adding the gigabytes 
def gigabyte_and_bytes(gb):
    return gb * 1024 * 1024 * 1024

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

