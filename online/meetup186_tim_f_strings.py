# # MeetUp 145 - Beginners' Python and Machine Learning - 07 Jun 2022 - f-strings for absolute beginners
# 
# Learning objectives:
# - Formatting output with f-strings
# 
# 
# Links:
# - Colab:   https://colab.research.google.com/drive/12k2VXt_9z6416PPhonh5WcPFqjU7m94F
# - Youtube: https://youtu.be/1P7y_H9ptSM
# - Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/294358336/
# - Github:  https://github.com/timcu/bpaml-sessions/tree/master/online
# 
# @author D Tim Cummings
# 
# This session will show you how to use the f-strings to format all text output. They were introduced in Python 3.6 and
# quickly became the formatting and string building method of choice.
# 
# - https://docs.python.org/3/library/string.html#formatspec
# - https://docs.python.org/3/tutorial/inputoutput.html
# - https://realpython.com/python-f-strings/
# 
# 
# # Using Google Colab / Jupyter Notebooks / IPython
# 
# - type into a cell
# - press `<shift><enter>` to execute the cell
# - cells can be python code or Markdown text or input fields
# - use ? or Help menu for help
# - see Help menu > Keyboard shortcuts
# 
# Datalore uses Python 3.8 while Google Colab uses Python 3.7

# standard and third party libraries need to be imported. built-in functions and classes do not.
import json
import math
import sys
import urllib.request
from datetime import datetime
from pprint import pprint
from urllib.request import urlopen

# How to determine Python version
print(sys.version)

# A string in Python 3 is a sequence of unicode characters
# Create a str by enclosing it in quotation marks
'Hello' 

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

# Solution 1: Note that double quotes can be used instead of singe quotes
# Multiplier can be before or after str
# Expressions can be passed straight through to functions
print("Solution 1:")
print(50 * "_")

# Challenge 2: Print the following line
# Python wasn't built in a day

# Solution 2: Use double quotes so Python knows the end of the str.
# Apart from different end characters, ' and " are equivalent for defining strs
print("Solution 2:")
print("# Python wasn't built in a day")

# Introducing f strings
# Python f strings or format strings are created by putting an f before the opening quotes
# and {} inside the quotes containing an expression
# The expression can be a string variable
city = "Brisbane"
s = f"Teaching about f strings from sunny {city}"
print(s)

# Expression can be numeric variable
meetup = 186
print(f"This is meetup number {meetup}")

# Challenge 3: Calculate the quotient and remainder from dividing meetup number by weeks per year and show in f string
weeks_per_year = 52

# Solution 3: Introducing how to put a newline character in str
print(f"Solution 3: \nBPAML has been running for {meetup // weeks_per_year} years and {meetup % weeks_per_year} weeks")

# Challenge 4: Print powers of 10 from 1 to a million
# Hint: 1000 = 10**3

# Solution 4: Introducing formats. A number after a : is the minimum width to display the result. 
# By default, numbers are right aligned and text is left aligned.
# Introducing f-string expression formatting after the :
# Demonstrating for loop and range function
print("Solution 4:")
for i in range(7):
    print(f"10**{i} is {10**i:7}")

# Challenge 5: Given that a mile is 1.6 km, print a conversion table of the form 
#  1 miles equals  1.6 km
#  2 miles equals  3.2 km
# ...
# 10 miles equals 16.0 km

# Solution 5: introducing formatting number of decimal places 
# Introducing number type f and formatting number of decimal places
print("Solution 5:")
for n in range(1, 11):
    print(f"{n:2} miles equals {n*1.6:4.1f} km")

# ints can be formatted as d=decimal, b=binary, o=octal, x=hexadecimal
# floats can be formatted as f=floating point (non exponential), e=exponential notation
print("Decimal  Binary   Octal      hex    HEX miles equals    f      e")
for n in range(16):
    print(f"{n:7d} {n:7b} {n:7o} {n:7x} {n:7X} miles equals {n*1.6:4.1f} km {n*1.6:8.3e} km")

# Import data from Brisbane City Council Open Data - Ferry Terminal locations
# https://www.data.brisbane.qld.gov.au/data/dataset/ferry-terminals/resource/430c7115-f63d-4614-816f-a8aa9265ec7b
# Sample Python 2 code
# import urllib
# url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?' \
#       'resource_id=430c7115-f63d-4614-816f-a8aa9265ec7b&limit=5&q=title:jones'
# fileobj = urllib.urlopen(url)
# print fileobj.read()
# Convert to Python 3, import statements moved to beginning of this file
# import urllib.request
url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?' \
      'resource_id=430c7115-f63d-4614-816f-a8aa9265ec7b&limit=5'
fileobj = urllib.request.urlopen(url)
print(fileobj.read())

# A better way to write. Note the import statements at beginning of this file
# import json
# from pprint import pprint
# from urllib.request import urlopen
url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?' \
      'resource_id=430c7115-f63d-4614-816f-a8aa9265ec7b&q=ACTIVE'
with urlopen(url) as file_obj:
    dct_ferry_full = json.loads(file_obj.read().decode('utf-8'))
pprint(dct_ferry_full)

# We are only interested in the ferry terminal records
lst_records = dct_ferry_full["result"]["records"]
for r in lst_records:
    print(r)

# Challenge 6: Print Ferry terminal DESCRIPTION, LATITUDE, LONGITUDE to match following title row
print(f"{'FERRY TERMINAL':35} {'LATITUDE':17} {'LONGITUDE':17}")

# Solution 6: Introducing align right operator
print("Solution 6:")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>17} {'LONGITUDE':>17}")
for r in lst_records[:10]:
    latitude = float(r['LATITUDE'])
    longitude = float(r['LONGITUDE'])
    print(f"{r['DESCRIPTION']:35} {latitude:17.3f} {longitude:17.3f}")

# Challenge 7: Print Ferry terminal DESCRIPTION, LATITUDE, LONGITUDE, PONTOON_LENGTH, PONTOON_MATERIAL 
# to match following title rows. Notice centre operator ^
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}")
print(f"{'              ':35} {'        ':>10} {'         ':>10} { 'LENGTH':>10}  {'MATERIAL':^10}")

print("Solution 7:")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}")
print(f"{'              ':35} {'        ':>10} {'         ':>10} { 'LENGTH':>10}  {'MATERIAL':^10}")
for r in lst_records:
    print(f"{r['DESCRIPTION']:35} {float(r['LATITUDE']):10.3f} {float(r['LONGITUDE']):10.3f} "
          f"{float(r['PONTOON_LENGTH']):9.1f}m  {r['PONTOON_MATERIAL'].strip():^10}")

# Challenge 8: Print terminal DESCRIPTION, LATITUDE, LONGITUDE, PONTOON_LENGTH, PONTOON_MATERIAL, LAST_INSPECTION_DATE
# Normally to convert '2020/10/09 00:00:00+00' I would add '00' and parse with timezone
# However, here they are obviously using a datetime with tz field to store 
# dates without tz (all dates end in ' 00:00:00+00')
# To convert str to date strip the last 12 characters and use strptime
# To convert date to str use strftime
d = datetime.strptime('2020/10/09 00:00:00+00'[:10], '%Y/%m/%d')
print(d.strftime('%d %b %Y'))

print("Solution 8:")
print(f"{'FERRY TERMINAL':35} {'LATITUDE':>10} {'LONGITUDE':>10} {'PONTOON':>10}  {'PONTOON' :^10}   LAST")
print(f"{''              :35} {''         :10} {''          :10} {'LENGTH' :>10}  {'MATERIAL':^10}   INSPECTION")
for r in lst_records:
    d = datetime.strptime(r['LAST_INSPECTION_DATE'][:10], '%Y/%m/%d')
    print(f"{r['DESCRIPTION']:35} {float(r['LATITUDE']):10.3f} {float(r['LONGITUDE']):10.3f} "
          f"{float(r['PONTOON_LENGTH']):9.1f}m  {r['PONTOON_MATERIAL'].strip():^10}   {d:%d %b %Y}")

# fill characters - first character after the : and before the <^> alignment operator
# e.g. zero filling
for i in range(16):
    print(f"Binary {i:2} is {i:>4b} or {i:0>4b}")

s = 'BPAML'
print(f"{s:*^30}")

# The logging notation (introduced in Python 3.8)
# Also possible to show thousands separator using comma
i = 15
print(f"Variable names and values {s=} {i**i=:,d} {i**(i/2)=:,.3f}")

# Showing braces in f-strings
print(f"The f-string f'{{5+7}}' evaluates to '{5+7}'")

# Using variables in formatting
for i in range(20):
    x = math.sin(math.pi * i / 20) * 50
    print(f"{'':->{x}s}")
# Alternative not using f-string
for i in range(20):
    x = math.sin(math.pi * i / 20) * 50
    print('+' * int(x))
