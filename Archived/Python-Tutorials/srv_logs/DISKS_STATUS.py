#!/usr/bin/python3.8

import csv
import subprocess
import re

# List of IP addresses
ip_addresses = [
    "172.27.0.5",
    "172.27.0.6",
    "172.27.0.7",
    "172.27.0.8",
    "172.27.0.11",
    "172.27.0.14",
    "172.27.0.18",
    "172.27.0.35",
    "172.27.0.36",
    "172.27.0.37",
    "172.27.0.38",
    "172.27.0.44",
    "172.27.0.45",
    "172.27.0.47",
    "172.27.0.48" ,
    "172.27.0.130",
    "172.27.0.150",
    "172.27.0.25",
    "172.27.0.26",
    "172.27.0.27",
    "172.27.0.28",
    "172.27.0.46",
    "172.27.0.144", 
    "172.27.0.15",
    "172.27.0.16",
    "172.27.0.17",
    "172.27.0.19"
    ]

# Function to run command and return output
#def run_command(ip, command):
#    result = subprocess.run(['ssh', ip, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#    if result.returncode == 0:
#        return result.stdout
#    else:
#        return result.stderr

# Function to run command and return output
def run_command(ip, command):
    result = subprocess.run(['ssh', 'erpnoc@' + ip, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr



# Function to get RHEL version
def get_rhel_version(ip):
    command = "cat /etc/redhat-release"
    output = run_command(ip, command)
    return output.strip()

# Function to get block storage disks
def get_block_storage(ip):
    command = "lsblk -o NAME,MOUNTPOINT,SIZE | grep -E 'sd|vd|hd'"
    output = run_command(ip, command)
    disks = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            disk_name = parts[0]
            size = parts[2]
            mount_point = parts[1] if len(parts) >= 2 else ""
            disks.append({"disk_name": disk_name, "size": size, "mount_point": mount_point})
    return disks

# Function to get NFS storage
def get_nfs_storage(ip):
    command = "df -hT | grep nfs"
    output = run_command(ip, command)
    nfs_storages = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 6:
            mount_point = parts[6]
            size = parts[2]
            source = parts[0]
            nfs_storages.append({"mount_point": mount_point, "size": size, "source": source})
    return nfs_storages

# List to store server information
server_info = []

# Iterate over IP addresses
for ip in ip_addresses:
    # Get server hostname
    command = "hostname"
    hostname = run_command(ip, command).strip()

    # Get RHEL version
    rhel_version = get_rhel_version(ip)

    # Get block storage disks
    block_storage = get_block_storage(ip)

    # Get NFS storage
    nfs_storage = get_nfs_storage(ip)

    # Calculate total number of block storage disks
    total_disks = len(block_storage)

    # Append server information to list
    server_info.append({
        "Serial Number": "",  # Assuming this is not available via SSH
        "Server Hostname": hostname,
        "RHEL Version": rhel_version,
        "IPv4 Address": ip,
        "Total number of block storage disks": total_disks,
        "Block Storage Disks": block_storage,
        "NFS Storage": nfs_storage
    })

# Write server information to CSV file
with open('server_info.csv', mode='w', newline='') as file:
    fieldnames = ['Serial Number', 'Server Hostname', 'RHEL Version', 'IPv4 Address', 'Total number of block storage disks', 'Block Storage Disks', 'NFS Storage']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for info in server_info:
        writer.writerow(info)

print("Server information saved to server_info.csv")
