# CloudLedger

CloudLedger is a command-line inventory for servers you own or are authorized
to manage. It connects to an entered IP address over SSH, reads the server's
operating system and disk information, and saves everything in a local
inventory file. It does not continuously monitor servers; the details are
collected once, when the server is added.

## Setup

Install Python, then install the packages CloudLedger uses:

```sh
python -m pip install -r requirements.txt
```

From the project root, start the app with:

```sh
python src/main.py
```

CloudLedger rejects SSH servers whose host keys are not already trusted. Before
adding a server for the first time, verify its SSH fingerprint with its
administrator and add the trusted host key to your SSH `known_hosts` file.

## Example

When the menu appears, choose **2** to add a server. Enter its IP address,
SSH username, and password when prompted (press Enter if the server uses an
SSH key instead). If the SSH connection succeeds, CloudLedger reads the OS and
disk details and saves the server to the inventory file, `CloudLedger.json`.
Choose **1** to view the inventory or **3** to remove a server.

Example inventory output:

```
Server inventory:
1. IP: 192.168.1.20
   OS: Linux homelab 6.1.0 x86_64 GNU/Linux
   Disk: total 100G 40G 60G 40% -
```

The OS and disk commands (`uname` and `df`) are written for Linux servers.

Only connect to servers you own or are authorized to manage.
