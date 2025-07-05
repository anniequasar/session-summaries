#!/usr/bin/env python3
"""MeetUp 074 - Beginners' Python and Machine Learning - 25 Aug 2020 - JSON and Regular Expressions

Youtube: https://youtu.be/4ocyF6nSyR0
Colab:   https://colab.research.google.com/drive/1El9hOgXGbhwkOnBpv0WrFnSEBZxfTt4B
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online
MeetUp:  https://www.meetup.com/beginners-python-machine-learning/events/272608641/

Learning objectives:
- How to get data from information servers such as events data from Brisbane City Council Planetarium JSON feed
- "Serialize" data so it can be transmitted across a network or saved in a file
- Reading and creating JSON (javascript object notation)
- How to do complex searching and pattern matching of text
- Regular expressions

@author D Tim Cummings
"""
import json  # standard library for javascript object notation. Import the full library but need to prefix every command with json
import re  # standard library for regular expressions.
import datetime  # standard library for dates and times.
import pprint  # standard library for pretty printing
import html  # standard library for html utility functions
from urllib.request import urlopen, urlretrieve  # standard library. Import urlopen and urlretrieve function so don't need to prefix

# See https://www.data.brisbane.qld.gov.au/ for sources of BCC open data
# Events data at https://www.data.brisbane.qld.gov.au/data/dataset/brisbane-city-council-events
# Get the response from trumba web site containing data from What's On in Brisbane
# JSON format: http://www.trumba.com/calendars/brisbane-city-council.json

# 'dumps' converts value to a json formatted str, 'dump' converts value to json file
json_str = json.dumps(123)
print(f"Dumping Python int to json string {json_str=}")

# If using IPython to display variable, don't be confused by which is the json and which is the python str
# IPython shows internal representation of value.
# json_str, 456, '789'
# If using Python use repr() to see how data in variable internally represented
print(f"{repr(json_str)=}, {repr(456)=}, {repr('789')=}")

# Python object notation and Javascript object notation are very similar
# Python to store int in a variable
# a = 123
# Javascript to store int in a variable
# a = 123;

# 'loads' converts json formatted str back to python value. 'load' converts json in file back to python value
print(f"{json.loads('123')=}")

# Task 1: convert a str to json. then convert it back to a Python str

# Solution 1: we can convert int, float, str, list, dict, bool, None to json
print("\nSolution 1: JSON is very similar to Python notation")
python_values = [234, 34.56e1, 3+4j, 'my string', [235, 1.23, 'string in a list', ['list in a list']],
                 ("string in a tuple", 0.0000000000000000000000000123),
                 {'numeric value': 1, 'key2': 'string in a dict', '3': ['list in a dict'], 4: 'numeric key!', },
                 True, None, {'string in a set', 123}, datetime.datetime.now()]
for eg in python_values:
    print("\n" + type(eg).__name__)
    try:
        js = json.dumps(eg)
        print(f"JSON representation  {js}")
        print(f"Original value       {eg!r}")  # !r says show internal representation of value. repr(eg)
        print(f"Reconverted value    {json.loads(js)!r}")
    except TypeError as e:
        print(f"Original value       {eg!r} can't be converted to JSON. {e}")
print()

json_values = []
js = '"JSON can store strings in double quotes"'
print(json.loads(js))
try:
    print(json.loads("'How about single quotes'"))
except json.JSONDecodeError as jde:
    print("JSON can't store strings in single quotes.", jde)

c = 3+4j
# repr() is similar to json.loads() for python object notation except json.loads only works on a few datatypes
ps = repr(3+4j)
print(f"{c=}, {ps=}, {repr(3+4j)=}")

# eval() is similar to json.dumps() for python object notation except eval could evaluate full expressions,
# not just object literals. SECURITY RISK!!
b = eval(ps)
print(f"eval(ps)={b}, type(eval(ps))={type(b).__name__}")

print(f'eval can evaluate any expression so is a security risk: {eval("c*c")=}')

# Load the json data from the Brisbane City Council url into a Python list of dicts
url = "http://www.trumba.com/calendars/brisbane-city-council.json"
events = json.load(urlopen(url=url))
print("\nLoading json from urlopen (file like object")
print(type(events), len(events), events[0])

# Alternatively we can save json to a file. Use !wget from IPython or Jupyter notebook
# !wget http://www.trumba.com/calendars/brisbane-city-council.json
# Use urlretrieve from Python
urlretrieve(url, "brisbane-city-council.json")

# How to load json file into a list of dicts
with open("brisbane-city-council.json", mode='r') as json_file:
    events = json.load(json_file)

print(f"Loading json from open (file object) {events[0]=}")

# Task 2: Find the set of unique values for key categoryCalendar

# Solution 2:
print("\nSolution 2: Unique values of categoryCalendar")
# use set comprehension to create set, then sort into a list
pprint.pprint(sorted({event['categoryCalendar'] for event in events}))

# Challenge 3: Convert startDateTime and endDateTime to datetimes
# Use datetime.strptime %d = 2 digit day, %b = month abbreviated name (Jan, Feb, Mar), %m = 2 digit month,
# %y = 2 digit year, %Y = 4 digit year,
# %I = 12-hour hours, %H = 24-hour hours, %M = minutes, %S = seconds, %p = AM/PM,
# %z = timezone eg -0500, +063415, %Z = timezone name eg UTC, EST AEST

print("\nSolution 3: Convert startDateTime and endDateTime to datetimes")
str_format = "%Y-%m-%dT%H:%M:%S %z"
for event in events:
    event['time_start'] = datetime.datetime.strptime(f"{event['startDateTime']} {event['startTimeZoneOffset']}", str_format)
    event['time_end'] = datetime.datetime.strptime(f"{event['endDateTime']} {event['endTimeZoneOffset']}", str_format)
for event in events[20:41]:
    print(f"Start {event['time_start']} from {event['startDateTime']} {event['startTimeZoneOffset']}, "
          f"End {event['time_end']} from {event['endDateTime']} {event['endTimeZoneOffset']}")

# Challenge 4: Find the first event with Planetarium categoryCalendar. Print the location, title, startDateTime

# Solution 4:
print("\nSolution 4: First event with categoryCalendar ending in 'Planetarium'")
for event in events:
    if 'Planetarium' in event['categoryCalendar']:
        print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}")
        break

# Challenge 5: Repeat challenge 4 also print Cost

print("\nSolution 5: First event with categoryCalendar ending in 'Planetarium' including 'Cost'")
for event in events:
    if 'Planetarium' in event['categoryCalendar']:
        print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}")
        for field in event['customFields']:
            if field['label'] == 'Cost':
                cost = field['value']
                print(cost)
                break  # break out of field loop
        break  # break out of event loop

# Challenge 6: Repeat challenge 4 using regular expression search on Planetarium.
# see https://regex101.com to practise regular expressions
# re.search(pattern, string)

print("\nSolution 6: First event with categoryCalendar ending in 'Planetarium' including 'Cost' using re")
for event in events:
    if re.search('Planetarium', event['categoryCalendar']):
        print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}")
        for field in event['customFields']:
            if field['label'] == 'Cost':
                print(field['value'])
                break
        break

# Use https://regex101.com to help build regular expression
# Example patterns:
# 'recogni[sz]e' : Search for recognise or recognize (any character within square brackets)
# 'ca.e' : Search for words like came, cake, case, cane. Third letter can be anything
# 'colou?r : Search for color or colour (? means 0 or 1 instances of previous character, + means 1 or more)
# 'ca.*e' : Search for text which starts with ca and ends with e and anything in between. (* means 0 or more)
# '^Hello' : Search for line which starts with 'Hello' (^ means start of line)
# 'again$' : Search for line which ends with 'again'   ($ means end of line)

# Challenge 7: Write and test regular expressions for the following:
# Match 'Planetarium' or 'planetarium'
# Match 'Planetarium' only if it is at the end of the line
# Match 'Planetarium' or 'planetariums'
# print(re.findall(r'', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums'))
# print(re.findall(r'', 'The Thomas Brisbane Planetarium shows planets shown in another planetarium'))
# print(re.findall(r'', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums'))

print("\nSolution 7: Regular expressions")
print(re.findall(r'[Pp]lanetarium', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums'))
print(re.findall(r'[Pp]lanetarium$', 'The Thomas Brisbane Planetarium shows planets shown in another planetarium'))
print(re.findall(r'Planetariums?', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums', re.IGNORECASE))

# Challenge 8: Find all events which are not free. Print the location, title, startDateTime, cost

print("\nSolution 8: Events which are not free")
free = re.compile('free', re.IGNORECASE)
for event in events:
    for field in event['customFields']:
        if field['label'] == 'Cost' and not free.search(field['value']):
            print(f"{event['location']}: "
                  f"{html.unescape(event['title'])}: "
                  f"{event['time_start']}: "
                  f"{event['categoryCalendar']}:", end=' ')
            print(field['value'])
            break

# Challenge 9: Extract all the numbers from a planetarium 'Cost' record using re.findall(pattern, cost)

print("\nSolution 9: Extract numbers from a planetarium 'Cost' record")
planetarium = re.compile(r'Planetarium', re.IGNORECASE)
for event in events:
    if planetarium.search(event['categoryCalendar']):
        for field in event['customFields']:
            if field['label'] == 'Cost':
                print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}:")
                cost = field['value']
                print(cost)
                print(re.findall(r'[0-9.]+', cost))
                break
        break

# Challenge 10: Extract all the prices from a 'Cost' record and convert to float. Test your regular expression on
cost = 'Adult $15.00.2 Adults $29.00.Children $5 each'

print("\nSolution 10: Extract prices from 'Cost' record", repr(cost))
str_prices = re.findall(r'\$([0-9]*\.?[0-9]{0,2})', cost)
prices = [float(p) for p in str_prices]
print(prices)

# Challenge 11: Find all events which cost between $13 and $14.

print("\nSolution 11: Find all events which cost between $11 and $20 inclusive.")
price_pattern = re.compile(r'\$([0-9]*\.?[0-9]{0,2})')
for event in events:
    for field in event['customFields']:
        if field['label'] == 'Cost':
            str_prices = price_pattern.findall(field['value'])
            prices = [p for p in str_prices if 11 <= float(p) <= 20]
            if len(prices) > 0:
                print(f"{event['location']}: {html.unescape(event['title'])}: {event['time_start']}: {event['categoryCalendar']}")
                print(field['value'])
                break

# Challenge 12: Use regular expressions to split prices and description of prices on commas between each price
cost = "Adult $16.40, Child (3-14 yrs) $10.00, Concession $13.40, " + \
       "Family (2 adult &amp; 2 child, or 1 adult &amp; 3 child) $45, " + \
       "Group (10+ adult) $13.90, Group (10+ child) $9.20"

print("\nSolution 12: Use regular expressions to split prices and description of prices on commas between each price")
print(repr(cost))
# solution 1 find all commas not between parentheses
# find_pattern = re.compile(r'[^,(]+(?:\(.*?\)+)*[^,]*')
# solution 2 split on commas not followed by closing parentheses without preceding opening parentheses
# split_pattern = re.compile(r",(?![^(]*\))")
# solution 3 split on price followed by comma
sub_pattern = re.compile(r'(\$[0-9]+\.?[0-9]{0,2}),\s*')
# dollar sign followed by 1 or more digits followed by decimal followed by 0 to 2 digits followed by comma and maybe some whitespace
# capture the price (dollar sign, digits, decimal, digits) but ignore the comma and whitespace
cut_pattern = re.compile(r"✂🧻✂")
cost = html.unescape(cost)
# replace captured price with itself plus scissors, paper, scissors dropping comma and whitespace
cost = sub_pattern.sub(r"\1✂🧻✂", cost)
pprint.pprint(cut_pattern.split(cost))
