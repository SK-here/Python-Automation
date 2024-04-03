#!/bin/python3

import subprocess

# List of host IP addresses
hosts = [
            '172.25.250.11', 
            '172.25.250.12', 
            '172.25.250.13', 
            '172.25.250.14', 
            '172.25.250.15', 
            '172.25.250.16'
        ]

# SSH username and SSH private key path
username = 'admin'
ssh_key = '/home/admin/.ssh/ansible_key'

# Commands to run on each host
check_hostname = 'hostname'
disk_space = 'df -Th'
srv_uptime = 'uptime'
srv_pretty_uptime = 'uptime -p'

hostnames = {}
disk_stats = {}
uptime_servers = {}
pretty_uptime_servers = {}

for host in hosts:
    try:
        # Running commands on each host
        hostname = subprocess.check_output(
            ['ssh', '-i', ssh_key, f'{username}@{host}', check_hostname],
            universal_newlines=True,
            stderr=subprocess.STDOUT
        )
        hostnames[host] = hostname.strip()
        
        disk_space_output = subprocess.check_output(
            ['ssh', '-i', ssh_key, f'{username}@{host}', disk_space],
            universal_newlines=True,
            stderr=subprocess.STDOUT
        )
        disk_stats[host] = disk_space_output.strip()

        uptime_output = subprocess.check_output(
            ['ssh', '-i', ssh_key, f'{username}@{host}', srv_uptime],
            universal_newlines=True,
            stderr=subprocess.STDOUT
        )
        uptime_servers[host] = uptime_output.strip()

        pretty_uptime_output = subprocess.check_output(
            ['ssh', '-i', ssh_key, f'{username}@{host}', srv_pretty_uptime],
            universal_newlines=True,
            stderr=subprocess.STDOUT
        )
        pretty_uptime_servers[host] = pretty_uptime_output.strip()
    except subprocess.CalledProcessError as error:
        hostnames[host] = f"Error: {error.output.strip()}"

# Print the output for each host
for host in hosts:
    print(f"Details for Server {host} are:", end='\n\n')
    print(f"Hostname: {hostnames.get(host, 'Not Available')}", end='\n\n')
 #  print(f"Server uptime: {uptime_servers.get(host, 'Not Available')}", end='\n\n')
    print(f"Server uptime: {pretty_uptime_servers.get(host, 'Not Available')}", end='\n\n')
    print(f"Disk space for {host}: {disk_stats.get(host, 'Not Available')}", end='\n\n')
    print()
