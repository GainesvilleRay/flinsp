# built-in libraries
import csv
import datetime
import os.path
import re
import sys

# installed with pip
import pandas as pd

# Create dataframe from files
colnames = [
    "county", "licnum", "sitename", "streetaddy", "cityaddy", "zip",
    "inspnum", "insptype", "inspdispos", "inspdate", "totalvio", "highvio",
    "intermedvio", "basicvio", "vio22", "vio23", "vio24", "vio25", "vio26",
    "vio28", "vio29", "vio30", "vio32", "vio33", "vio37", "vio43", "vio48",
    "vio49", "vio50", "vio52", "vio56", "vio62", "vio71", "vio73", "vio74",
    "licid", "visitid"
    ]

colnums = [
    2, 4, 5, 6, 7, 8, 9, 12, 13, 14, 17, 18, 19, 20, 22, 23, 24, 25, 26,
    28, 29, 30, 32, 33, 37, 43, 48, 49, 50, 52, 56, 62, 71, 73, 74, 80, 81
    ]

filepath18_1 = 'fy2018/1fdinspi_1819.csv'
filepath18_2 = 'fy2018/2fdinspi_1819.csv'
filepath18_3 = 'fy2018/3fdinspi_1819.csv'
filepath18_4 = 'fy2018/4fdinspi_1819.csv'
filepath18_5 = 'fy2018/5fdinspi_1819.csv'
filepath18_6 = 'fy2018/6fdinspi_1819.csv'

df18_1 = pd.read_csv(
    filepath18_1,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df18_2 = pd.read_csv(
    filepath18_2,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df18_3 = pd.read_csv(
    filepath18_3,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df18_4 = pd.read_csv(
    filepath18_4,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df18_5 = pd.read_csv(
    filepath18_5,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df18_6 = pd.read_csv(
    filepath18_6,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df18_all = pd.concat(
    [df18_1, df18_2, df18_3, df18_4, df18_5, df18_6], ignore_index=True
    )

# START OUR ANALYSIS

# How many counties are included in the dataframe
co_count = len(list(df18_all.groupby(['county']).groups.keys()))

print("There are " + str(co_count) + " counties in our dataframe.\n")

# Which counties are included
co_inc = list(df18_all.groupby(['county']).groups.keys())
print("These counties are: " + str(', '.join(co_inc)) + "\n")

#List of all Florida counties
with open('counties.txt', 'r') as f:
    fl_counties = [line.rstrip('\n') for line in f]

def diff(co_inc, fl_counties):
    co_dif = [i for i in co_inc + fl_counties if i not in co_inc]
    return co_dif

missing_counties = diff(co_inc, fl_counties)

print("The ones not included are: " + str(', '.join(missing_counties)))

""" WHY ARE WE MISSING SOME?? """
