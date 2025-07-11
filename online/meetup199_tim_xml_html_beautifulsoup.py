#!/usr/bin/env python3
r"""MeetUp 199 - Beginners' Python and Machine Learning - 13 Mar 2024 - RSS XML HTML

Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/299605933/
Youtube: https://youtu.be/wOeLWXogLZc
Colab:   https://colab.research.google.com/drive/14y4tAJHzmkNVaEvrwjgu40lhiGuHQ5eG
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

Learning objectives:
- Collecting data from http feeds RSS, XML, HTML using BeautifulSoup

Requirements:
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

@author D Tim Cummings
"""

# Check what third party libraries come with Google Colab
# !pip list | grep beaut
# Check what third party libraries come with Python. Go to terminal with active 
# virtual environment and type the same command without the !
# If your virtual environment is a standard Python then you will need to install
# third party libraries with
# pip install beautifulsoup4 lxml
import datetime
import re

from decimal import Decimal
from pprint import pprint  # standard library for pretty printing
from urllib.request import urlopen  # standard library for sending URL requests

from bs4 import BeautifulSoup

# Reserve Bank publishes exchange rates using RSS
# https://www.rba.gov.au/statistics/frequency/exchange-rates.html

# Documentation is available at https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Use Beautiful Soup to parse the content
# To parse html use features="html.parser" or "lxml" (requires lxml installed) or "html5lib" (requires html5lib installed)
# To parse xml  use features="xml" (requires lxml installed)
# BeautifulSoup can read str or open filehandle (eg from urlopen HTTPRequest response 'page')
page = urlopen('https://www.rba.gov.au/rss/rss-cb-exchange-rates.xml')
soup = BeautifulSoup(page, features="xml")

# Beautiful Soup preserves xml structure (no flattening), namespaces and tag names
print("'soup.item' finds the first 'item' Tag in the soup. 'prettify' displays it formatted nicely")
print(soup.item.prettify())

# Task 1: Find the first Tag <cb:exchangeRate>


# Solution 1:
print("\n\nSOLUTION 1\n")
print("'soup.exchangeRate' or 'soup.find('exchangeRate') find the first 'exchangeRate' Tag in the soup")
print(soup.find('exchangeRate'))

# .text extracts the text from Tag and all descendents
# .string extracts the text from Tag only if it is unambiguous what should be returned
#     eg no subtags, or exactly one direct subtag and it has a string
# .strings extracts list of .string from all descendents
print("'soup.exchangeRate.text' extracts the text from all tags in the first 'exchangeRate' Tag in the soup")
print(f"{soup.exchangeRate.text=}\n")

# Task 2: Display the .string value for a Tag which has a .string


# Solution 2:
# descendants finds all sub tags and sub text
# some tags have no .string eg <cb:statistics>
# text has no .string (the containing tag has the .string)
print("\n\nSOLUTION 2\n")
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

# Task 3: Go through all the exchange rates by currency code and then look up rate for JPY


# Solution 3: each Tag can be navigated the same way as the original soup
print("\n\nSOLUTION 3\n")
rates_from_soup = {}
for er in soup.find_all('exchangeRate'):
    rates_from_soup[er.targetCurrency.text] = er.value.text
# Alternatively use dict comprehension
# rates_from_soup = {er.targetCurrency.string: er.value.string for er in soup.find_all('exchangeRate')}
pprint(rates_from_soup)
print(f"1 AUD = {rates_from_soup['JPY']} JPY")

# attributes can be displayed. attributes need the namespace qualifier
soup.channel['rdf:about']

# for tags the namespace qualifier is optional
soup.find('rdf:li'), soup.find('li'), soup.li

# Any keyword argument can be passed a str, list of strs, regular expression, function or True
soup.find('targetCurrency', string='JPY').parent.value.text

# help(soup.find)

# help(soup.find_all)

# Find petrol buying advice in Brisbane.
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

# Task 4: Find when next low price is going to be


# Solution 4:
print("\n\nSOLUTION 4\n")
# find the next table
table = anchor_bne.parent.find_next("table")
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

# Task 5: Find date of last low price for every city with name ending in 'e'
# Hint see https://regex101.com to test your regular expressions
# import re


# Solution 5: Example of using regular expression when finding
print("\n\nSOLUTION 5\n")
anchors = accc.find_all(id=re.compile(r'petrol-prices-in-\w*e$'))
for anchor in anchors:
    idx = anchor['title'].rfind(' ')
    city = anchor['title'][idx+1:]
    print(f"Last low price in {city} was {anchor.parent.find_next('table').find_all('td')[-5].string}")

# Task 6: From the RBA web site find the full name of currencies IDR and INR
url = "https://www.rba.gov.au/statistics/frequency/exchange-rates.html"


# Solution 6: Example of using a list of strs when finding
# Unfortunately this solution no longer works. See solution after commented out code
print("\n\nSOLUTION 6\n")
# rba_html = BeautifulSoup(urlopen(url), features="html.parser")
# tr = rba_html.find("h2", string="Exchange Rates").find_next("table").find_all("tr")[3]
# print(tr)
# trs = rba_html.find_all("tr", id=['IDR', 'INR'])
# for tr in trs:
#     id = tr['id']
#     th = tr.th
#     print(f"Code: {id}, Currency: {th.string}")

# Data doesn't exist when page is first loaded. It is created later by asynchronous javascript
# copy html from final page manually.
# another option is to use selenium to fetch the html after the javascript has fetched it.
print("\nAfter copying html from RBA manually")
table = """<table class="table-linear table-numeric width100"><caption>Units of Foreign Currencies per Australian Dollar</caption>
<thead><tr><td></td><th class="sub" scope="col">11 Mar 2024</th><th class="sub" scope="col">12 Mar 2024</th><th class="sub" scope="col"><strong>13 Mar 2024</strong></th></tr></thead>
<tbody>
<tr id="USD"><th scope="row">United States dollar</th><td>0.6611</td><td>0.6615</td><td class="highlight">0.6614</td></tr><tr id="CNY"><th scope="row">Chinese renminbi</th><td>4.7536</td><td>4.7479</td><td class="highlight">4.7544</td></tr><tr id="JPY"><th scope="row">Japanese yen</th><td>97.12</td><td>97.50</td><td class="highlight">97.60</td></tr><tr id="EUR"><th scope="row">European euro</th><td>0.6044</td><td>0.6048</td><td class="highlight">0.6055</td></tr><tr id="KRW"><th scope="row">South Korean won</th><td>868.93</td><td>866.18</td><td class="highlight">869.64</td></tr><tr id="SGD"><th scope="row">Singapore dollar</th><td>0.8799</td><td>0.8804</td><td class="highlight">0.8812</td></tr><tr id="INR"><th scope="row">Indian rupee</th><td>54.65</td><td>54.74</td><td class="highlight">54.80</td></tr><tr id="TWD"><th scope="row">New Taiwan dollar</th><td>20.80</td><td>20.78</td><td class="highlight">20.81</td></tr><tr id="MYR"><th scope="row">Malaysian ringgit</th><td>3.0976</td><td>3.0975</td><td class="highlight">3.0997</td></tr><tr id="NZD"><th scope="row">New Zealand dollar</th><td>1.0710</td><td>1.0719</td><td class="highlight">1.0734</td></tr><tr id="THB"><th scope="row">Thai baht</th><td>23.44</td><td>23.49</td><td class="highlight">23.61</td></tr><tr id="GBP"><th scope="row">UK pound sterling</th><td>0.5144</td><td>0.5160</td><td class="highlight">0.5171</td></tr><tr id="VND"><th scope="row">Vietnamese dong</th><td>16300</td><td>16299</td><td class="highlight">16313</td></tr><tr id="IDR"><th scope="row">Indonesian rupiah</th><td>10307</td><td>10313</td><td class="highlight">10301</td></tr><tr id="HKD"><th scope="row">Hong Kong dollar</th><td>5.1697</td><td>5.1749</td><td class="highlight">5.1752</td></tr><tr id="CAD"><th scope="row">Canadian dollar</th><td>0.8916</td><td>0.8914</td><td class="highlight">0.8926</td></tr><tr id="PHP"><th scope="row">Philippines peso</th><td>36.75</td><td>36.60</td><td class="highlight">36.67</td></tr><tr id="TWI_4pm"><th scope="row"><strong>Trade-weighted Index (4pm)</strong></th><td>61.5</td><td>61.5</td><td class="highlight"><strong>61.6</strong></td></tr><tr id="SDR"><th scope="row">Special Drawing Right</th><td>0.4953</td><td>0.4953</td><td class="highlight">0.4956</td></tr>
</tbody>
</table>"""
rba_html = BeautifulSoup(table, features="html.parser")
rba_html
trs = rba_html.find_all("tr", id=['IDR', 'INR'])
for tr in trs:
    id = tr['id']
    th = tr.th
    print(f"Code: {id}, Currency: {th.string}")

# Task 7: From the RBA page showing rates over the last three days, find currencies
# where rate has both increased and decreased over that time period


# Solution 7: Example of using a callable when finding
def procasterate(tag):
    if tag.name != "tr":
        return False
    tds = tag.find_all('td')
    r1 = float(tds[0].string)
    r2 = float(tds[1].string)
    r3 = float(tds[2].string)
    return r1 < r2 > r3 or r1 > r2 < r3


print("\n\nSOLUTION 7\n")
tbody = rba_html.tbody
trs = tbody.find_all(procasterate)
print("Procrastinating Rates")
for tr in trs:
    tds = tr.find_all('td')
    print(f"{tr['id']:7} {tr.th.string:26}, "
          f"r1 {float(tds[0].string):10.4f}, "
          f"r2 {float(tds[1].string):10.4f}, "
          f"r3 {float(tds[2].string):10.4f}")

# Task 8: Find all tags which have an id attribute


# Solution 8: Example of using True when finding
# Also demonstrates that h2 tags don't have ids when page loaded. They are probably added afterwards using javascript
print("\n\nSOLUTION 8\n")
ids = rba_html.find_all(id=True)
for id in ids:
    print(id.name, id['id'])
