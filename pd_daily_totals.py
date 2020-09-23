#!/usr/bin/env python3

import time
import datetime
import math
import pandas as pd


def menu():
    return """
D. Display current database
A. Add entry
S. Save database
R. Sort database
M. Add multiple daily entries
T. Display daily sums
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
        _date = input("YYYY/MM/DD - ").replace(".", "/").replace(" ", "/").replace("-", "/")
        _time = input("HH:MM - ").replace(".", ":").replace(" ", ":").replace("-", "/")

        if _time == "":
            return time.time()
        if _date == "":
            _date = datetime.date.today().strftime("%Y/%m/%d")

        year, month, day = map(int, _date.split("/"))
        hour, minute = map(int, _time.split(":"))
        return datetime.datetime(year, month, day, hour, minute).timestamp()

    except ValueError:
        print("Bad date/time given")
        return 0


def add_multiple_entriesa():
    new_entries = []
    _date = input("YYYY/MM/DD - ").replace(".", "/").replace(" ", "/").replace("-", "/")
    if _date == "":
        _date = datetime.date.today().strftime("%Y/%m/%d")
    year, month, day = map(int, _date.split("/"))
    while True:
        _time = input("HH:MM - ").replace(".", ":").replace(" ", ":").replace("-", "/")
        if _time == "":
            break
        try:
            hour, minute = map(int, _time.split(":"))
        except ValueError:
            hour = int(_time)
            minute = 0
        value = get_input(float, "Enter dosage ", "Must be float value")
        epoch = datetime.datetime(year, month, day, hour, minute).timestamp()
        new_entries.append({
            "epoch": epoch,
            "value": value,
            "date_time": pd.to_datetime(epoch, unit="s", utc=True).tz_convert("US/Pacific"),
        })

    return new_entries


def pd_read_database(file_name):
    database = pd.read_csv(file_name)
    database["date_time"] = pd.to_datetime(database.epoch, unit="s", utc=True).dt.tz_convert("US/Pacific")
    return database


def pd_save_database(file_name, database):
    # cols_to_keep = ["epoch", "value"]
    # database[cols_to_keep].to_csv(file_name, index=False)
    database.to_csv(file_name, index=False)


def add_entry(time, value, database):
    new_entry = pd.DataFrame(
        data={
            "epoch": [time],
            "value": [value],
            "date_time": [pd.to_datetime(time, unit="s", utc=True).tz_convert("US/Pacific")],
        }
    )
    database = database.append(new_entry, ignore_index=True)
    return database


def pd_sort_database(database):
    return database.sort_values(by=["epoch"])


def pd_display_database(database):
    print(database)


def display_daily_totals(database):
    daily_totals = database.set_index('date_time').groupby(pd.Grouper(freq='D')).sum().reset_index()
    print(daily_totals[['date_time', 'value']])


def main():
    file_name = "database.csv"
    database = pd_read_database(file_name)
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    # pd.options.display.float_format = '{:.2f}'.format

    while True:
        selection = input(menu())

        if selection.lower() == "d":
            pd_display_database(database)

        elif selection.lower() == "a":
            new_date_time = get_date_time()
            if new_date_time != 0:
                value = get_input(float, "Enter dosage ", "Must be float value")
                database = add_entry(math.floor(new_date_time), str(value), database)

        elif selection.lower() == "s":
            pd_save_database(file_name, database)

        elif selection.lower() == "r":
            database = pd_sort_database(database)

        elif selection.lower() == 'm':
            database = database.append(add_multiple_entriesa(), ignore_index=True)

        elif selection.lower() == 't':
            display_daily_totals(database)

        elif selection.lower() == "x":
            return

        else:
            pass


if __name__ == "__main__":
    main()
