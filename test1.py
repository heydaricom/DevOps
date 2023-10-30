import paramiko

# Get router SSH details from user input
router_ip = input("Enter router IP address: ")
router_username = input("Enter your username: ")
router_password = input("Enter your password: ")
enable_password = input("Enter enable password: ")

# SSH connection setup
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the router
    ssh_client.connect(router_ip, username=router_username, password=router_password)

    # Start an interactive shell session
    ssh_shell = ssh_client.invoke_shell()

    # Send 'enable' command and wait for the 'Password' prompt
    ssh_shell.send("enable\n")
    ssh_shell.recv(1000)  # Wait for the password prompt

    # Send enable password and wait for the prompt
    ssh_shell.send(enable_password + "\n")
    ssh_shell.recv(1000)  # Wait for the command prompt

    # Send command to get configuration
    ssh_shell.send("terminal length 0\n")  # To disable pagination
    ssh_shell.send("show running-config\n")
    
    # Wait for the command to complete (adjust the delay based on your network)
    import time
    time.sleep(10)

    # Read configuration output
    router_config = ssh_shell.recv(65535).decode()

    # Save configuration to a file
    with open("router_config.txt", "w") as config_file:
        config_file.write(router_config)

    print("Router configuration collected and saved successfully.")

except paramiko.AuthenticationException:
    print("Authentication failed, please verify your credentials.")
except paramiko.SSHException as e:
    print("SSH connection failed:", str(e))
finally:
    # Close the SSH connection
    ssh_client.close()
