r"""MeetUp 213 - Beginners' Python and Machine Learning - 07 May 2025 - f-strings for absolute beginners

Learning objectives:
- Formatting output with f-strings

Links:
- Colab:   https://colab.research.google.com/drive/1BUWHHqIcIPeQRoGtGEaoCDReBBZzNk9G
- Youtube: https://youtu.be/JLVEJsVg8xQ
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/307299857/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

This session will show you how to use the f-strings to format all text output. They were introduced in Python 3.6 and
quickly became the formatting and string building method of choice.

- https://docs.python.org/3/library/string.html#formatspec
- https://docs.python.org/3/tutorial/inputoutput.html
- https://realpython.com/python-f-strings/


# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or Markdown text or input fields
- use ? or Help menu for help
- see Help menu > Keyboard shortcuts

standard and third party libraries need to be imported. built-in functions and classes do not.
"""
# standard libraries
import json
import locale
import math
import sys
import urllib.request
from datetime import datetime
from pprint import pprint
from urllib.request import urlopen
# third party library (install into virtual environment with `pip install requests`)
import requests

# How to determine Python version
print("System Python version")
print(sys.version)

# A string in Python 3 is a sequence of unicode characters
# Create a str by enclosing it in quotation marks
# Nothing will display unless running in Jupyter Notebook such as Google Colab
'Hello' 

print("\nDisplaying the contents of string variables and literal string constants")
# Assign a string to a variable
s = 'World'
# To display contents of variable in Python use print()
print(s)

# To display representation of variable in IPython (such as Jupyter Notebooks or Google Colab) put the variable on a
# line of its own as the last line of a cell

# For the rest of this session we want to avoid seeing the quotation marks so will use print
print('Hello World')

# print() can print several values space separated
c = 'New York'
print(c, c)

# We can add strings together using +
d = 'Hello ' + c + ' ' + c
print(d)

# Extending the mathematical metaphor, we can multiply 'strings'
dashes = '-' * 40
print(dashes)

# It doesn't have to be a single character str to be multiplied
dash_pipe = '-|-' * 40
print(dash_pipe)

# Challenge: Print a str of 50 underscores

# Solution 1: Note that double quotes can be used instead of single quotes
# Multiplier can be before or after str
# Expressions can be passed straight through to functions
print("\nSolution 1:")
print(50 * "_")

# Challenge 2: Print the following line
# Python wasn't built in a day

# Solution 2: Use double quotes so Python knows the end of the str.
# Apart from different end characters, ' and " are equivalent for defining strs
print("\nSolution 2:")
print("# Python wasn't built in a day")

print("\nIntroducing f strings")
# Python f strings or format strings are created by putting an f before the opening quotes
# and {} inside the quotes containing an expression
# The expression can be a string variable
city = "Brisbane"
s = f"Teaching about f strings from sunny {city}"
print(s)

# Expression can be numeric variable
meetup = 213
print(f"This is meetup number {meetup}")

# Challenge 3: Calculate the quotient and remainder from dividing meetup number by weeks per year and show in f string
weeks_per_year = 52

# Solution 3: Introducing how to put a newline character in str
print(f"\nSolution 3: \nTo present a numbered BPAML session every week would take {meetup // weeks_per_year} years and {meetup % weeks_per_year} weeks")

# Challenge 4: Print powers of 10 from 1 to a million
# Hint: 1000 = 10**3

# Solution 4: Introducing formats. A number after a : is the minimum width to display the result. 
# By default, numbers are right aligned and text is left aligned.
# Introducing f-string expression formatting after the :
# Demonstrating for loop and range function
print("\nSolution 4:")
for i in range(7):
    print(f"10**{i} is {10**i:7}")

# Challenge 5: Given that a mile is 1.6 km, print a conversion table of the form 
#  1 miles equals  1.6 km
#  2 miles equals  3.2 km
# ...
# 10 miles equals 16.0 km

# Solution 5: introducing formatting number of decimal places 
# Introducing number type f and formatting number of decimal places
print("\nSolution 5:")
for n in range(1, 11):
    print(f"{n:2} miles equals {n*1.6:4.1f} km")

# ints can be formatted as d=decimal, b=binary, o=octal, x=hexadecimal
# floats can be formatted as f=floating point (non exponential), e=exponential notation
print("Decimal  Binary   Octal      hex    HEX miles equals    f      e")
for n in range(16):
    print(f"{n:7d} {n:7b} {n:7o} {n:7x} {n:7X} miles equals {n*1.6:4.1f} km {n*1.6:8.3e} km")

print("\nTwo records from Brisbane City Council ferry location opendata api")
# Import data from Brisbane City Council Open Data - Ferry Terminal locations
# https://data.brisbane.qld.gov.au/explore/dataset/ferry-terminals/api/
# Using standard libraries
url = 'https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/ferry-terminals/records?limit=2'
with urlopen(url) as file_obj:
    dct_ferry_two = json.loads(file_obj.read().decode('utf-8'))
pprint(dct_ferry_two)

print("\nAll records from Brisbane City Council ferry location opendata api")
# We are interested in the ferry terminal records. If limit unspecified then default is 10.
# Using 'requests' library
url = f'https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/ferry-terminals/records?limit={dct_ferry_two["total_count"]}'
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse JSON data from the response
    dct_ferry_full = response.json()
    lst_records = dct_ferry_full["results"]
    for r in lst_records:
        print(r)
else:
    print(f"Failed to retrieve data: {response.status_code}")
    lst_records = []

# Define field names
DESCRIPTION = 'description'
GEO_POINT = 'geo_point_2d'
LATITUDE = 'lat'
LONGITUDE = 'lon'
PONTOON_LENGTH = 'pontoon_length'
PONTOON_MATERIAL = 'pontoon_material'
LAST_INSPECTION_DATE = 'last_inspection_date'

# Challenge 6: Print Ferry terminal DESCRIPTION, LATITUDE, LONGITUDE to match following title row
print("\nChallenge 6:")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':17} {'LONGITUDE':17}")

# Solution 6: Introducing align right operator
print("\nSolution 6:")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>17} {'LONGITUDE':>17}")
for r in lst_records[:10]:
    gp = r[GEO_POINT]
    print(f"{r[DESCRIPTION]:35} {gp[LATITUDE]:17.3f} {gp[LONGITUDE]:17.3f}")

# Challenge 7: Print Ferry terminal DESCRIPTION, LATITUDE, LONGITUDE, PONTOON_LENGTH, PONTOON_MATERIAL 
# to match following title rows. Notice centre operator ^
print("\nChallenge 7:")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}")
print(f"{'              ':35} {'        ':>10} {'         ':>10} { 'LENGTH':>10}  {'MATERIAL':^10}")

print("\nSolution 7:")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}")
print(f"{'              ':35} {'        ':>10} {'         ':>10} { 'LENGTH':>10}  {'MATERIAL':^10}")
for r in lst_records:
    gp = r[GEO_POINT]
    print(f"{r[DESCRIPTION]:35} {gp[LATITUDE]:10.3f} {gp[LONGITUDE]:10.3f} "
          f"{r[PONTOON_LENGTH]:9.1f}m  {r[PONTOON_MATERIAL].strip():^10}")

# Let us look at inspection dates
print("\nInspection dates as raw strings from json")
for r in lst_records:
    print(r[LAST_INSPECTION_DATE])

print("\nConverting strings to dates with time zones")
# Normally to convert '2024-04-17T02:00:00+00:00' I would parse to datetime
# However, here they are obviously using a datetime field to store
# dates, and have a bug in their data processing so that they are using Sydney 
# time even though they are in Brisbane
# (all dates are 2AM UTC or 1AM UTC which is 12 noon in Sydney)
# To convert str to datetime use strptime or fromisoformat Python 3.7+
# To convert datetime to date use .date()
# To convert date to str use strftime
from datetime import datetime
from zoneinfo import ZoneInfo
# When using python before 3.7 would have to do the following
# d = datetime.strptime('2024-03-22T01:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
# Python 3.7+ has fromisoformat method
d = datetime.fromisoformat('2024-03-22T01:00:00+00:00')
print("Using strftime")
print(d.strftime('%d %b %Y %H:%M:%S %z'))
# Can use these formats in f-strings
print("Using f-string")
print(f"{d:%d %b %Y %H:%M:%S %z}")
# To change time zones use zoneinfo standard library in Python 3.9+
print(f"Current time zone from json is {d.tzinfo}")
print(f"Same time in Brisbane is {d.astimezone(ZoneInfo('Australia/Brisbane')):%d %b %Y %H:%M:%S %z}")

# Challenge 8: Investigate all times in Brisbane and Sydney time zones

# Solution 8
DT_FMT = '%d %b %Y %H:%M:%S %Z'
print("\nSolution 8:")
for r in lst_records:
    d = datetime.fromisoformat(r[LAST_INSPECTION_DATE])
    print(f"{r[DESCRIPTION]:35} {d.astimezone(ZoneInfo('Australia/Brisbane')):{DT_FMT}}   {d.astimezone(ZoneInfo('Australia/Sydney')):{DT_FMT}}")

# Challenge 9: Print Ferry terminal DESCRIPTION, LATITUDE, LONGITUDE, PONTOON_LENGTH, PONTOON_MATERIAL, LAST_INSPECTION_DATE

print("\nSolution 9:")
DATE_FMT = '%d %b %Y'
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}   LAST")
print(f"{''              :35} {''         :10} {''          :10} {'LENGTH' :>10}  {'MATERIAL':^10}   INSPECTION")
for r in lst_records:
    gp = r[GEO_POINT]
    d = datetime.fromisoformat(r[LAST_INSPECTION_DATE])
    print(f"{r[DESCRIPTION]:35} {gp[LATITUDE]:10.3f} {gp[LONGITUDE]:10.3f} "
          f"{r[PONTOON_LENGTH]:9.1f}m  {r[PONTOON_MATERIAL].strip():^10}   {d:{DATE_FMT}}")

print("\nFill character examples")
# fill characters - first character after the : and before the <^> alignment operator
# e.g. zero filling
for i in range(16):
    print(f"Binary {i:2} is {i:>4b} or {i:0>4b}")

s = 'BPAML'
print(f"{s:*^30}")

print("\nLogging notation using f-strings")
# The logging notation (introduced in Python 3.8)
# Also possible to show thousands separator using comma
i = 15
print(f"Variable names and values {s=} {i**i=:,d} {i**(i/2)=:,.3f}")

print("\nShowing braces in f-strings")
print(f"The f-string f'{{5+7}}' evaluates to '{5+7}'")

print("\nUsing variables in formatting with f-strings")
for i in range(20):
    x = math.sin(math.pi * i / 20) * 50
    print(f"{'':->{x}s}")
print("Alternative not using f-string")
for i in range(20):
    x = math.sin(math.pi * i / 20) * 50
    print('+' * int(x))

# Other formats g and n
# g (general) chooses between e and f depending on value
# n is same as g using currently selected locale
# precision is number of significant figures, not number of decimal places
print("\nUsing g formats in f-strings")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}   LAST")
print(f"{''              :35} {''         :10} {''          :10} {'LENGTH' :>10}  {'MATERIAL':^10}   INSPECTION")
for r in lst_records:
    gp = r[GEO_POINT]
    d = datetime.fromisoformat(r[LAST_INSPECTION_DATE])
    print(f"{r[DESCRIPTION]:35} {gp[LATITUDE]:10.5g} {gp[LONGITUDE]:10.5g} "
          f"{r[PONTOON_LENGTH]:9.1g}m  {r[PONTOON_MATERIAL].strip():^10}   {d:{DATE_FMT}}")

# How to display results in a different locale
# Check available locales (ubuntu)
#!locale -a

# Generate en_DK locale if missing (Denmark with English language)
#!locale-gen en_DK.UTF-8
#!locale -a

print("\nUsing locale and n formats in f-strings")
# Set locale to a European locale that uses comma as decimal separator
locale.setlocale(locale.LC_ALL, 'en_DK.UTF-8')
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}   LAST")
print(f"{''              :35} {''         :10} {''          :10} {'LENGTH' :>10}  {'MATERIAL':^10}   INSPECTION")
for r in lst_records:
    gp = r[GEO_POINT]
    d = datetime.fromisoformat(r[LAST_INSPECTION_DATE])
    print(f"{r[DESCRIPTION]:35} {gp[LATITUDE]:10.5n} {gp[LONGITUDE]:10.5n} "
          f"{r[PONTOON_LENGTH]:9.1n}m  {r[PONTOON_MATERIAL].strip():^10}   {d:{DATE_FMT}}")
    