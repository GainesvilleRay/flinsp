# built-in libraries
import csv
import datetime
import os.path
import re
import sys

# installed with pip
import pandas as pd
import numpy as np

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
filepath18_7 = 'fy2018/7fdinspi_1819.csv'

df18_1 = pd.read_csv(
    filepath18_1,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df18_2 = pd.read_csv(
    filepath18_2,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df18_3 = pd.read_csv(
    filepath18_3,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df18_4 = pd.read_csv(
    filepath18_4,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df18_5 = pd.read_csv(
    filepath18_5,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df18_6 = pd.read_csv(
    filepath18_6,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df18_7 = pd.read_csv(
    filepath18_7,
    names=colnames,
    usecols=colnums,
    encoding="ISO-8859-1"
    )

df18_all = pd.concat(
    [df18_1, df18_2, df18_3, df18_4, df18_5, df18_6, df18_7], ignore_index=True
    )

# START OUR ANALYSIS

# Test to see all counties in Florida are included in our dataframe.

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
print("But it's listed simply as Dade.")

# What was worst restaurant inspection in Florida for the year?
# The most total violations:
most_vios = df18_all.loc[df18_all['totalvio'].idxmax()]
print('\nThe restaurant with the most total violations last year was:')
print(most_vios.iloc[2] + ", " + most_vios.iloc[3] + ", " + most_vios.iloc[4] +
      ", in " + most_vios.iloc[0] + " County, on " + most_vios.iloc[9] + ".")
print("It had " + str(most_vios.iloc[10]) + " total violations, including " + str(most_vios.iloc[11]) +
     " high violations, " + str(most_vios.iloc[12]) + " intermediate violations, and " +
     str(most_vios.iloc[13]) + " basic violations.")

# The most 'high' violations:
most_high_vios = df18_all.loc[df18_all['highvio'].idxmax()]
print('\nThe restaurant with the most "high" violations last year was:')
print(most_high_vios.iloc[2] + ", " + most_high_vios.iloc[3] + ", " + most_high_vios.iloc[4] +
      ", in " + most_high_vios.iloc[0] + " County, on " + most_high_vios.iloc[9] + ".")
print("It had " + str(most_high_vios.iloc[10]) + " total violations, including " + str(most_high_vios.iloc[11]) +
     " high violations, " + str(most_high_vios.iloc[12]) + " intermediate violations, and " +
     str(most_high_vios.iloc[13]) + " basic violations.")

# What is the mean of total violations statewide?
mean_total_vios = round(df18_all['totalvio'].mean(),2) # rounded to two places
print("\nThe mean of total violations per inspection statewide is: " +
      str(mean_total_vios))

# What is the mean of high violations statewide?
mean_high_vios = round(df18_all['highvio'].mean(),2) # rounded to two places
print("\nThe mean of high violations per inspection statewide is: " +
      str(mean_high_vios))

# Which counties have the most & least violations?
# Rather than simply sum them, we'll do this by finding the mean
# for each county, and then seeing which are at least one standard
# deviation away from the mean.

# Mean violations grouped by county
dfcm = df18_all.groupby('county').mean()

# Looking at total violations
dfcmt = dfcm[['totalvio']]
dfcmt = dfcmt.sort_values(by=['totalvio'], axis=0, ascending=False)
dfcmt_mean = round(float(dfcmt.mean()),2) # rounded to two places
print("\nThe mean of total violations when grouped by county is: " +
      str(dfcmt_mean))
# Standard deviation from the grouped mean of total violations
dfcmt_std = round(float(dfcmt.std()),2) # rounded to two places
print("\nThe standard deviation from the mean for total violations grouped by county is: " +
      str(dfcmt_std))

"""
# Looking at outliers: those a standard deviation from the mean
# https://www.quora.com/How-do-I-subtract-the-mean-of-a-row-from-each-element-of-the-row-in-a-data-frame-in-Python-data-handling
dfcmto = dfcmt.sub(dfcmt.mean(axis=1), axis=0)
dfcmto = dfcmto.sort_values(by=['totalvio'], axis=0, ascending=True)
dfcmto

"""


# What is the mean of total violations?
# What is the mean of high violations?
# What is the most common violation?
# Which county has the highest mean for total violations?
# Which county has the highest mean for high violations?
# Which county has the lowest mean for total violations?
# Which county has the lowest mean for high violations?
# Which county has the most inspections per licensed restaurant? (Need data on licensed restaurants)
# Which county has the lowest inspections per licensed restaurant?
