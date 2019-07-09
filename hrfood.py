"""
This gathers information on all licensed restaurants in Florida
(in fiscal year 2018-19) as a reference for further analaysis
in our other scripts.

It is based on csv files available at:

We'll just use some of the columns most relevant to our work.

Currently it produces a csv file that shows the number of licensed
restaurants in each county of Florida.
"""

# built-in libraries
import csv
import datetime
import os.path
import re
import sys

# installed with pip
import numpy as np
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
    dtype='str',
    encoding="ISO-8859-1"
    )

df2 = pd.read_csv(
    path2,
    names=colnames,
    usecols=colnums,
    dtype='str',
    encoding="ISO-8859-1"
    )

df3 = pd.read_csv(
    path3,
    names=colnames,
    usecols=colnums,
    dtype='str',
    encoding="ISO-8859-1"
    )

df4 = pd.read_csv(
    path4,
    names=colnames,
    usecols=colnums,
    dtype='str',
    encoding="ISO-8859-1"
    )

df5 = pd.read_csv(
    path5,
    names=colnames,
    usecols=colnums,
    dtype='str',
    encoding="ISO-8859-1"
    )

df6 = pd.read_csv(
    path6,
    names=colnames,
    usecols=colnums,
    dtype='str',
    encoding="ISO-8859-1"
    )

df7 = pd.read_csv(
    path7,
    names=colnames,
    usecols=colnums,
    dtype='str',
    encoding="ISO-8859-1"
    )

df = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)

#df.countynum = df.countynum.astype(int)

# a few remaining NAN values for sitenames and an address
dfna = df[df.isna().any(axis=1)]

# count how many rows per county code
dfcounts = df.groupby('countynum').count()

# dictionary of county codes and names
countydict = {
    '11' : 'Alachua',
    '12' : 'Baker',
    '13' : 'Bay',
    '14' : 'Bradford',
    '15' : 'Brevard',
    '16' : 'Broward',
    '17' : 'Calhoun',
    '18' : 'Charlotte',
    '19' : 'Citrus',
    '20': 'Clay',
    '21' :'Collier',
    '22' : 'Columbia',
    '23' : 'Dade',
    '24' : 'DeSoto',
    '25' : 'Dixie',
    '26' : 'Duval',
    '27' : 'Escambia',
    '28' : 'Flagler',
    '29' : 'Franklin',
    '30' : 'Gadsden',
    '31' : 'Gilchrist',
    '32' : 'Glades',
    '33' : 'Gulf',
    '34' : 'Hamilton',
    '35' : 'Hardee',
    '36' : 'Hendry',
    '37' : 'Hernando',
    '38' : 'Highlands',
    '39' : 'Hillsborough',
    '40' : 'Holmes',
    '41' : 'Indian River',
    '42' : 'Jackson',
    '43' : 'Jefferson',
    '44' : 'Lafayette',
    '45' : 'Lake',
    '46' : 'Lee',
    '47' : 'Leon',
    '48' : 'Levy',
    '49' : 'Liberty',
    '50' : 'Madison',
    '51' : 'Manatee',
    '52' : 'Marion',
    '53' : 'Martin',
    '54' : 'Monroe',
    '55' : 'Nassau',
    '56' : 'Okaloosa',
    '57' : 'Okeechobee',
    '58' : 'Orange',
    '59' : 'Osceola',
    '60' : 'Palm Beach',
    '61' : 'Pasco',
    '62' : 'Pinellas',
    '63' : 'Polk',
    '64' : 'Putnam',
    '65' : 'St. Johns',
    '66' : 'St. Lucie',
    '67' : 'Santa Rosa',
    '68' : 'Sarasota',
    '69' : 'Seminole',
    '70' : 'Sumter',
    '71' : 'Suwannee',
    '72' : 'Taylor',
    '73' : 'Union',
    '74' : 'Volusia',
    '75' : 'Wakulla',
    '76' : 'Walton',
    '77' : 'Washington',
    '78' : 'Unknown',
    '79' : 'Out of State',
    '701' : 'Out of State',
    '705' : 'Out of State',
    '714' : 'Out of State',
    '720' : 'Out of State',
    '730' : 'Out of State',
    '732' : 'Out of State',
    '736' : 'Out of State',
    '739' : 'Out of State',
    '743' : 'Out of State',
    '746' : 'Out of State',
    '80' : 'Foreign',
    '99' :'Unknown'
}

# merge dictionary into dataframe

s1 = pd.Series(countydict) # turn dict into series
result = pd.concat([dfcounts, s1], axis=1, sort=True)
result.rename(columns={0 : 'county'}, inplace=True)
result = result.drop(['sitename', 'streetaddy', 'cityaddy', 'countynum'])
result = result[result['county'] != 'Out of State']
result = result[result['county'] != 'Unknown']
result = result[result['county'] != 'Foreign']
result = result[pd.notnull(result['county'])]
result = result.set_index('county')
result = result.astype(int)

# make a dictionary
cocountdict = result.to_dict()

# write a csv
result.to_csv('countycounty.csv')
