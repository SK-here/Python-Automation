#!/usr/bin/python3

from datetime import datetime

############################################## READIN A LOG FILE SECTION ###########################################################

# reading the log from a file
log_file = datetime.now().strftime("%d-%m-%Y") + '.log'
log_dir = 'daily-logs'

logfile = open(log_dir + '/' + log_file)

for i in (log_file):
    print(logfile.readline( ))