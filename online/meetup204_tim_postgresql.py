r"""MeetUp 204 - Beginners' Python and Machine Learning - 12 Jun 2024 - Postgresql using psycopg

Learning objectives:
- using psycopg to create, read, update, delete data (crud)

Links:
- Colab:   https://colab.research.google.com/drive/1myQ2KzNeczjcUp2Ej1HoGVlPUXo6WFHx
- Youtube: https://youtu.be/DuQ70Yw702k
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/300853260/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

Relational databases are useful when you have different tables of data related to each other via foreign keys. This session will use techniques learnt in the session 172 to collect data over the Internet and will then save them in a postgresql database for our private use.

References:
- https://postgresql.org
- https://www.psycopg.org/psycopg3/docs/index.html
- https://www.data.brisbane.qld.gov.au

Related:
- Meetup 078 - MongoDB
- Meetup 173 - SQLite3

## Brisbane City Council OpenData project

We will collect data from telemetry sensors for rainfall and stream heights. The data is in two files:
### 1. the static metadata giving locations and datatypes
https://www.data.brisbane.qld.gov.au/data/dataset/telemetry-sensors-rainfall-and-stream-heights/resource/117218af-4adc-4f8e-927a-0fe43c46cdb4
### 2. the dynamic measurement data
https://www.data.brisbane.qld.gov.au/data/dataset/telemetry-sensors-rainfall-and-stream-heights/resource/78c37b45-ecb5-4a99-86b2-f7a514f0f447

## Install Postgresql in ubuntu or debian

Note that this is not ideal as data will disappear when you close notebook. Try installing postgresql locally and running this notebook locally. See github for a script to run locally.

You need to install postgresql and psycopg

- Version 2 is called `psycopg2` - don't use for new projects
- Version 3 is called `psycopg` and comes in three types
- `psycopg[binary]` = Quickest and easiest to install. No compilation or libpg dependencies
- `psycopg[c]` = Requires compilation and links to server libraries. Use for production deployments
- `psycopg` = Pure python version. Slower but compatible everywhere

# The following script will work in bash on debian or ubuntu based linux

```bash
# Check which OS
cat /etc/os-release
python3 -m venv venv204
source venv204/bin/activate

# Does it come with psycopg 3
pip list | grep psyco

# install psycopg
pip install psycopg[binary]
# install and start postgresql
sudo apt-get update
sudo apt-get install postgresql postgresql-client
sudo systemctl start postgresql

# Install and start postgresql server, Install client, psycopg library and create database and role
USER=bpaml
 PASS=bpaml
DBNAME=bpaml204
sudo -u postgres psql -c "CREATE ROLE $USER LOGIN PASSWORD '$PASS'"
sudo -u postgres psql -c "CREATE DATABASE $DBNAME WITH ENCODING='UTF8' OWNER=$USER"
cat <<EOF | tee db_config.ini
[postgresql]
host=localhost
dbname=$DBNAME
user=$USER
password=$PASS
EOF
```
"""

import datetime
import requests
# Note: the module name is psycopg, not psycopg3
import psycopg

# Challenge 1 - Create a list of dicts of metadata and data from telemetry sensors for rainfall and stream heights

# Interim solution 1 after BCC changed their API on 03 June 2024
resp_meta = requests.get('https://pythonator.com/api/sensor_meta.json')
resp_data = requests.get('https://pythonator.com/api/sensor_data.json')
# Old Solution 1 before BCC changed their API - see meetup 172
# resource_id_meta = '117218af-4adc-4f8e-927a-0fe43c46cdb4'
# resource_id_data = '78c37b45-ecb5-4a99-86b2-f7a514f0f447'# url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search'
# p_meta = {'resource_id': resource_id_meta}
# resp_meta = requests.get(url=url, params=p_meta)
# p_data = {'resource_id': resource_id_data}
# resp_data = requests.get(url=url, params=p_data)

lst_data_raw = resp_data.json()['result']['records']
for row in lst_data_raw[:5]:
    print(row)
print(len(lst_data_raw))

lst_meta_raw = resp_meta.json()['result']['records']
for row in lst_meta_raw[:5]:
    print(row)
print(len(lst_meta_raw))

# Define database configuration in dictionary that could have been read from a file
from configparser import ConfigParser
parser = ConfigParser()
parser.read("db_config.ini")
dct_db_config = {param[0]: param[1] for param in parser.items("postgresql")}
print(dct_db_config)

sql = """
DROP TABLE IF EXISTS tbl_measure;
DROP TABLE IF EXISTS tbl_sensor;
CREATE TABLE tbl_sensor (
    _id           INTEGER,
    id_sensor     TEXT    PRIMARY KEY,
    id_location   TEXT,
    txt_location  TEXT,
    txt_type      TEXT,
    txt_unit      TEXT,
    deg_latitude  DOUBLE PRECISION,
    deg_longitude DOUBLE PRECISION);"""

# Connect to an existing database
# Using contextlib `with` means conn will
#   1. automatically commit or rollback depending on whether exception
#   2. automatically close connection
with psycopg.connect(**dct_db_config) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table (dropping if it exists)
        cur.execute(sql)
# exiting `with` code block commits change and closes connection


# In terminal you can run psql. To paste into terminal use ctrl-shift-v
# sudo -u postgres psql
# \? for help. <space> to page, q to quit paging
# \l to list databases
# \c bpaml204 to connect to a database
# \dt to display tables in that database
# \d tbl_sensor to display the structure of a table
# drop table tbl_sensor; to drop a table
# \q to quit psql

# Check if table was created (easier to use psql above)
sql = """SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY table_schema, table_name;"""
with psycopg.connect(**dct_db_config) as conn:
    # we get the results from the cur object. use fetchall to save results in list
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
for row in rows:
    print(row)

# By default, psycopg returns results as tuples.
# Set the row_factory in connect() or cursor() if you want something else
from psycopg.rows import dict_row, namedtuple_row
with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn:
    # we get the results from the cur object. use fetchall to save results in list
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)
            print(row['table_name'])
    with conn.cursor(row_factory=namedtuple_row) as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)
            print(row.table_name)

# Challenge 2 - Prepare our metadata for insertion in database
# 1. Rename keys so they don't include spaces (str.replace(" ", "_"))
# Example
# {'_id': 1, 'Sensor ID': 'E1809', 'Location ID': '540801', 'Location Name': 'Rachele Close, Forest Lake', 'Sensor Type': 'Rainfall', 'Unit of Measure': 'mm', 'Latitude': '-27.631476', 'Longitude': '152.953555'}



# Solution 2
lst_meta = []
for raw in lst_meta_raw:
    row = {k.replace(" ", "_"): v for k, v in raw.items()}
    lst_meta.append(row)
lst_meta[:2]

# https://www.psycopg.org/psycopg3/docs/basic/params.html
# 3 different forms of sql to insert values into table. We'll use third
# Always use bindings when building queries using data from untrusted sources to prevent sql injection
# psycopg 3 uses server side bindings (2 used client side bindings)

# 1. Insert from a tuple of values. Depends on order of columns in table correct and order in tuple correct
sql = """INSERT INTO tbl_sensor VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

# 2. Insert from a dict of keys and values. Depends on order of columns in table correct
sql = """INSERT INTO tbl_sensor VALUES (%(_id)s, %(Sensor_ID)s, %(Location_ID)s, %(Location_Name)s, %(Sensor_Type)s, %(Unit_of_Measure)s, %(Latitude)s, %(Longitude)s)"""

# 3. Insert from a dict of keys and values. Order unimportant because all fields named
sql = """INSERT INTO tbl_sensor
   (_id,  id_sensor,  id_location,  txt_location,  txt_type,  txt_unit,  deg_latitude,  deg_longitude)
   VALUES
   (%(_id)s, %(Sensor_ID)s, %(Location_ID)s, %(Location_Name)s, %(Sensor_Type)s, %(Unit_of_Measure)s, %(Latitude)s, %(Longitude)s)"""

with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn:
    with conn.cursor() as cur:
        cur.execute(sql, lst_meta[0])
        for row in cur.execute("SELECT * from tbl_sensor"):
            print(row)
# Notice how even though we entered latitudes and longitudes as str they came back as floats

"""## Transactions

Transactions are a feature used by banks to ensure if money was taken out of
one account and added to another in two separate sql statements, then if the
two statements were in the same transaction then either they both were
committed or neither were committed. Can't have one committed without the
other.

Using `with` connect will commit or rollback transactions depending on whether an exception occurs.

```python
with psycopg.connect() as conn:
    ... # use the connection

# the connection is now closed
```

is roughly equivalent to

```python
conn = psycopg.connect()
try:
    ... # use the connection
except BaseException:
    conn.rollback()
else:
    conn.commit()
finally:
    conn.close()
```
"""

# Challenge 3 - insert second row into table and display full contents of table



# Solution 3
with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn:
    with conn.cursor() as cur:
        cur.execute(sql, lst_meta[1])
        for row in cur.execute("SELECT * from tbl_sensor"):
            print(row)

# Challenge 4 - inse# Note: the module name is psycopg, not psycopg3
import psycopg
rt remaining rows into table



# Solution 4 - example of using executemany
# Nested with statements can be written on one line

# with psycopg.connect(**dct_db_config) as conn:
#     with conn.cursor() as cur:

# same as
with psycopg.connect(**dct_db_config) as conn, conn.cursor() as cur:
    # Nothing special about executemany. It just loops over execute()
    # It is possible to use copy for improved performance of bulk insert
    cur.executemany(sql, lst_meta[2:])
    for row in cur.execute("SELECT count(*) from tbl_sensor"):
        print(row)

# Challenge 5 - try inserting first row again



# Solution 5 - commented out because it raises an exception
# Demonstrates a shortcut running execute on connection object which creates a cursor
# with psycopg.connect(**dct_db_config) as conn, conn.execute(sql, lst_meta[0]):
#     pass

# Challenge 6 - create a datastructure for lst_data
print(lst_data_raw[0])



# Solution 6
# Let's call this table tbl_measure
# _id can be ignored because the same records get a different _id every 10 mins
# 'Measured' would be more useful as a datetime object eg 'dt_measure'
# Separate columns for each Sensor ID would mean changing the data structure
# whenever a new sensor added which would be bad
# Easier to link to related table tbl_sensor if this tbl_measure had a foreign
# key pointing to the primary key in tbl_sensor
# Measurement values can be a numeric value or '-'.
# For '-' we can just not store a record
sql = """
DROP TABLE IF EXISTS tbl_measure;
CREATE TABLE tbl_measure (
    dt_measure TIMESTAMP NOT NULL,
    id_sensor TEXT NOT NULL,
    rl_measurement REAL,
    FOREIGN KEY (id_sensor) REFERENCES tbl_sensor (id_sensor));
"""

# create empty tbl_measure
with psycopg.connect(**dct_db_config) as conn, conn.execute(sql) as cur:
    pass

# Convert all our measurement times to datetimes so we can do date arithmetic
# sqlite3 can do some date arithmetic even if dates are in strings
fmt = '%Y-%m-%dT%H:%M:%S'
for row in lst_data_raw:
    row['dt_measure'] = datetime.datetime.strptime(row['Measured'], fmt)
print(lst_data_raw[0])

sql = "INSERT INTO tbl_measure (dt_measure, id_sensor, rl_measurement) VALUES (%(dt_measure)s, %(id_sensor)s, %(rl_measurement)s)"
raw = lst_data_raw[0]
with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn, conn.cursor() as cur:
    for k, v in raw.items():
        if k not in ['_id', 'Measured', 'dt_measure'] and v != '-':
            data = {'dt_measure': raw['dt_measure'], 'id_sensor': k, 'rl_measurement': v}
            cur.execute(sql, data)

    for row in cur.execute("SELECT * from tbl_measure LIMIT 5"):
        print(dict(row))

# Challenge 7 - add remaining data



# Solution 7
lst_data = []
for raw in lst_data_raw[1:]:
    for k, v in raw.items():
        if k not in ['_id', 'Measured', 'dt_measure'] and v != '-':
            lst_data.append({'dt_measure': raw['dt_measure'], 'id_sensor': k, 'rl_measurement': v})
# using copy() can be more efficient than many execute()
with psycopg.connect(**dct_db_config) as conn:
    with conn.cursor() as cur:
        with cur.copy("COPY tbl_measure (dt_measure, id_sensor, rl_measurement) FROM STDIN") as copy:
            for data in lst_data:
                copy.write_row((data['dt_measure'], data['id_sensor'], data['rl_measurement']))
        print(cur.execute("select count(*) from tbl_measure").fetchone())

# QUERYING DATA
sql = "SELECT * FROM tbl_sensor WHERE deg_latitude > -27.4 AND id_sensor LIKE 'E18%'"
# SELECT *        : we want every column from the table(s)
# FROM tbl_sensor : The table(s) we are retrieving data from is tbl_sensor
# WHERE deg_latitude > -27.4 AND id_sensor LIKE 'E18%'
# returns only those records where the latitude is further north than 27.4 deg S
# and the sensor id starts with E18 and ends with anything

with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn:
    with conn.cursor() as cur:
        for row in cur.execute(sql):
            print(row)

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
with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn, conn.execute(sql) as cur:
    print(f"{'Time':<16s}{'Measurement':>16s}{'Sensor':^12s}{'Type':<20s}{'Location':<8s}")
    print(f"{'====':<16s}{'===========':>16s}{'======':^12s}{'====':<20s}{'========':<8s}")
    for r in cur:
        print(f"{r['dt_measure']:%Y-%m-%d %H:%M}{r['rl_measurement']:>12.3f} {r['txt_unit']:<3s}{r['id_sensor']:^12s}{r['txt_type']:<20s}{r['txt_location']:<8s}")

for r in lst_data_raw:
    print(r['E1843'], end='  ')
print()

# Data constraints - eg don't want the same sensor measured at the same time twice in database
sql = """CREATE UNIQUE INDEX IF NOT EXISTS idx_sensor_time ON tbl_measure (dt_measure, id_sensor)"""
with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn, conn.execute(sql) as cur:
    pass

# Now try adding duplicate data - commented out because raises UniqueViolation
sql = "INSERT INTO tbl_measure (dt_measure, id_sensor, rl_measurement) VALUES (%(dt_measure)s, %(id_sensor)s, %(rl_measurement)s)"
raw = lst_data_raw[0]
with psycopg.connect(**dct_db_config) as conn, conn.cursor() as cur:
    for k, v in raw.items():
        if k not in ['_id', 'Measured', 'dt_measure'] and v != '-':
            data = {'dt_measure': raw['dt_measure'], 'id_sensor': k, 'rl_measurement': v}
            # cur.execute(sql, data)

# Databases are good at aggregate functions like summing and counting on groups
sql = """
SELECT COUNT(*) as frequency, SUM(rl_measurement) as total,
       m.id_sensor, s.txt_unit
FROM tbl_measure m
JOIN tbl_sensor s ON m.id_sensor=s.id_sensor
WHERE m.rl_measurement <> 0
GROUP BY m.id_sensor, s.txt_unit
HAVING COUNT(*) > 3
ORDER BY COUNT(*) DESC, total DESC"""
with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn, conn.execute(sql) as cur:
    for row in cur:
        print(dict(row))

# Updating data
sql = "UPDATE tbl_sensor SET txt_type = 'rainfall' WHERE txt_type = 'Rainfall'"
with psycopg.connect(**dct_db_config) as conn, conn.execute(sql) as cur:
    print(f"{cur.rowcount=}")

sql = "SELECT * FROM tbl_sensor WHERE txt_type='Rainfall'"
with psycopg.connect(row_factory=dict_row, **dct_db_config) as conn, conn.execute(sql) as cur:
    for row in cur:
        print(row)

# Deleting data
sql = "DELETE FROM tbl_measure USING tbl_sensor WHERE tbl_measure.id_sensor = tbl_sensor.id_sensor and tbl_sensor.txt_type = 'rainfall'"
with psycopg.connect(**dct_db_config) as conn, conn.execute(sql) as cur:
    print(f"{cur.rowcount=}")

sql = "SELECT COUNT(*) FROM tbl_measure"
with psycopg.connect(**dct_db_config) as conn, conn.execute(sql) as cur:
    print(cur.fetchone())

"""## Postgresql data types

|Description|Postgresl|Python|
|-|-|-|
|integer|int2, int4, int8|int|
|autoincrementing integer|serial2, serial4, serial8|int|
|floating point|float8, double precision|float|
|exact decimal|numeric(p, s), decimal(p, s)|Decimal|
|true or false|bool|bool|
|text|varchar(n), text|str|
|dates|date, timestamp, timestamptz|datetime.datetime|
|bytes|bytea|bytes|
|UUID|uuid|uuid.UUID|
|JSON|json, jsonb|dict or list|
|XML|xml|dict|
|Arrays|eg int4[] or text[][]|list|

Can't go from Python `float` to Postgresql `float4` or `real`.
"""

sql = """
DROP TABLE IF EXISTS tbl_type_demo;
CREATE TABLE tbl_type_demo (
    id            bigserial primary key,
    json_demo     json,
    jsonb_demo    jsonb,
    array_int     int4[],
    array_2d_text text[][]);"""

with psycopg.connect(**dct_db_config) as conn:
    with conn.cursor() as cur:
        cur.execute(sql)

# JSON (postgresql json stores as text data (parsed when read), postgresql jsonb stores as binary data (parsed when saved))
from psycopg.types.json import Jsonb, Json
d = {"a": "alfa", "b": 2, 3: "three", "d": {"e": "echo"}}
sql = "INSERT INTO tbl_type_demo (json_demo, jsonb_demo) VALUES (%s, %s)"
with psycopg.connect(**dct_db_config) as conn:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, (Json(d), Json(d)))
        cur.execute(sql, (Jsonb(d), Jsonb(d)))
        for row in cur.execute("select id, json_demo, jsonb_demo from tbl_type_demo"):
            print(row)

# JSON cannot serialize datetime objects - exception line commented out
d = {"d": datetime.datetime.now()}
print(d)
sql = "INSERT INTO tbl_type_demo (json_demo, jsonb_demo) VALUES (%s, %s)"
with psycopg.connect(**dct_db_config) as conn:
    with conn.cursor(row_factory=dict_row) as cur:
        # cur.execute(sql, (Jsonb(d), Jsonb(d)))
        for row in cur.execute("select id, json_demo, jsonb_demo from tbl_type_demo"):
            print(row)

sql = "INSERT INTO tbl_type_demo (array_int, array_2d_text) VALUES (%s, %s)"
with psycopg.connect(**dct_db_config) as conn:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, ([1, 1, 2, 3, 5, 8], [["a1", "a2", "a3"], ["b1", "b2", "b3"], ["c1", "c2", "c3"]]))
        for row in cur.execute("select id, array_int, array_2d_text from tbl_type_demo"):
            print(row)

