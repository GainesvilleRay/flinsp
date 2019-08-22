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

imacpath = "/Users/rayd/workspace/flinsp/datafiles/"
airpath = "/Users/Doug/workspace/flinsp/datafiles/"
dbfile = "rinspect18.sqlite"
dbpath = imacpath + dbfile
conn = sqlite3.connect(dbpath)

# Make a list of visitid numbers for restaurants shut down
# by inspectors.

conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

# on initial inspection
vids = c.execute("SELECT visitid FROM fdinsp WHERE inspdispos = 'Emergency order recommended'").fetchall()

# remained shut on subsequent inspection
vids2 = c.execute("SELECT visitid FROM fdinsp WHERE inspdispos = 'Emergency Order Callback Not Complied'").fetchall()

# Make pandas dataframe for both sets

conn = sqlite3.connect(dbpath)

df = pd.read_sql_query("SELECT * FROM fdinsp WHERE inspdispos = 'Emergency order recommended';", conn)
df2 = pd.read_sql_query("SELECT * FROM fdinsp WHERE inspdispos = 'Emergency Order Callback Not Complied';", conn)

# Test to see if our dataset is complete

count1 = df.shape
count2 = df2.shape
print("There were " + str(count1[0]) + " restaurants closed on first inspection.")
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

# initial closures
for vid in vids:
    con = sqlite3.connect(dbpath)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(f"SELECT * FROM violations WHERE visitid = {vid}")
    lvio.extend(cur.fetchall())
    con.close()

# orders to remain closed
for vid2 in vids2:
    con = sqlite3.connect(dbpath)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(f"SELECT * FROM violations WHERE visitid = {vid2}")
    lvio2.extend(cur.fetchall())
    con.close()

# Make dataframes with violation details

df3 = pd.DataFrame(lvio) # Closed on initial inspection
df4 = pd.DataFrame(lvio2) # Remained closed after follow-up

# What was the most common violation in a closure inspection?

df3g = df3.groupby('violation').count().sort_values(by=['visitid'], axis=0, ascending=False)

# What were the most common violations in a closure inspection?

df3.groupby('violation').count().sort_values(
    by=['visitid'], axis=0, ascending=False
    ).head(10)

df_stopsale = df3[df3.obs.str.contains("Stop Sale issued")==True]
df_stopsale.shape
print("In the df of inspections using the summary reports that contained")
print("the words 'Emergency order recommended', we saw " + str(count1[0]) + " initial closures." )
print("But in checking the detailed reports, we find " + str(df_stopsale.shape[0]) + " with 'Stop sale'")
print("Can you have a closure without a 'Stop sale'?")
print("Answers: Yes. 'Stop sale' refers to food item, maybe bad temp, not to the restaurant generally.")

# Can we find which violations resulted in the most closures?

# Violation codes and descriptions
a = '35A-01-4' # Intermediate: Service animals
b = '35A-02-5' # High priority: Live, small flying insects in food service area
c = '35A-03-4' # Basic: Dead roaches on premesis
d = '35A-04-4' # High priority: Rodent activity present as evidenced by droppings
e = '35A-05-4' # High priority: Live roaches found
f = '35A-06-4' # Basic: Accumulation of dead or trapped pests
g = '35A-07-4' # High priority: Small flying insects in bar, kitchen, dumster, prep area
h = '35A-09-4' # High priority: Presence of insects, rodents or other pests
i = '35A-18-4' # High priority: Rodent rub marks present
j = '35A-20-4' # Basic: Dead rodent present
k = '35A-21-4' # High priority: Rodent burrow or nesting materials present
l = '35A-23-4' # High priority: Rodent droppings present
m = '03A-02-4' # High priority: Potentially hazardous  cold food held at greater than 41 degrees

# Are there any closures that don't involve 35A-0*'?
df3z = df3
df3za = df3.groupby('visitid').filter(lambda x: all(a != i for i in x['violation']))
df3zb = df3z.groupby('visitid').filter(lambda x: all(b != i for i in x['violation']))
df3zc = df3z.groupby('visitid').filter(lambda x: all(c != i for i in x['violation']))
df3zd = df3z.groupby('visitid').filter(lambda x: all(d != i for i in x['violation']))
df3ze = df3z.groupby('visitid').filter(lambda x: all(e != i for i in x['violation']))
df3zf = df3z.groupby('visitid').filter(lambda x: all(f != i for i in x['violation']))
df3zg = df3z.groupby('visitid').filter(lambda x: all(g != i for i in x['violation']))
df3zh = df3z.groupby('visitid').filter(lambda x: all(h != i for i in x['violation']))
df3zi = df3z.groupby('visitid').filter(lambda x: all(i != i for i in x['violation']))
df3zj = df3z.groupby('visitid').filter(lambda x: all(j != i for i in x['violation']))
df3zk = df3z.groupby('visitid').filter(lambda x: all(k != i for i in x['violation']))
df3zl = df3z.groupby('visitid').filter(lambda x: all(l != i for i in x['violation']))
df3zm = df3z.groupby('visitid').filter(lambda x: all(m != i for i in x['violation']))

#On checking database directly, this doesn't seem to work ....
print("This approach finds whether, if a violation is present, it always")
print("results in a closure order:")
print("\nThe number of closures on initial inspection = " + str(df3z.shape[0]))
print("\nThe number of closures, despite this being found:")
print("'Service animals' = " + str(df3za.shape[0]))
print("'Live, small flying insects in food service area' = " + str(df3zb.shape[0]))
print("'Dead roaches on premesis' = " + str(df3zc.shape[0]))
print("'Rodent activity present as evidenced by droppings' = " + str(df3zd.shape[0]))
print("'Live roaches found' = " + str(df3ze.shape[0]))
print("'Accumulation of dead or trapped pests' = " + str(df3zf.shape[0]))
print("'Small flying insects in bar, kitchen, dumster, prep area' = " + str(df3zg.shape[0]))
print("'Presence of insects, rodents or other pests' = " + str(df3zh.shape[0]))
print("'Rodent rub marks present' = " + str(df3zi.shape[0]))
print("'Dead rodent present' = " + str(df3zj.shape[0]))
print("'Rodent burrow or nesting materials present' = " + str(df3zk.shape[0]))
print("'Rodent droppings present' = " + str(df3zl.shape[0]))
print("'Potentially hazardous  cold food held at greater than 41 degrees' = " + str(df3zm.shape[0]))
print("\nSo, if 'Rodent rub marks present', the doors are closed!")

# Which counties had the most closures?
# Calculated as closers per licensed restaurant

# Count closures per county; these were closed on initial inspection.
dfc = df.groupby('county').count()
dfc = dfc.licnum.reset_index()
dfc = dfc.rename(columns={'county' : 'county', 'licnum' : 'closures'})
dfc = dfc.set_index('county')
print(dfc)

# Which counties are included in closures
co_inc = list(df.groupby(['county']).groups.keys())

#List of all Florida counties
with open('outfiles/counties.txt', 'r') as f:
    fl_counties = [line.rstrip('\n') for line in f]

def diff(co_inc, fl_counties):
    co_dif = [i for i in co_inc + fl_counties if i not in co_inc]
    return co_dif

missing_counties = diff(co_inc, fl_counties)

print("\nDid any counties not have closure orders in FY2018-19?")
print("\nThese are not included: " + str(', '.join(missing_counties)))
print("\nBut Miami-Dade listed simply as Dade in our data frame.")

missing = list(missing_counties)
missing.remove('Miami-Dade')

# Read in csv of licensed restaurants per county
df_cntylic = pd.read_csv('datafiles/countycount.csv')
df_cntylic = df_cntylic.drop(['Unnamed: 0'], axis=1)
df_cntylic = df_cntylic[~df_cntylic['co_name'].isin(missing)] # drop missing counties
df_cntylic= df_cntylic.rename(columns={"lic_count": "licenses", "co_name": "county"})
df_cntylic = df_cntylic.set_index('county')

# Closures per license
dfc = df_cntylic.join(dfc) # join closures in each county with count of licenses in each county
dfc['ratio'] = dfc.closures / dfc.licenses
dfc['percent'] = dfc.ratio * 100
dfc = dfc.sort_values(by=['ratio'])
most_closed = dfc.sort_values(by=['ratio'], ascending=False).head(10)
least_closed  = dfc.sort_values(by=['ratio'], ascending=True).head(10)
dfc['ratio'] = dfc.closures / dfc.licenses
dfc['percent'] = dfc.ratio * 100
dfc = dfc.sort_values(by=['ratio'])
most_closed = dfc.sort_values(by=['ratio'], ascending=False).head(10)
least_closed  = dfc.sort_values(by=['ratio'], ascending=True).head(10)
print("Counties as outliers for the most closures:")
print(most_closed.head(20))

print("Counties as outliers for the least closures:")
print(least_closed.head(20))

# List restaurants by how many closures they had this year.

# Drop unneeded columns
dropcols = ['librow', 'inspnum', 'insptype', 'inspdispos', 'inspdate', 'totalvio', 'highvio', 'licid', 'visitid', 'time_now', 'time_posted']
df_restaurants = df.drop(dropcols, axis=1)

#Count repeated closures per restaurant, listed by license number
dupes = df_restaurants.pivot_table(index=['licnum'],aggfunc='size')
dupes = dupes.reset_index()

# Drop repeated rows so we can match with the dupes
df_repeats = df_restaurants[df_restaurants.duplicated()]

# Merge dataframes to get df with count of repeats
dupes_count = pd.merge(df_repeats, dupes, on='licnum')
dupes_count = dupes_count.sort_values(by=[0], ascending=False)
dupes_count = dupes_count.drop_duplicates()
isdupe = dupes_count[0]>1 # those with >1 closure
dupes = dupes_count[isdupe] # filter for those >1 closure
dupes

def closure_csv(df_restaurants, lvio, lvio2):

    ''' Write all restaurants with initial closures to csv '''

    df_restaurants = df_restaurants.drop_duplicates()
    df_restaurants.to_csv('outfiles/closedrestaurants.csv', index=False)

    # Write csv file for violation details on initial closures
    keys = lvio[0].keys
    with open('outfiles/closurevios.csv', 'w', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=lvio[0].keys())
        fc.writeheader()
        fc.writerows(lvio)

    # Write csv file for violation details on continued closures
    keys = lvio2[0].keys
    with open('outfiles/closurevios2.csv', 'w', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=lvio2[0].keys())
        fc.writeheader()
        fc.writerows(lvio2)

response = input("Do you want to get a new csv file for restaurant closures: Y or N")

if response == "Y":
    closure_csv(df_restaurants, lvio, lvio2)
elif response == "N":
    pass
