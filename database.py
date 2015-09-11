import sqlite3 as lite
import pandas as pd

con = lite.connect('getting_started.db')

# Inserting rows by passing values directly to `execute()`
with con:

    cur = con.cursor()
    
    cur.execute("DROP TABLE IF EXISTS cities")
    cur.execute("DROP TABLE IF EXISTS weather")
    cur.execute("CREATE TABLE cities (name text, state text)")
    cur.execute("CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)")
    cur.execute("INSERT INTO cities VALUES('Boston', 'MA')")
    cur.execute("INSERT INTO cities VALUES('Chicago', 'IL')")
    cur.execute("INSERT INTO cities VALUES('Miami', 'FL')")
    cur.execute("INSERT INTO cities VALUES('Dallas', 'TX')")
    cur.execute("INSERT INTO cities VALUES('Seattle', 'WA')")
    cur.execute("INSERT INTO cities VALUES('Portland', 'OR')")
    cur.execute("INSERT INTO cities VALUES('San Francisco', 'CA')")
    cur.execute("INSERT INTO cities VALUES('Los Angeles', 'CA')")
    
    cur.execute("INSERT INTO weather VALUES('New York City', 2013, 'July', 'January', 62)")
    cur.execute("INSERT INTO weather VALUES('Boston', 2013, 'July', 'January', 59)")
    cur.execute("INSERT INTO weather VALUES('Chicago', 2013, 'July', 'January', 59)")
    cur.execute("INSERT INTO weather VALUES('Miami', 2013, 'August', 'January', 84)")
    cur.execute("INSERT INTO weather VALUES('Dallas', 2013, 'July', 'January', 77)")
    cur.execute("INSERT INTO weather VALUES('Seattle', 2013, 'July', 'January', 61)")
    cur.execute("INSERT INTO weather VALUES('Portland', 2013, 'July', 'December', 63)")
    cur.execute("INSERT INTO weather VALUES('San Francisco', 2013, 'September', 'December', 64)")
    cur.execute("INSERT INTO weather VALUES('Los Angeles', 2013, 'September', 'December', 75)")
    
    cur.execute("SELECT name, state, year, warm_month, cold_month FROM cities INNER JOIN weather ON name = city WHERE warm_month = 'July';")

rows = cur.fetchall()
df = pd.DataFrame(rows)

print "The cities that are warmest in July are: "
  	
for index, row in df.iterrows():
  	print row[0] + ", " + row[1]