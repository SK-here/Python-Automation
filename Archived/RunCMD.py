'''
@Author: Saksham (SK) Trivedi
@Description: A Python Script to run single command on a multiple nodes
'''

import paramiko
import getpass

def execute_command_on_ip(ip, username, password, command):
    print(f"Connecting to {ip}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        result = {
            'stdout': stdout.read().decode('utf-8'),
            'stderr': stderr.read().decode('utf-8')
        }
    except Exception as e:
        result = {
            'stdout': '',
            'stderr': str(e)
        }
    finally:
        ssh.close()
    return result

def main():
    # List of IPs provided in the code
    ip_list = [
                '192.168.45.10',
                '192.168.45.20',
                '192.168.45.12'
                #... list goes on
            ]   
    
    # Username
    username = input("Enter SSH Username: ")
    
    # Command to run
    command = input(f"Enter the command to execute:\n")  

    for ip in ip_list:
        print('------------------------------------------------------------------------------')
        password = getpass.getpass(f"Enter your SSH password for {ip}: ")
        result = execute_command_on_ip(ip, username, password, command)

        print(f"\nResults for {ip}:")
        print("STDOUT:")
        print(result['stdout'])
        print("STDERR:")
        print(result['stderr'])

if __name__ == "__main__":
    main()
