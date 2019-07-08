"""
This gathers information on all licensed restaurants in Florida
(in fiscal year 2018-19) as a reference for further analaysis
in our other scripts.

It is based on csv files available at:

We'll just use some of the columns most relevant to our work.
"""

# built-in libraries
import csv
import datetime
import os.path
import re
import sys

# installed with pip
import pandas as pd

# Create dataframe from files
colnames = ["sitename", "streetaddy", "cityaddy", "countynum", "licnum"]

colnums = [14, 16, 19, 22, 26]

path1 = 'fy2018/hrfood1.csv'
path2 = 'fy2018/hrfood2.csv'
path3 = 'fy2018/hrfood3.csv'
path4 = 'fy2018/hrfood4.csv'
path5 = 'fy2018/hrfood5.csv'
path6 = 'fy2018/hrfood6.csv'
path7 = 'fy2018/hrfood7.csv'

df1 = pd.read_csv(
    path1,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df2 = pd.read_csv(
    path2,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df3 = pd.read_csv(
    path3,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df4 = pd.read_csv(
    path4,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df5 = pd.read_csv(
    path5,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df6 = pd.read_csv(
    path6,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df7 = pd.read_csv(
    path7,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)
