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

filepath1 = '1fdinspi.csv'
filepath2 = '2fdinspi.csv'
filepath3 = '3fdinspi.csv'
filepath4 = '4fdinspi.csv'
filepath5 = '5fdinspi.csv'
filepath6 = '6fdinspi.csv'

df1 = pd.read_csv(
    filepath1,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df2 = pd.read_csv(
    filepath2,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df3 = pd.read_csv(
    filepath3,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df4 = pd.read_csv(
    filepath4,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df5 = pd.read_csv(
    filepath5,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df6 = pd.read_csv(
    filepath6,
    names=colnames,
    usecols=colnums,
    dtype=object,
    encoding="ISO-8859-1"
    )

df_all = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)
