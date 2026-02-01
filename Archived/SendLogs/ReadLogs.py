#!/usr/bin/python3

from datetime import datetime
import re as read_lines

############################################## READIN A LOG FILE SECTION ###########################################################

# reading the log from a file
log_file = datetime.now().strftime("%d-%m-%Y") + '.log'
log_dir = 'daily-logs'

logs = open(log_dir + '/' + log_file)


for log in (logs):
 #  print(log.strip())

    # Sample text containing the output

    text = log

    # Regular expression to find percentage values
#   pattern = r'(\d+)%'

#   # Find all percentage values in the text
#   percentages = read_lines.findall(pattern, text)

#   # Print the extracted percentage values
#   for percentage in percentages:
#       print(f"Percentage: {percentage}%")
    # Regular expression to find lines containing '85% '
    pattern = r'.*85%\s.*'

    # Find all lines containing '85% '
    lines_with_85_percent = read_lines.findall(pattern, text)

    # Print the lines containing '85% '
    for line in lines_with_85_percent:
        print(line)
