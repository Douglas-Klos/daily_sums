#!/usr/bin/env python3

# Entered some data with a minute of :03 instead of :30.
#   We're correcting those entries and re-writing the database with adjusted epoch times.


import datetime

df = []

with open("database.csv.back") as database_file:
    for line in database_file:
        new_data =line.strip().split(',') 
        new_data[2] = new_data[2][:-9]
        
        if new_data[2][-1:] == '3':
            new_data[0] = int(new_data[0]) + 1620    

        print(new_data)
        df.append(new_data)

with open("database.csv.new", "w") as database_file:
    for line in df:
        database_file.write(f"{line[0]},{line[1]}\n")
