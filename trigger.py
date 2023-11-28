# Josh Brown and Dre Owens
# Fall 2023 - Zak Rubin
# CNE 430

# YouTube to MP3 Converter Trigger Script

import paramiko
import time

def trigger():
    # SSH connection settings
    key_path = "/Users/joshuabrown/Downloads/yt2mp3.pem"
    host = "ec2-34-210-31-250.us-west-2.compute.amazonaws.com"
    username = "ubuntu"

    # Establish SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=username, key_filename=key_path)
        print("Connection successful")

        # Run remote script
        inception(client)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the SSH connection
        client.close()

# Run second script
def inception(ssh_client):
    try:
        # Start an interactive shell
        shell = ssh_client.invoke_shell()

        # Send the command to run the remote script
        command = 'python3 /home/ubuntu/ec2/script.py\n'
        shell.send(command)

        # Wait for a moment to ensure the command is executed
        time.sleep(2)

        # Prompt the user to input a URL
        video_url = input("Enter video URL: ")
        shell.send(video_url + '\n')

        # Wait for a moment to ensure the URL is processed
        time.sleep(2)

        # Read the output of the remote script in a loop until it completes
        while not shell.exit_status_ready():
            output = shell.recv(4096).decode('utf-8', 'ignore')
            if output:
                print(output)

        # Close the interactive shell
        shell.close()

    except Exception as e:
        print(f"Error running remote script: {e}")

if __name__ == "__main__":
    trigger()