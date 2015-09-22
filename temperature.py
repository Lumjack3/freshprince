import sqlite3 as lite
import datetime
import requests
from pandas.io.json import json_normalize
import time
from dateutil.parser import parse 
import collections
import pandas as pd

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }
con = lite.connect('weather.db')
cur = con.cursor()
cities.keys()
APIKEY = "401d4891dd29b0487e3999d1042ad76a"

with con:
    cur.execute('DROP TABLE IF EXISTS daily_temp')
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Boston REAL, Atlanta REAL, Cleveland REAL, Austin REAL, Chicago REAL);') ## #use your own city names instead of city1...
    
    end_date = datetime.datetime.now() # by setting this equal to a variable, we fix the calculation to the point when we started the scrip (rather than have things move aroudn while we're coding.)

    query_date = end_date - datetime.timedelta(days=30) #the current value being processed

    with con:
        while query_date < end_date:
            qd = query_date - datetime.datetime(1970,1,1)
            cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(qd.total_seconds()),))
            query_date += datetime.timedelta(days=1)

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        url = "https://api.forecast.io/forecast/" + APIKEY +"/" 

        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
        qd = query_date - datetime.datetime(1970,1,1)
        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + str(int(qd.total_seconds())))
            #cur.execute("SELECT * FROM daily_temp WHERE day_of_reading = " + str(int(qd.total_seconds())))
            #rows = cur.fetchall()
            #print rows
        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day


con.close() # a good practice to close connection to database

con = lite.connect('weather.db')
cur = con.cursor()

with con:
    cur.execute("SELECT * FROM daily_temp ORDER BY day_of_reading")

rows = cur.fetchall()
df = pd.DataFrame(rows)

for a in df.columns:
    if a>0:
        print "city: %s min: %s max: %s range: %s" % (cities.keys()[a-1], df[a].min(), df[a].max(), df[a].max()-df[a].min())

con.close()        