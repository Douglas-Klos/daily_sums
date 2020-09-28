#!/usr/bin/env python3

import time
import datetime
import math

def menu():
    return """
D. Display current database
A. Add entry
S. Save database
X. Exit
>>> """


def get_input(_type, message, error):
    while True:
        try:
            return _type(input(message))
        except ValueError:
            print(error)


def get_date_time():
    try:
        print("Press ENTER for current date / time...")
        date = input("YYYY/MM/DD - ")

        if date == "":
            return time.time()

        _time = input("HH:MM:SS - ")
        year, month, day = map(int, date.split("/"))
        hour, minute, second = map(int, _time.split(":"))
        return datetime.datetime(year, month, day, hour, minute, second).timestamp()
    except ValueError:
        print("Bad date/time given")
        return 0


def read_database(file_name):
    database = []
    with open(file_name) as open_file:
        for line in open_file:
            database.append(line.strip().split(","))

    return database


def save_database(file_name, database):
    with open(file_name, "w") as database_file:
        for line in database:
            database_file.write(("{}," * len(line)).format(*line).strip(",") + "\n")


def add_entry(time, value, database):
    database.append([time, value])


def display_database(database):
    for line in database:
        print(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(line[0])))
            + ", "
            + line[1]
        )


def main():
    file_name = "database.csv"
    database = read_database(file_name)

    while True:
        selection = input(menu())

        if selection.lower() == "d":
            display_database(database)

        elif selection.lower() == "a":
            new_date_time = get_date_time()
            if new_date_time != 0:
                value = get_input(float, "Enter amount ", "Must be float value")
                add_entry(math.floor(new_date_time), str(value), database)

        elif selection.lower() == "s":
            save_database(file_name, database)

        elif selection.lower() == "x":
            return


if __name__ == "__main__":
    main()
