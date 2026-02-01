#!/bin/python3

import subprocess
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime


# List of host IP addresses
hosts = [
        # Production Servers
            '172.27.0.35',   # Prod App1
            '172.27.0.36',   # Prod App2
            '172.27.0.37',   # Prod DB1
            '172.27.0.38',   # Prod DB2
        # Iservices
            '172.27.0.170',  # Iservices (new)
            '172.27.0.144',  # UAT Iservices
            '172.27.0.130',  # Iservices
        # UAT
            '172.27.0.44',   # ERPUAT ECC
            '172.27.0.45',   # ERPUAT App1
            '172.27.0.46',   # ERPUAT App2
            '172.27.0.47',   # ERP UAT DB1
            '172.27.0.48',   # ERP UAT DB2
        # SIT
            '172.27.0.5',    # EBS SIT App1
            '172.27.0.6',    # EBS SIT DB2
            '172.27.0.7',    # EBS SIT DB1
            '172.27.0.8',    # EBS SIT DB2
        # TEST Instances (Prodution Replica)
            '172.27.0.15',   # TEST App1
            '172.27.0.16',   # TEST App2
            '172.27.0.17',   # TEST DB1
            '172.27.0.19',   # TEST DB2
        # FTP
            '172.27.0.150',  # FTP Server
        # EBS
            '172.27.0.14',   # EBSDEV
            '172.27.0.18',   # EBSQA
        # ECC
            '172.27.0.34',   # ECC Dashboard
        # EBIZ Production
            '172.27.0.25',   # Ebizprodapp1
            '172.27.0.26',   # Ebizprodapp2
            '172.27.0.27',   # Ebizproddb1
            '172.27.0.28',   # Ebizproddb2
        # Quality Assurance
            '172.27.0.11',   # DEVQADB
        # Honeypot
            '172.27.0.141'   # Honeypot Server
        ]


# SSH username and SSH private key path
username = 'erpnoc'
ssh_key = '/home/admin/.ssh/id_rsa'


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
log_dir = '/home/admin/daily-logs'
log_file = f"Linux-Server-Report-{datetime.now().strftime('%d-%m-%Y')}.txt"
log_path = os.path.join(log_dir, log_file)

os.makedirs(log_dir, exist_ok=True)
with open(log_path, 'w') as f:
    f.write(msg_content)

# Set up email message
msg = EmailMessage()
msg['Subject'] = 'Server Details Report'
msg['From'] = os.environ.get('EMAIL_USER')
msg['To'] = 'linuxadminjbp@vsndirect.com'
msg['Cc'] = ['mistersolo009@gmail.com']
msg.set_content( 
        f"""
Dear Team,
Please find details regarding the Daily Server checklist as of {datetime.now().strftime('%d-%m-%Y')}

# 85+% Server Mount Point Details goes here...

# System Uptime with 5 Days or less goes Here...

# Server Down/Unreachable Goes here...

Thanks & Regards
ERP HelpDesk
MPPKVVCL
Shakti Bhawan
0761-2666806-07
""" 
    )
#        + f"{datetime.now().strftime('%d-%m-%Y')}" 

with open(log_path, 'rb') as f:
    msg.add_attachment(f.read(), maintype='text', subtype='plain', filename=log_file)

# Send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS'))
    smtp.send_message(msg)
