import paramiko
import string
import random

# Function to generate a strong random password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# List of commands to disable Telnet, HTTP, FTP and enable SSH with strong password
commands = [
    "no service telnet",
    "no ip http server",
    "no ip http secure-server",
    "no ip ftp server",
    "ip ssh version 2",  # Enable SSHv2
    "ip ssh authentication-retries 3",  # Limit SSH login attempts
    "ip ssh time-out 60",  # Set SSH timeout to 60 seconds
    "ip ssh pubkey-chain",
]

# Ask user for device details
device_ip = input("Enter device IP: ")
ssh_username = input("Enter SSH username: ")
ssh_password = input("Enter SSH password (or leave empty to generate a strong password): ")

# Generate a strong random password if not provided by the user
if not ssh_password:
    ssh_password = generate_strong_password()
    print(f"Generated strong SSH password: {ssh_password}")

try:
    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device_ip, username=ssh_username, password=ssh_password, timeout=10)

    print(f"Connected to {device_ip}")

    # Send commands to the device
    for command in commands:
        ssh.exec_command(command)
        print(f"Executed: {command}")

    # Close SSH connection
    ssh.close()

except Exception as e:
    print(f"Failed to connect to {device_ip}: {e}")
