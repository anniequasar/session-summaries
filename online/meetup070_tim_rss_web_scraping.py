#!/usr/bin/env python3
"""MeetUp 070 - Beginners' Python and Machine Learning - 28 Jul 2020 - RSS XML HTML

Youtube: https://youtu.be/BJGSjOmKiZw
Colab:   https://colab.research.google.com/drive/1RksbsUKRf5zik1lhGmLG5jsEo0amOOnh
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

Learning objectives:
- Collecting data from http feeds using RSS, XML, HTML

Requirements:
feedparser
beautifulsoup4
lxml

Data formats
- XML = eXtensible Markup Language - for data (subset of SGML)
- RSS = Really Simple Syndication or Rich Site Summary or RDF Site Summary  - for frequently updated data (subset of XML)
- HTML = HyperText Markup Language - for web pages (subset of SGML) (xhtml is subset of XML)
- JSON = JavaScript Object Notation - for data - similar to Python dict, list, str, float (Not covered today)

Other acronyms
- SGML = Standard Generalised Markup Language
- RDF = Resource Description Framework

Meetup: https://www.meetup.com/Beginners-Python-Machine-Learning/events/272101949/

@author D Tim Cummings
"""

# Third party library designed for reading RSS or ATOM feeds is feedparser
# Documentation available at https://pythonhosted.org/feedparser
# Not available by default in Google colab so use ! to run command line commands in Jupyter Notebook to install
# !pip install feedparser
import datetime
import feedparser
import http  # standard library for comparing HTTP status codes (optional)
import re

from decimal import Decimal
from pprint import pprint  # standard library for pretty printing
from urllib.request import urlopen  # standard library for sending URL requests

from bs4 import BeautifulSoup

# Reserve Bank publishes exchange rates using RSS
# https://www.rba.gov.au/statistics/frequency/exchange-rates.html
# First time you call just provide the URL
p = feedparser.parse("https://www.rba.gov.au/rss/rss-cb-exchange-rates.xml")
# A status of 200 means success
print(f"feedparser parse status {p.status}, data last modified {p.modified}")

# Subsequent times you should provide when your current data was last updated to play nicely with network and server resources
p2 = feedparser.parse("https://www.rba.gov.au/rss/rss-cb-exchange-rates.xml", modified=p.modified)
print("Result of feedparser.parse when data hasn't changed since last time")
pprint(p2)

# Status 304 means Not Modified. Can compare to http.HTTPStatus.NOT_MODIFIED for more readable code
print(f"{p2.status=}, {http.HTTPStatus.NOT_MODIFIED=}, {http.HTTPStatus.NOT_MODIFIED == p2.status=}")

# feedparser lets you use atom or rss feeds.
# atom: feed and entries
# rss: channel and items
# To get a list of rss items can use p['items'] or p['entries'] or p.entries
# Can't use p.items because p is a dict and p.items() returns key, value pairs
print(f"type(p) is {type(p)} which is a subclass of dict {isinstance(p, dict)}")
for item in p['items']:
    print(item['link'])

# Task 1: Display the whole item for Japanese Yen. How does original xml compare to feedparsed dict


# Solution 1
# XML structure has been flattened by feedparser "statistics > exchangeRate > targetCurrency" -> "cb_targetcurrency"
# namespace and tagname are concatenated and lowercase cb:targetCurrency -> cb_targetcurrency
# dc:date -> updated and updated_parsed
# title -> title and title_detail
# description -> summary and summary_detail
# rdf:about -> id
print("\n\nSOLUTION 1\n")
for item in p.entries:
    if item['cb_targetcurrency'] == 'JPY':
        pprint(item)

# Task 2: Read all exchange rates into a dict. Lookup dict for JPY exchange rate


# Solution 2
# from decimal import Decimal
print("\n\nSOLUTION 2\n")


def align_point(d):
    """return str of number with decimal point aligned in column 7"""
    d = Decimal(d)
    if d < 0:
        return "-" + align_point(-d).replace(" ", "", 1)
    return f"{int(d):>6}{str(d - int(d))[1:]:6}"


# create dict of exchange rates using dict comprehension
exchange_rate = {item['cb_targetcurrency']: item['cb_value'] for item in p['items']}
# sort exchange rates alphabetically
keys = list(exchange_rate.keys())
keys.sort()
for key in keys:
    print(f"1 AUD = {align_point(exchange_rate[key])} {key}")

# Side benefit of getting rates as strings rather than numbers
# Significant zeroes are preserved
# No rounding when converting decimal to binary
print(f"Align point {align_point('13.4500')}")
print(f"Align point {align_point(1.100)}")
# Test for negative numbers. Function align_point uses recursion.
print(f"Align point {align_point('-13.45')}")
print(f"Align point {align_point('-.000045')}")
print(f"Align point {align_point('-0.45650')}")
print(f"Align point {align_point('-1300')}")

# from urllib.request import urlopen  # standard library for sending URL requests

# feedparser can take str, url string, filename, open file handle
# This is an example of an open filehandle
page = urlopen('https://www.rba.gov.au/rss/rss-cb-exchange-rates.xml')
p3 = feedparser.parse(page)
print("using feedparser with urlopen", [e['cb_targetcurrency'] for e in p3.entries])
print("urlopen status code", page.getcode())
# Alternatively store content of response from URL request in variable 'page_content'
# page_content = page.read()
# you can only do read() once. If you want to do it again, create a new one from urlopen

# Third party libraries beautifulsoup4 and lxml, used together, are alternative means of parsing xml, html
# They are more flexible but require more configuration
# They are provided by colab so don't need installing
# Other users need to install with
# !pip install beautifulsoup4 lxml
# Documentation is available at https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# from bs4 import BeautifulSoup

# Use Beautiful Soup to parse the content
# To parse html use features="html.parser" or "lxml" (requires lxml installed) or "html5lib" (requires html5lib installed)
# To parse xml  use features="xml" (requires lxml installed)
# BeautifulSoup can read str or open filehandle (eg from urlopen HTTPRequest response 'page')
page = urlopen('https://www.rba.gov.au/rss/rss-cb-exchange-rates.xml')
soup = BeautifulSoup(page, features="xml")

# Beautiful Soup preserves xml structure (no flattening), namespaces and tag names
print("'soup.item' finds the first 'item' Tag in the soup. 'prettify' displays it formatted nicely")
print(soup.item.prettify())

# Task 3: Find the first Tag <cb:exchangeRate>


# Solution 3:
print("\n\nSOLUTION 3\n")
print("'soup.exchangeRate' or 'soup.find('exchangeRate') find the first 'exchangeRate' Tag in the soup")
print(soup.find('exchangeRate'))

# .text extracts the text from Tag and all descendents
# .string extracts the text from Tag only if it is unambiguous what should be returned
#     eg no subtags, or exactly one direct subtag and it has a string
# .strings extracts list of .string from all descendents
print("'soup.exchangeRate.text' extracts the text from all tags in the first 'exchangeRate' Tag in the soup")
print(f"{soup.exchangeRate.text=}\n")

# Task 4: Display the .string value for a Tag which has a .string


# Solution 4:
# descendants finds all sub tags and sub text
# some tags have no .string eg <cb:statistics>
# text has no .string (the containing tag has the .string)
print("\n\nSOLUTION 4\n")
for tag in soup.item.descendants:
    if tag.name is not None and tag.string is not None:
        print(f"Tag {tag.parent.name:20} {tag.name:20} string {tag.string}")

print("'soup.targetCurrency.text' extracts the text from the first 'targetCurrency' Tag in the soup")
print(f"{soup.targetCurrency.text=}\n")

print("'soup.targetCurrency.string' extracts the text from the first 'targetCurrency' Tag in the soup only if unambiguous")
print(f"{soup.targetCurrency.string=}\n")

# 'soup.find()' finds the first Tag. 'soup.item' is the same as 'soup.find("item")'
# 'soup.find_all()' finds all the Tags and returns them in a list
items = soup.find_all('item')
print(f"Soup has len(items) = {len(items)}")

# Task 5: Go through all the exchange rates by currency code and then look up rate for JPY


# Solution 5: each Tag can be navigated the same way as the original soup
print("\n\nSOLUTION 5\n")
rates_from_soup = {}
for er in soup.find_all('exchangeRate'):
    rates_from_soup[er.targetCurrency.text] = er.value.text
# Alternatively use dict comprehension
pprint(rates_from_soup)
# rates_from_soup = {er.targetCurrency.string: er.value.string for er in soup.find_all('exchangeRate')}
print(f"1 AUD = {rates_from_soup['JPY']} JPY")

# attributes can be displayed. attributes need the namespace qualifier
soup.channel['rdf:about']

# for tags the namespace qualifier is optional
soup.find('rdf:li'), soup.find('li'), soup.li

# Any keyword argument can be passed a str, list of strs, regular expression, function or True
soup.find('targetCurrency', string='JPY').parent.value.text

help(soup.find)

help(soup.find_all)

# Task 6: Find petrol buying advice in Brisbane.
# html slightly different to xml, eg multi-value attributes such as class
url = "https://www.accc.gov.au/consumers/petrol-diesel-lpg/petrol-price-cycles"
accc = BeautifulSoup(urlopen(url), features="html.parser")


# Look for h2 tags which separate each capital city data
accc.find_all("h2")

# We can filter further on class = "toc-header"
# Second argument of find_all is attrs. If it is a str then it matches the same as named argument class_="toc-header"
accc.find_all("h2", "toc-header")

# The most reliable is to search on id because id should be unique in an html page
anchor_bne = accc.find(id='petrol-prices-in-brisbane')
# this form useful to search on attributes such as name or data-foo that can't be used in kwargs
anchor_bne = accc.find(attrs={'id': 'petrol-prices-in-brisbane'})
print("\n\nSOLUTION 6\n")
print(anchor_bne)

# From the anchor need to navigate up to the h2, then through the siblings to the ul
# Be careful because characters between tags are also siblings
ul = anchor_bne.parent
while ul.name != "ul":
    ul = ul.next_sibling
    if ul is None:
        break
    try:
        print(f"Looking for ul. Found {str(ul.name):5} of type {type(ul).__name__:15} with text   {ul.text!r}")
    except AttributeError:
        # print(repr(ul))
        print(f"Looking for ul. Found {str(ul.name):5} of type {type(ul).__name__:15} with string {ul.string!r}")
print()
print("Current recommendation in Brisbane:")
if ul is None:
    print("No recommendation")
else:
    print(ul.text)

# Previous example is a common requirement so we can use the find_next_sibling() function
anchor_bne.parent.find_next_sibling("ul")

# Task 7: Find when next low price is going to be


# Solution 7:
# import datetime
print("\n\nSOLUTION 7\n")
# find the next table
table = anchor_bne.parent.find_next("table")  # could also have used find_next_sibling
# find all rows in table
trs = table.tbody.find_all("tr")
# find all cells in last row
tds = trs[-1].find_all("td")
# Convert date of previous low to datetime
date_low_prev = datetime.datetime.strptime(tds[0].string, "%a %d %b %y")
# add the number of days predicted for the cycle
days_in_cycle = int(tds[4].string)
date_low = date_low_prev + datetime.timedelta(days=days_in_cycle)
# display the results
print(f"Predict next low {datetime.datetime.strftime(date_low, '%d %B %Y')}")

# Task 8: Find date of last low price for every city with name ending in 'e'
# Hint see https://regex101.com to test your regular expressions
# import re


# Solution 8: Example of using regular expression when finding
print("\n\nSOLUTION 8\n")
anchors = accc.find_all(id=re.compile(r'petrol-prices-in-\w*e$'))
for anchor in anchors:
    idx = anchor['title'].rfind(' ')
    city = anchor['title'][idx+1:]
    print(f"Last low price in {city} was {anchor.parent.find_next_sibling('table').find_all('td')[-5].string}")

# Task 9: From the RBA web site find the full name of currencies IDR and INR
url = "https://www.rba.gov.au/statistics/frequency/exchange-rates.html"


# Solution 9: Example of using a list of strs when finding
print("\n\nSOLUTION 9\n")
rba_html = BeautifulSoup(urlopen(url), features="html.parser")
trs = rba_html.find_all("tr", id=['IDR', 'INR'])
for tr in trs:
    id = tr['id']
    th = tr.th
    print(f"Code: {id}, Currency: {th.string}")

# Task 10: From the RBA page showing rates over the last three days, find currencies
# where rate has both increased and decreased over that time period


# Solution 10: Example of using a callable when finding
def procasterate(tag):
    if tag.name != "tr":
        return False
    tds = tag.find_all('td')
    r1 = float(tds[0].string)
    r2 = float(tds[1].string)
    r3 = float(tds[2].string)
    return r1 < r2 > r3 or r1 > r2 < r3


print("\n\nSOLUTION 10\n")
tbody = rba_html.find("h2", string="Latest Exchange Rates").find_next_sibling("table").tbody
trs = tbody.find_all(procasterate)
print("Procrastinating Rates")
for tr in trs:
    tds = tr.find_all('td')
    print(f"{tr['id']:7} {tr.th.string:26}, "
          f"r1 {align_point(tds[0].string)}, "
          f"r2 {align_point(tds[1].string)}, "
          f"r3 {align_point(tds[2].string)}")

# Task 11: Find all tags which have an id attribute


# Solution 11: Example of using True when finding
# Also demonstrates that h2 tags don't have ids when page loaded. They are probably added afterwards using javascript
print("\n\nSOLUTION 11\n")
ids = rba_html.find_all(id=True)
for id in ids:
    print(id.name, id['id'])
