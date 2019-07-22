# Code to analyze emergency closure data

"""
Here are codes used by state inspectors when they determine
a restaurant should be closed temporarily. This is taken from
http://www.myfloridalicense.com/DBPR/hotels-restaurants/inspections/inspection-dispositions/


Facility Temporarily Closed:
Operations ordered stopped until violations are corrected
The inspector recommended closing the facility immediately
after finding conditions that may endanger the health and
safety of the public.

Dispositions included in this result are:

Emergency order recommended – Conditions have been found
that endanger the health and safety of the public requiring
immediate closure of the establishment.

Administrative determination recommended – The establishment
is operating without a license and action is being taken
to ensure proper licensing is completed.

Emergency Order Callback Not Complied – Corrections to violations
that resulted in an emergency order were not completed
at the time of inspection. Violations may not be noted
again on these inspection reports.
"""

import csv
import pandas as pd
import numpy as np
import sqlite3

# Set up connection to database.

filepath = "/Users/rayd/workspace/flinsp/datafiles/"
dbfile = "rinspect18.sqlite"
dbfile = filepath + dbfile
conn = sqlite3.connect(dbfile)

# Make a list of visitid numbers for restaurants shut down
# by inspectors.

conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

# on initial inspection
vids = c.execute("SELECT visitid FROM fdinsp WHERE inspdispos = 'Emergency order recommended'").fetchall()

# remained shut on subsequent inspection
vids2 = c.execute("SELECT visitid FROM fdinsp WHERE inspdispos = 'Emergency Order Callback Not Complied'").fetchall()

# Make pandas dataframe for both sets

conn = sqlite3.connect(dbfile)

df = pd.read_sql_query("SELECT * FROM fdinsp WHERE inspdispos = 'Emergency order recommended';", conn)
df2 = pd.read_sql_query("SELECT * FROM fdinsp WHERE inspdispos = 'Emergency Order Callback Not Complied';", conn)

# Test to see if our dataset is complete

count1 = df.shape
count2 = df2.shape
print("There were " + str(count1[0]) + " inspections closed on first inspection.")
print("\nThere were " + str(count2[0]) + " remained closed on subsequent inspection.")

# Contains 'Emergency' but means reopened
df_test1 = pd.read_sql_query(
    "SELECT * FROM fdinsp WHERE inspdispos = 'Emergency Order Callback Complied';", conn
    )
count3 = df_test1.shape
print("\nThere were " + str(count3[0]) + " cleared and opened by subsequent inspection.")

# Contains 'Emergency' but also means reopened
df_test2 = pd.read_sql_query(
    "SELECT * FROM fdinsp WHERE inspdispos = 'Emergency Order Callback Time Extension';", conn
    )
count4 = df_test2.shape
print("\nThere were " + str(count4[0]) + " reopened but will need another inspection.")

print("\n" +
    str(count1[0]) + " + " +
    str(count2[0]) + " + " +
    str(count3[0]) + " + " +
    str(count4[0]) + " + " +
    " = " + str(count1[0] + count2[0] + count3[0] + count4[0])
     )

# Contains something like 'Emergency' but are there some where spelling or capitalization shifts?
df_test3 = pd.read_sql_query("SELECT * FROM fdinsp WHERE inspdispos LIKE '%mergency%';", conn)
count5 = df_test3.shape
print("\nThere were " + str(count5[0]) + " that had some word like 'emergency'.")

print("\nSo it looks like we got them all.")

# Create list of dictionaries with detailed inspection reports
# that led to closures

def dict_factory(cursor, row):
    dvio = {}
    for idx, col in enumerate(cursor.description):
        dvio[col[0]] = row[idx]
    return dvio

lvio = []
lvio2 = []

for vid in vids:
    con = sqlite3.connect(dbfile)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(f"SELECT * FROM violations WHERE visitid = {vid}")
    lvio.extend(cur.fetchall())
    con.close()

for vid2 in vids2:
    con = sqlite3.connect(dbfile)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(f"SELECT * FROM violations WHERE visitid = {vid2}")
    lvio2.extend(cur.fetchall())
    con.close()

# Write csv files for violation details

keys = lvio[0].keys

with open('closurevios.csv', 'w', newline='') as output_file:
    fc = csv.DictWriter(output_file,
                        fieldnames=lvio[0].keys()
                       )

    fc.writeheader()
    fc.writerows(lvio)

keys = lvio2[0].keys

with open('closurevios2.csv', 'w', newline='') as output_file:
    fc = csv.DictWriter(output_file,
                        fieldnames=lvio2[0].keys()
                       )

    fc.writeheader()
    fc.writerows(lvio2)

# Make dataframes with violation details

df3 = pd.DataFrame(lvio)
df4 = pd.DataFrame(lvio2)

# What was the most common violation in a closure inspection?

df3.groupby('violation').count().sort_values(by=['visitid'], axis=0, ascending=False)
