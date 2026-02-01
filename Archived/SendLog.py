#!/bin/python3

import subprocess
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Set up email message
msg = EmailMessage()
msg['Subject'] = 'Server Details Report'
msg['From'] = os.environ.get('EMAIL_USER')
msg['To'] = 'linuxadminjbp@vnsdirect.com'
msg['Cc'] = ['mistersolo009@gmail.com']
msg.set_content( 
        f"""
        Dear Team,\n\n 
        Please find attached the server details report for Date: 
        """ 
        + f"{datetime.now().strftime('%d-%m-%Y')}" 
    )

with open(log_path, 'rb') as f:
    msg.add_attachment(f.read(), maintype='text', subtype='plain', filename=log_file)

# Send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS'))
    smtp.send_message(msg)
