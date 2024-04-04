#!/bin/python3

import subprocess
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# List of host IP addresses
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
# username = 'erpnoc'
# ssh_key = '/home/admin/.ssh/id_rsa'

# SSH username and SSH private key path
username = 'admin'
ssh_key = '/home/admin/.ssh/ansible_key'


# Commands to run on each host
check_hostname = 'hostname'
disk_space = 'echo "$(df -Th)" '
srv_uptime = 'uptime'
srv_pretty_uptime = 'echo `(uptime -p)` '

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

# Create message content with server details
msg_content = ''
for host in hosts:
    msg_content += f'-------------------------------------------------------------------------------------------\n'
    msg_content += f"Details for Server {host} are:\n\n"
    msg_content += f"Hostname: {hostnames.get(host, 'Not Available')}\n\n"
    msg_content += f"Server uptime: {uptime_servers.get(host, 'Not Available')}\n\n"
    msg_content += f"Server uptime: {pretty_uptime_servers.get(host, 'Not Available')}\n\n"
    msg_content += f"Disk space for {host}: {disk_stats.get(host, 'Not Available')}\n\n\n"

# Store the output in a log file
log_dir = './daily-logs'
log_file = f"{datetime.now().strftime('%d-%m-%Y')}.log"
log_path = os.path.join(log_dir, log_file)

os.makedirs(log_dir, exist_ok=True)
with open(log_path, 'w') as f:
    f.write(msg_content)

# Set up email message
msg = EmailMessage()
msg['Subject'] = 'Server Details Report'
msg['From'] = os.environ.get('EMAIL_USER')
msg['To'] = 'trivedianuj171@gmail.com'
msg['Cc'] = ['trivedisaksham@gmail.com', 'mistersolo009@gmail.com', 'linuxadminjbp@vsndirect.com']
msg.set_content('Please find attached the server details report.')

with open(log_path, 'rb') as f:
    msg.add_attachment(f.read(), maintype='text', subtype='plain', filename=log_file)

# Send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS'))
    smtp.send_message(msg)
