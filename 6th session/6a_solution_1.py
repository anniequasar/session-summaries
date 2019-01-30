# 6th Session solution to challenge
# Q1. Who won each race?

import csv

#this is an empty dictionary
fastest = {}

with open('run_results.csv',mode='r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter = ',', quotechar = '"', quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        race = row[0]
        runner = row [1]
        time = row[2] 
        if runner in fastest:
            old_time = fastest[runner]["time"]
            if time < old_time:
                fastest[runner] = {"race":race,"time":time}
        else:
            fastest[runner] = {"race":race, "time":time}
print(fastest)
