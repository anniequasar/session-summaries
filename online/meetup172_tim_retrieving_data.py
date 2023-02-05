r"""MeetUp 172 - Beginners' Python and Machine Learning - 08 Feb 2022 - Retrieving data over the Internet

Learning objectives:
- fetching data over a network
- translating data from csv, tsv, json, xml
- byte strings and unicode strings

Links:
- Colab:   https://colab.research.google.com/drive/1bpmolwTKDGHT0-0v97i9i86K6One9C0N
- Youtube: https://youtu.be/sGTDhmejk8E
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/291354144/
- Github:  https://github.com/timcu/session-summaries/tree/master/online

@author D Tim Cummings

Accessing data is an important skill for data scientists. Today we will practise downloading data from the Internet as csv, json, tsv, xml. We will look at character encodings (ascii, utf-8, utf-16) and byte order marks. We will convert between unicode and byte `str`. We will save the data in python collections such as `list` or `dict` or pandas `DataFrame`.

References:
- https://docs.python.org/3/library/urllib.request.html
- https://docs.python.org/3/library/csv.html
- https://requests.readthedocs.io/en/latest/
- https://realpython.com/python-xml-parser/
- https://github.com/timcu/session-summaries/blob/master/online/meetup070_tim_rss_web_scraping.py
- https://en.wikipedia.org/wiki/Byte_order_mark
- https://www.data.brisbane.qld.gov.au

## Bribane City Council OpenData project

We will collect data from telemetry sensors for rainfall and stream heights. The data is in two files:
### 1. the static metadata giving locations and datatypes
https://www.data.brisbane.qld.gov.au/data/dataset/telemetry-sensors-rainfall-and-stream-heights/resource/117218af-4adc-4f8e-927a-0fe43c46cdb4
### 2. the changing measurement data
https://www.data.brisbane.qld.gov.au/data/dataset/telemetry-sensors-rainfall-and-stream-heights/resource/78c37b45-ecb5-4a99-86b2-f7a514f0f447


To run this code in your own virtual environment, create a file called requirements.txt
```
requests
pandas
beautifulsoup4
lxml
```

Then install requirements from command line after activating virtual environment with
```
pip install -r requirements.txt
```
"""

import requests
import pprint
import csv
import io
import pandas as pd
from bs4 import BeautifulSoup

# Challenge 1 - Go to the metadata link and find the Python code to access their data

# Solution 1
# Check the Data API button (top right) which has Python 2 code

# import urllib
# url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?resource_id=117218af-4adc-4f8e-927a-0fe43c46cdb4&limit=5&q=title:jones'  
# fileobj = urllib.urlopen(url)
# print fileobj.read()

# Challenge 2 - Convert to python 3 - Note that urlopen from python2 is in python3 module urllib.request

print("\nSolution 2 - Equivalent Python 3 code")
from urllib.request import urlopen
url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?resource_id=117218af-4adc-4f8e-927a-0fe43c46cdb4&limit=5&q=title:jones'  
fileobj = urlopen(url)
print(fileobj.read())

# Challenge 3 - convert byte str to a unicode str using b.decode(encoding='utf-8')

print("\nSolution 3 - using urllib.request.urlopen()")
# Create a context manager so urlopen resource is automatically closed when exiting context
# Store bytes in a variable so we can convert it to a unicode string
with urlopen(url) as f:
    bytes_from_response = f.read()
print(f"{bytes_from_response=}")

# Solution 3 (continued) - convert using the str method decode()
unicode_from_response = bytes_from_response.decode(encoding='utf-8')
print(f"{unicode_from_response=}")

# Third party library 'requests' is recommended for this type of work
# Only downside is you need to install a third party library using `pip install requests`
# It is already included in anaconda and colab
# In colab we can run commands in OS shell using exclamation mark
# pip list | grep requests

print("\nUsing requests.get()")
# `get` is the http method. also available are `post`, `put`, `delete`
response = requests.get(url)
# `text` is the unicode string already decoded from the bytes because requests has inferred the character encoding
print(f"{response.text[:300]=}")

# you can see what `encoding` requests has inferred
print(f"{response.encoding=}")

# if you really want the original byte string use `content`
print(f"{response.content[:300]=}")

# requests can use 'Content-Type' header to infer encoding
print(f"{response.headers['Content-Type']=}")

# The header also tells us the data type, in this case json
# We can use the python json library to decode this str into a dict or list
#     import json
#     json.loads(response.text)
# or we could use the json() function built-in to requests
print("response.json()=")
pprint.pprint(response.json())

# Note that no data was returned in 'records'. This is because BCC council example had a query filter in the URL that doesn't apply to this record set

# Challenge 4 - remove query parameters from url that are irrelevant and refetch metadata
# Remember original URL
# url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?resource_id=117218af-4adc-4f8e-927a-0fe43c46cdb4&limit=5&q=title:jones'

print("\nSolution 4")
# Anything after ? is a query filter
url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search'
params = {'resource_id': '117218af-4adc-4f8e-927a-0fe43c46cdb4',
          'limit': 5,
          'q': 'title:jones'}
response = requests.get(url=url, params=params)
print("Before deleting q response.json()=")
pprint.pprint(response.json())

# Solution 4 continued - now we can delete q from our params dict and try again
# We will leave the limit of 5
del params['q']
response = requests.get(url=url, params=params)
print("\nAfter deleting q response.json()=")
pprint.pprint(response.json())

print("\nChallenge 5 - get the 'next' batch of 5")
# Hint - look at 
print(f"{response.json()['result']['_links']['next']=}")

# Solution 5
params['offset'] = 5
print("\nSolution 5")
print("requests.get(url=url, params=params).json()=")
pprint.pprint(requests.get(url=url, params=params).json())

# Based on the URLs to the datasets we can infer the following resource_id
resource_id_meta = '117218af-4adc-4f8e-927a-0fe43c46cdb4'
resource_id_data = '78c37b45-ecb5-4a99-86b2-f7a514f0f447'

# Challenge 6 - Programmatically retrieve data from the download buttons csv

print("\nSolution 6")
# Can use the download CSV link to get the csv data
url_csv = 'https://www.data.brisbane.qld.gov.au/data/datastore/dump/78c37b45-ecb5-4a99-86b2-f7a514f0f447?bom=True'
url_data = f'https://www.data.brisbane.qld.gov.au/data/datastore/dump/{resource_id_data}'
params = {'bom': True}
response = requests.get(url_data, params=params)
print(f"{repr(response.text[:1000])=}")

# We don't really want the bom which is not recommended for utf-8 data (byte order is not machine dependent for utf-8
# because each value is 8 bits)
# Confusing that first line ends in \r\n and other lines end in \n
response = requests.get(url_data)  # no BOM
# Create an in-memory text stream
stream = io.StringIO(response.text)
# You can create a csv reader which creates dicts from a text stream or file opened as text
reader = csv.DictReader(stream)
# Can create list of dicts because reader is iterable
lst_data = list(reader)
for row in lst_data[:5]:
    print(row)

# We can also download file and work with downloaded file - from command line
# curl -o data.csv 'https://www.data.brisbane.qld.gov.au/data/datastore/dump/78c37b45-ecb5-4a99-86b2-f7a514f0f447'

# We can save downloaded file using python (wb = writing bytes)
with open('data_from_py.csv', 'wb') as f:
    f.write(response.content)

# ls -al


# Challenge 7 - Create list of dicts using tsv file
# Hint - csv.DictReader(stream, dialect='excel-tab')
# Other formats
url_tsv = 'https://www.data.brisbane.qld.gov.au/data/datastore/dump/78c37b45-ecb5-4a99-86b2-f7a514f0f447?format=tsv&bom=True'
url_json = 'https://www.data.brisbane.qld.gov.au/data/datastore/dump/7e943407-3c0f-48ce-9c4d-9a1a1f679161?format=json'
url_xml = 'https://www.data.brisbane.qld.gov.au/data/datastore/dump/7e943407-3c0f-48ce-9c4d-9a1a1f679161?format=xml'
print(f"\n{csv.list_dialects()=}")

print("\nSolution 7")
response = requests.get(url_data, params={'format': 'tsv'})
# Create an in-memory text stream
stream = io.StringIO(response.text)
# You can create a csv reader which creates dicts from a text stream or file opened as text
reader = csv.DictReader(stream, dialect='excel-tab')
# Can create list of dicts because reader is iterable
lst_data = list(reader)
for row in lst_data[:5]:
    print(row)
# Check that data actually has tabs
print(f"{repr(response.text[:300])=}")

# pandas can do a lot of the work for us if you are using DataFrames already
df = pd.read_csv(url_data, index_col='_id')
print("\nUsing pandas")
print(df)

print("\nXML")
# xml is a big topic and we only need a small subset
# I recommend viewing my session on web scraping with BeautifulSoup
# Check if Beautiful Soup and lxml are installed
# pip list | grep -E 'beautifulsoup4|lxml'

response = requests.get(url_data, {'format': 'xml'})
# Be careful. lxml is for html and lxml-xml is for xml
soup = BeautifulSoup(response.text, features='lxml-xml')
# Find the first row
print(soup.row)
# write some code to convert soup to dict
lst_from_xml = []
rows = soup.findAll('row')
for row in rows:
    d = {'_id': row['_id']}
    d.update({child.name:child.string for child in row.contents})
    lst_from_xml.append(d)
for d in lst_from_xml[:5]:
    print(d)

