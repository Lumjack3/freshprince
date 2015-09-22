import sqlite3 as lite
import datetime
import requests
from pandas.io.json import json_normalize
import time
from dateutil.parser import parse 
import collections
import pandas as pd


r = requests.get('http://www.citibikenyc.com/stations/json')
df = json_normalize(r.json()['stationBeanList'])

con = lite.connect('citi_bike7.db')
cur = con.cursor()

#load static data about bike stations
with con:
    cur.execute('DROP TABLE IF EXISTS citibike_reference')
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')
#a prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

with con:
    for station in r.json()['stationBeanList']:
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))
#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ('_' + str(x) + ' INT' for x in station_ids) 

#clear bike data with every run of the code
with con:
	cur.execute("DROP TABLE IF EXISTS available_bikes")
	cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

for a in range(60):
    r = requests.get('http://www.citibikenyc.com/stations/json')

    df = json_normalize(r.json()['stationBeanList'])

    #take the string and parse it into a Python datetime object
    exec_time = parse(r.json()['executionTime'])

    with con:
        tm = exec_time - datetime.datetime(1970,1,1)
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (tm.total_seconds(),)) 

    id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

    #loop through the stations in the station list
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    #iterate through the defaultdict to update the values in the database
    with con:
        for k, v in id_bikes.iteritems():
            cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + str(tm.total_seconds()) + ";")
    con.commit()
    time.sleep(60)
con.close()

#analysis
con = lite.connect('citi_bike7.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

with con:
    cur.execute("SELECT max(execution_time) FROM available_bikes")
    
rows = cur.fetchall()
mx = rows[0][0]

with con:
    cur.execute("SELECT min(execution_time) FROM available_bikes")
rows = cur.fetchall()
mn = rows[0][0] 
mxchg = 0
chgarray = []
for a in df.columns:
    s = df[a]
    chg = abs(s[mx] - s[mn])
    s1 = chg.tolist()
    s2 = s1[0]
    chgarray.append([a,s2])
    if s2 > mxchg:
        mxchg = s2
        mxrw = a

#query sqlite for reference information
max_station = a[1:]

with con:
    cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
    data = cur.fetchone()

print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(mxchg) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')
