# coding=utf-8
"""
MeetUp 028 - Beginners Python Support Sessions - Tue 17 Sep 2019 - Regular Expressions and JSON

Learning objectives:
    How to read JSON from URL
    Reading lists, dicts, strs, ints, datetimes from JSON
    Find and clean data using regular expressions
    Using sets to find unique values
    Clean html entities

@author D Tim Cummings

Challenge 1: Read Brisbane City Council events calendar in JSON format
http://www.trumba.com/calendars/brisbane-city-council.json
Convert from JSON to python objects (list of dicts)
Print the dict for the first event

Challenge 2: Find the set of unique values for key categoryCalendar

Challenge 3: Convert startDateTime and endDateTime to datetimes

Challenge 4: Find the first event with Planetarium categoryCalendar. Print the location, title, startDateTime

Challenge 5: Repeat challenge 4 also print Cost

Challenge 6: Repeat challenge 4 using regular expression search on Planetarium.

Challenge 7: Write and test regular expressions for the following:
Match 'Planetarium' or 'planetarium'
Match 'Planetarium' only if it is at the end of the line
Match 'Planetarium' or 'Planetariums'

Challenge 8: Find all events which are not free. Print the location, title, startDateTime, cost

Challenge 9: Extract all the numbers from a 'Cost' record using re.findall(pattern, cost)

Challenge 10: Extract all the prices from a 'Cost' record and convert to float. Test your regular expression on
cost = 'Adult $15.00.2 Adults $29.00. Children $5 each'

Challenge 11: Find all events which cost between $13 and $14.

Challenge 12: Use regular expressions to split planetarium prices and description of prices on commas between each price
"""

# Challenge 1: Read Brisbane City Council events calendar in JSON format
# http://www.trumba.com/calendars/brisbane-city-council.json
# Convert from JSON to python objects (list of dicts)
# Print the dict for the first event

from urllib.request import urlopen
import json

# See https://www.data.brisbane.qld.gov.au/ for sources of BCC open data
# get the response from trumba web site containing data from What's On in Brisbane
url = 'http://www.trumba.com/calendars/brisbane-city-council.json'
# response = urlopen(url)
# bytes_from_response = response.read()
# str_from_response = bytes_from_response.decode('utf-8')

# Examples of json dumping to str
json.dumps(123)
json.dumps('abc')
# json.dumps({'abc', 'def', 123})  # not json serializable
# json.dumps(datetime.now())       # not json serializable
json.dumps({'abc': 'def', 123: 'ghi'})
json.dumps(['abc', 'def', 123, 'ghi'])
json.dumps(('abc', 'def', 123, 'ghi'))

# Examples of json loading from str
json.loads('{"abc": "def", "123": "ghi"}')
json.loads('["abc", "def", 123, "ghi"]')
# load the json (JavaScript Object Notation) data from the url's http response into a python list of dicts
# events = json.loads(str_from_response)
# Because HTTPResponse also has a read() function, can also do
# events = json.load(urlopen(url))
with open("brisbane-city-council.json", mode='r') as json_file:
    events = json.load(json_file)

# pretty print the first event
from pprint import pprint
print("Challenge 1: First event from", url)
pprint(events[0])

# Challenge 2: Find the set of unique values for key categoryCalendar
calendars = set()
for event in events:
    calendars.add(event['categoryCalendar'])
print("\nChallenge 2: Set of unique values for key categoryCalendar")
pprint(calendars)

# Challenge 3: Convert startDateTime and endDateTime to datetimes
# Use datetime.strptime %d = 2 digit day, %b = month abbreviated name (Jan, Feb, Mar), %m = 2 digit month,
# %y = 2 digit year, %Y = 4 digit year,
# %I = 12-hour hours, %H = 24-hour hours, %M = minutes, %S = seconds, %p = AM/PM,
# %z = timezone eg -0500, +063415, %Z = timezone name eg UTC, EST AEST
print("\nChallenge 3: Convert startDateTime and endDateTime to datetimes")
from datetime import datetime
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
for event in events:
    event['time_start'] = datetime.strptime(event['startDateTime'] + event['startTimeZoneOffset'], DATETIME_FORMAT)
    event['time_end'] = datetime.strptime(event['endDateTime'] + event['endTimeZoneOffset'], DATETIME_FORMAT)
print("Event 0 start time", events[0]['startDateTime'], events[0]['startTimeZoneOffset'], events[0]['time_start'], type(events[0]['time_start']))

# Challenge 4: Find the first event with Planetarium categoryCalendar. Print the location, title, startDateTime
print("\nChallenge 4: First event with categoryCalendar ending in 'Planetarium'")
for event in events:
    if 'Planetarium' in event['categoryCalendar']:
        print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}")
        break

# Challenge 5: Repeat challenge 4 also print Cost
print("\nChallenge 5: First event with categoryCalendar ending in 'Planetarium' including 'Cost'")
import html

for event in events:
    if 'Planetarium' in event['categoryCalendar']:
        print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}")
        for field in event['customFields']:
            if field['label'] == 'Cost':
                cost_with_entities = field['value']
                print(cost_with_entities)
                cost = html.unescape(cost_with_entities)
                print(cost)
                break
        break

# Challenge 6: Repeat challenge 4 using regular expression search on Planetarium.
print("\nChallenge 6: First event with categoryCalendar ending in 'Planetarium' including 'Cost' using regular expressions")
import re
for event in events:
    if re.search('Planetarium', event['categoryCalendar']):
        print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}")
        for field in event['customFields']:
            if field['label'] == 'Cost':
                print(html.unescape(field['value']))
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
# Match 'Planetarium' or 'Planetariums'
print("\nChallenge 7: Regular expressions")
print(re.findall(r'[Pp]lanetarium', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums'))
print(re.findall(r'[Pp]lanetarium$', 'The Thomas Brisbane Planetarium shows planets shown in another planetarium'))
print(re.findall(r'[Pp]lanetariums?', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums'))

print(re.findall(r'', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums'))
print(re.findall(r'', 'The Thomas Brisbane Planetarium shows planets shown in another planetarium'))
print(re.findall(r'', 'The Thomas Brisbane Planetarium shows planets shown in other planetariums'))

# Challenge 8: Find all events which are not free. Print the location, title, startDateTime, cost
print("\nChallenge 8: Events which are not free")
free = re.compile('[Ff]ree')
for event in events:
    for field in event['customFields']:
        if field['label'] == 'Cost' and not free.search(field['value']):
            print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}:", end=' ')
            print(html.unescape(field['value']))
            break

# Challenge 9: Extract all the numbers from a planetarium 'Cost' record using re.findall(pattern, cost)
print("\nChallenge 9: Extract numbers from a planetarium 'Cost' record")
planetarium = re.compile(r'Planetarium')
for event in events:
    if planetarium.search(event['categoryCalendar']):
        for field in event['customFields']:
            if field['label'] == 'Cost':
                print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}:")
                cost = html.unescape(field['value'])
                print(cost)
                print(re.findall(r'[0-9\.]+', cost))
                break
        break

# Challenge 10: Extract all the prices from a 'Cost' record and convert to float. Test your regular expression on
cost = 'Adult $15.00.2 Adults $29.00. Children $5 each'
print("\nChallenge 10: Extract prices from 'Cost' record", repr(cost))
str_prices = re.findall(r'\$([0-9]*\.?[0-9]{0,2})', cost)
prices = [float(p) for p in str_prices]
print(prices)

# Challenge 11: Find all events which cost between $13 and $14.
print("\nChallenge 11: Find all events which cost between $13 and $14.")
price_pattern = re.compile(r'\$([0-9]*\.?[0-9]{0,2})')
for event in events:
    for field in event['customFields']:
        if field['label'] == 'Cost':
            str_prices = price_pattern.findall(field['value'])
            prices = [p for p in str_prices if 13 <= float(p) <= 14]
            if len(prices) > 0:
                print(f"{event['location']}: {event['title']}: {event['time_start']}: {event['categoryCalendar']}")
                print(field['value'])
                break

# Challenge 12: Use regular expressions to split planetarium prices and description of prices on commas between each price
# cost = "Adult $16.40, Child (3-14 yrs) $10.00, Concession $13.40, Family (2 adult &amp; 2 child, or 1 adult &amp; 3 child) $45, Group (10+ adult) $13.90, Group (10+ child) $9.20"
print("\nChallenge 12: Use regular expressions to split planetarium prices and description of prices on commas between each price")
# solution 1 find all commas not between parentheses
# find_pattern = re.compile(r'[^,(]+(?:\(.*?\)+)*[^,]*')
# solution 2 split on commas not followed by closing parentheses without preceding opening parentheses
# split_pattern = re.compile(r",(?![^(]*\))")
# solution 3 split on price followed by comma
sub_pattern = re.compile(r'(\$[0-9]+\.?[0-9]{0,2}),\s*')
# dollar sign followed by 1 or more digits followed by decimal point followed by 0 to 2 digits followed by comma and maybe some whitespace
# capture the price (dollar sign, digits, decimal, digits) but ignore the comma and whitespace
cut_pattern = re.compile(r"✂🧻✂")
for event in events:
    if "Planetarium" in event["categoryCalendar"]:
        for field in event['customFields']:
            if field['label'] == 'Cost':
                cost = html.unescape(field['value'])
                print(cost)
                # replace captured price with itself plus scissors, paper, scissors dropping comma and whitespace
                cost = sub_pattern.sub(r"\1✂🧻✂", cost)
                print(cost)
                pprint(cut_pattern.split(cost))
        break
