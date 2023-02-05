r"""# MeetUp 173 - Beginners' Python and Machine Learning - 15 Feb 2022 - Python's Relational Database - Sqlite3

Learning objectives:
- using python's sqlite3 to create, read, update, delete data (crud)

Links:
- Colab:   https://colab.research.google.com/drive/1MgCv1TiEYuOeXlrIggICaTKRwdVshFgr
- Youtube: https://youtu.be/_gtAl51nuIk
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/291354161/
- Github:  https://github.com/timcu/session-summaries/tree/master/online

@author D Tim Cummings

Relational databases are useful when you have different tables of data related to each other via foreign keys.
This session will use techniques learnt in the last session to collect data over the Internet and will then save them
in a sqlite3 database for our private use.

References:
- https://docs.python.org/3/library/sqlite3.html
- https://www.sqlite.org/
- https://www.data.brisbane.qld.gov.au

## Brisbane City Council OpenData project

We will collect data from telemetry sensors for rainfall and stream heights. The data is in two files:
### 1. the static metadata giving locations and datatypes
https://www.data.brisbane.qld.gov.au/data/dataset/telemetry-sensors-rainfall-and-stream-heights/resource/117218af-4adc-4f8e-927a-0fe43c46cdb4
### 2. the dynamic measurement data
https://www.data.brisbane.qld.gov.au/data/dataset/telemetry-sensors-rainfall-and-stream-heights/resource/78c37b45-ecb5-4a99-86b2-f7a514f0f447


To run this code in your own virtual environment, create a file called requirements.txt
```
requests
```

Then install requirements from command line after activating virtual environment with
```
pip install -r requirements.txt
```

"""

import datetime
import pprint
import requests
import sqlite3

# Challenge 1 - Create a list of dicts of metadata and data from telemetry sensors for rainfall and stream heights
resource_id_meta = '117218af-4adc-4f8e-927a-0fe43c46cdb4'
resource_id_data = '78c37b45-ecb5-4a99-86b2-f7a514f0f447'

# Solution 1 - see meetup 172
url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search'
p_meta = {'resource_id': resource_id_meta}
resp_meta = requests.get(url=url, params=p_meta)
p_data = {'resource_id': resource_id_data}
resp_data = requests.get(url=url, params=p_data)

lst_data_raw = resp_data.json()['result']['records']
print("Solution 1 - measurement data from BCC")
for row in lst_data_raw[:5]:
    print(row)

lst_meta_raw = resp_meta.json()['result']['records']
print("\nSolution 1 - sensor data from BCC")
for row in lst_meta_raw[:5]:
    print(row)

# Connect to our database (creates a file to store our data)
# Need to detect types otherwise our datetime values won't be recognised as datetimes.
# in colab this file gets deleted every time you leave colab so not good for storing historical data
# Consider mounting your Google Drive in colab so data can persist
con = sqlite3.connect("bpaml173.db", detect_types=sqlite3.PARSE_DECLTYPES)

# https://www.sqlite.org/lang_createtable.html
# Create a table for the metadata. We will make id_sensor primary key because
# don't know if BCC will change existing _id when adding or removing sensors
# Best not to have spaces in column names. Not case-sensitive.
# Can also provide type name such as TEXT, INTEGER, REAL, BLOB (default BLOB)
# and column constraints such as 'PRIMARY KEY' or 'NOT NULL' or 'UNIQUE'
sql = """
DROP TABLE IF EXISTS tbl_sensor;
CREATE TABLE tbl_sensor (
    _id           INTEGER, 
    id_sensor     TEXT    PRIMARY KEY, 
    id_location   TEXT, 
    txt_location  TEXT, 
    txt_type      TEXT, 
    txt_unit      TEXT, 
    deg_latitude  REAL, 
    deg_longitude REAL);"""

# There are 3 ways to execute sql called on connection or cursor object
# - execute        # one sql statement with results
# - executescript  # many sql statements separated by ; but no results
# - executemany    # one sql statement with a list of parameter data
cur = con.executescript(sql)  
cur.close() 
# close cursor when finished with it
# Closing cursor is especially important in jupyter notebooks to avoid 
# 'database locked' errors

# Check if table was created (sqlite_master is a table created automatically)
sql = 'SELECT name FROM sqlite_master'
cur = con.execute(sql)
# we get the results from the cur object. use fetchall to save results in list
rows = cur.fetchall()
cur.close()
print("\nnames from sqlite_master as tuples")
for row in rows:
    print(row)

# By default, sqlite3 returns results as tuples. 
# Set the row_factory if you want something else 
con.row_factory = sqlite3.Row
# sqlite3.Row allows us to access results by index or case-insensitive name
cur = con.execute(sql)
# iterate over cursor if you don't need all data at once saved in variable
# this is more memory efficient
print("\nnames from sqlite_master as Rows converted to dicts")
for row in cur:
    print(row, dict(row))
# need to leave cursor open until finished iterating over it
cur.close()

# Challenge 2 - Prepare our metadata for insertion in database
# 1. Rename keys, so they don't include spaces (str.replace(" ", "_"))

print("\nSolution 2 - dict keys with no spaces")
lst_meta = []
for raw in lst_meta_raw:
    row = {k.replace(" ", "_"): v for k, v in raw.items()}
    lst_meta.append(row)
pprint.pprint(lst_meta[:2])

# https://www.sqlite.org/lang_insert.html
# 3 different forms of sql to insert values into table. We'll use third
# Always use bindings when building queries using data from untrusted sources

# 1. Insert from a tuple of values. Depends on order of columns in table correct and order in tuple correct
# sql = """INSERT INTO tbl_sensor VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

# 2. Insert from a dict of keys and values. Depends on order of columns in table correct 
# sql = """
# INSERT INTO tbl_sensor
# VALUES (:_id, :Sensor_ID, :Location_ID, :Location_Name, :Sensor_Type, :Unit_of_Measure, :Latitude, :Longitude)
# """

# 3. Insert from a dict of keys and values. Order unimportant because all fields named
sql = """
INSERT INTO tbl_sensor 
   (_id,  id_sensor,  id_location,  txt_location,  txt_type,  txt_unit,  deg_latitude,  deg_longitude) 
   VALUES 
   (:_id, :Sensor_ID, :Location_ID, :Location_Name, :Sensor_Type, :Unit_of_Measure, :Latitude, :Longitude)"""

cur = con.execute(sql, lst_meta[0])
# transactions are a feature used by banks to ensure if money was taken out of
# one account and added to another in two separate sql statements, then if the 
# two statements were in the same transaction then either they both were 
# committed or neither were committed. Can't have one committed without the 
# other.
con.commit()  # Need to commit after inserting unless autocommit turned on
cur.close()

cur = con.execute("SELECT * from tbl_sensor")
print("\nRecords in tbl_sensor after one insert")
for row in cur:
    print(dict(row))
cur.close()
# Notice how even though we entered latitudes and longitudes as str they came back as floats

# Challenge 3 - insert second row into table and display full contents of table

print("\nSolution 3 - Records in tbl_sensor after second insert")
cur = con.execute(sql, lst_meta[1])
con.commit()
cur.close()
cur = con.execute("SELECT * from tbl_sensor")
for row in cur:
    print(dict(row))
cur.close()

# Challenge 4 - insert remaining rows into table

print("\nSolution 4 - Number of records in tbl_sensor after all inserts")
# example of using executemany
cur = con.executemany(sql, lst_meta[2:])
con.commit()
# can also re-use open cursor 
for row in cur.execute("SELECT count(*) from tbl_sensor"):
    print(dict(row))
cur.close()

# Challenge 5 - try inserting first row again

# Solution 5 - commented out because it raises an exception
# cur = con.execute(sql, lst_meta[0])
# cur.close()
# con.commit()

# Challenge 6 - create a datastructure for lst_data
# {'_id': 1, 'Measured': '2023-02-04T18:00:00', 'E1809': '0', 'E1531': '-', 'E1515': '0', 'E1512': '0', 'E2020': '0',
# 'E1886': '0', 'E2111': '-', 'E1594': '-0.21', 'E1561': '-0.22', 'E1560': '0', 'E1736': '0', 'E2121': '-',
# 'E1518': '0', 'E1857': '-', 'E1855': '-0.32', 'E1854': '-', 'E1888': '0', 'E1549': '-', 'E2114': '0',
# 'E1764': '-0.72', 'E1554': '0', 'E1710': '-', 'E1596': '0', 'E1528': '-0.26', 'E1850': '0', 'E1580': '-',
# 'E1548': '0', 'E1727': '-', 'E1839': '0', 'E1588': '-0.32', 'E1765': '-', 'E1540': '-', 'E1884': '-',
# 'E1852': '0', 'E2108': '0', 'E1563': '0', 'E1742': '0', 'E1873': '0', 'E1755': '0', 'E1804': '-',
# 'E2023': '-', 'E1845': '-', 'E1572': '0', 'E1849': '2.72', 'E1527': '0', 'E2138': '0', 'E1830': '0',
# 'E1879': '0', 'E2116': '0', 'E1836': '0', 'E1851': '-', 'E1739': '0', 'E1707': '-', 'E1747': '0', 'E2125': '-',
# 'E1752': '0', 'E1803': '0', 'E1573': '-', 'E1706': '0', 'E1578': '0', 'E1847': '-', 'E1745': '-', 'E1524': '0',
# 'E1557': '0', 'E1749': '0', 'E1844': '0', 'E1507': '0', 'E1539': '0', 'E1841': '0', 'E1575': '0', 'E1837': '0',
# 'E1831': '-', 'E1576': '-', 'E1856': '-0.4', 'E1564': '-', 'E1892': '-', 'E1555': '-', 'E1763': '-', 'E1722': '-',
# 'E2141': '0', 'E1702': '-', 'E1566': '0', 'E1875': '0', 'E1838': '0', 'E1843': '-', 'E1570': '-', 'E2142': '-',
# 'E1890': '-', 'E1761': '0', 'E2129': '4.8', 'E1525': '-0.18', 'E1558': '-'}

# Solution 6
# Let's call this table tbl_measure
# _id can be ignored because the same records get a different _id every 10 minutes
# 'Measured' would be more useful as a datetime object eg 'dt_measure'
# Separate columns for each Sensor ID would mean changing the data structure whenever
# a new sensor added which would be bad
# Easier to link to related table tbl_sensor if this tbl_measure had a foreign key
# pointing to the primary key in tbl_sensor
# Measurement values can be a numeric value or '-', For '-' we can just not store a record
sql = """
BEGIN;
DROP TABLE IF EXISTS tbl_measure;
CREATE TABLE tbl_measure (
    dt_measure TIMESTAMP NOT NULL, 
    id_sensor TEXT NOT NULL, 
    rl_measurement REAL,
    FOREIGN KEY (id_sensor) REFERENCES tbl_sensor (id_sensor));
COMMIT;
"""
# BEGIN COMMIT start and stop an SQL transaction

# create empty tbl_measure
cur = con.executescript(sql)  # use executescript for multiple sql statements
cur.close()
con.commit()

# Convert all our measurement times to datetimes, so we can do date arithmetic
# sqlite3 can do some date arithmetic even if dates are in strings, but I would rather be sure.
for row in lst_data_raw:
    row['dt_measure'] = datetime.datetime.strptime(row['Measured'], '%Y-%m-%dT%H:%M:%S')
print("\nFirst data row after parsing time str to datetime")
pprint.pprint(lst_data_raw[0])

sql = """INSERT INTO tbl_measure (dt_measure, id_sensor, rl_measurement) 
         VALUES (:dt_measure, :id_sensor, :rl_measurement)"""
raw = lst_data_raw[0]
cur = con.cursor()  # can get the cursor before executing sql
for k, v in raw.items():
    if k not in ['_id', 'Measured'] and v != '-':
        data = {'dt_measure': raw['dt_measure'], 'id_sensor': k, 'rl_measurement': v}
        cur.execute(sql, data)
con.commit()

print("\nFirst 5 records which have been inserted into tbl_measure")
for row in cur.execute("SELECT * from tbl_measure LIMIT 5"):
    print(dict(row))
cur.close()  # still have to remember to close it when finished

# Challenge 7 - add remaining data

print("\nSolution 7 - Number of records added to tbl_measure")
lst_data = []
for raw in lst_data_raw[1:]:
    for k, v in raw.items():
        if k not in ['_id', 'Measured'] and v != '-':
            lst_data.append({'dt_measure': raw['dt_measure'], 'id_sensor': k, 'rl_measurement': v})
# using executemany() can be more efficient than many execute()
cur = con.executemany(sql, lst_data)
print(f"{cur.rowcount=}")
cur.close()
con.commit()

# QUERYING DATA
sql = "SELECT * FROM tbl_sensor WHERE deg_latitude > -27.4 AND id_sensor LIKE 'E18%'"
# SELECT *        : we want every column from the table(s)
# FROM tbl_sensor : The table(s) we are retrieving data from is tbl_sensor
# WHERE deg_latitude > -27.4 AND id_sensor LIKE 'E18%'
# returns only those records where the latitude is further north than 27.4 deg S
# and the sensor id starts with E18 and ends with anything
print("\nQUERY EXAMPLES")
print(sql)
cur = con.execute(sql)
for row in cur:
    print(dict(row))
cur.close()

# Querying relational data
sql = """
SELECT m.dt_measure, m.rl_measurement, s.txt_unit, m.id_sensor, 
       s.id_sensor as id_sensor_s, s.txt_type, s.txt_location
FROM tbl_measure m 
  JOIN tbl_sensor s ON s.id_sensor=m.id_sensor 
WHERE s.deg_latitude > -27.4 
  AND s.id_sensor LIKE 'E18%'
  AND m.rl_measurement <> 0
ORDER BY m.id_sensor, dt_measure
LIMIT 30
"""
print()
print(sql)
cur = con.execute(sql)
print(f"{'Time':<16s}{'Measurement':>16s}{'Sensor':^12s}{'Type':<20s}{'Location':<8s}")
print(f"{'====':<16s}{'===========':>16s}{'======':^12s}{'====':<20s}{'========':<8s}")
for r in cur:
    print(f"{r['dt_measure']:%Y-%m-%d %H:%M}{r['rl_measurement']:>12.3f} {r['txt_unit']:<3s}{r['id_sensor']:^12s}"
          f"{r['txt_type']:<20s}{r['txt_location']:<8s}")
cur.close()

# Data constraints - e.g., don't want the same sensor measured at the same time twice in database
sql = """CREATE UNIQUE INDEX IF NOT EXISTS idx_sensor_time ON tbl_measure (dt_measure, id_sensor)"""
cur = con.execute(sql)
cur.close()
con.commit()

# Now try adding duplicate data - commented out because raises IntegrityError
sql = """INSERT INTO tbl_measure (dt_measure, id_sensor, rl_measurement) 
         VALUES (:dt_measure, :id_sensor, :rl_measurement)"""
raw = lst_data_raw[0]
cur = con.cursor()
for k, v in raw.items():
    if k not in ['_id', 'Measured'] and v != '-':
        data = {'dt_measure': raw['dt_measure'], 'id_sensor': k, 'rl_measurement': v}
        # cur.execute(sql, data)
con.commit()

# Databases are good at aggregate functions like summing and counting on groups
sql = """
SELECT COUNT(*) as frequency, SUM(rl_measurement) as total, 
       m.id_sensor, s.txt_unit 
FROM tbl_measure m 
JOIN tbl_sensor s ON m.id_sensor=s.id_sensor
WHERE m.rl_measurement <> 0
GROUP BY m.id_sensor, s.txt_unit 
HAVING frequency > 3 
ORDER BY frequency DESC, total DESC"""
print()
print(sql)
cur = con.execute(sql)
for row in cur:
    print(dict(row))
cur.close()

# Updating data
sql = "UPDATE tbl_sensor SET txt_type = 'rainfall' WHERE txt_type = 'Rainfall'"
cur = con.execute(sql)
print()
print(sql)
print(f"{cur.rowcount=}")
cur.close()
con.commit()  # after any sql that updates data

sql = "SELECT * FROM tbl_sensor WHERE txt_type='Rainfall'"
print()
print(sql)
cur = con.execute(sql)
for row in cur:
    print(dict(row))
cur.close()

# Deleting data
sql = "DELETE FROM tbl_sensor WHERE txt_type = 'rainfall'"
print()
print(sql)
cur = con.execute(sql)
print(f"{cur.rowcount=}")
cur.close()
con.commit()  # after any sql that updates data

sql = "SELECT COUNT(*) FROM tbl_sensor"
cur = con.execute(sql)
print(sql)
for row in cur:
    print(dict(row))
cur.close()
