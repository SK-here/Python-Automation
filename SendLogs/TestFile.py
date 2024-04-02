#!/usr/bin/python3


#   from datetime import datetime

#   # Get the current date
#   current_date = datetime.now()

#   # Format the date as dd-mm-YY
#   formatted_date = current_date.strftime("%d-%m-%y")

#   # Print the formatted date
#   print(formatted_date)

# Establishing an connection to a gmail server
#   with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#       smtp.ehlo ()
#       smtp.starttls()
#       smtp.ehlo()
#       smtp.login(EMAIL_ADDRESS, EMAIL_PASSWD) 

#       subject = 'Test Subject'
#       body = ' This is a test email'

#       msg = f'Subject: {subject}\n\n{body}'

#       # Format: Sender, Receiver & msg
#       smtp.sendmail (EMAIL_ADDRESS, 'trivedianuj171@gmail.com', msg)

#-------------------- Another Method --------------------
# Instead of starting a session creating a tls session and
# then closing it we can use more secure SSL channel to send
# email plus using email.message library we can define a structured
# way for our message instead of just dumping it to a file



################### GENERATING LOGS 