"""
MeetUp 017a - Beginners Python Support Sessions 25-Jun-2019

Learning objectives:
    Webscraping - develop algorithm to find latest url

@author D Tim Cummings

Challenge: Webscrape site to find latest url of stoma costs spreadsheet. Read spreadsheet into dataframe
https://www.health.gov.au/internet/main/publishing.nsf/Content/health-stoma-products-utilisation.htm


requirements.txt
beautifulsoup4
xlrd
pandas

"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import datetime

base_url_str = "https://www.health.gov.au/internet/main/publishing.nsf/Content/"
page_url_str = "health-stoma-products-utilisation.htm"
page = urlopen(base_url_str + page_url_str)

soup = BeautifulSoup(page, features="html.parser")

div_read = soup.find(id='read')

lst_a = div_read.find_all("a")
if len(lst_a) == 0:
    raise IOError("Could not find any hyperlinks on SAS Utilisition web page " + base_url_str + page_url_str)
xl_url_str = None
for a in lst_a:
    href = a.get('href')
    if 'xlsx' in href:
        xl_url_str = base_url_str + href
        break

if xl_url_str is None:
    raise IOError("Could not find url for xlsx for any year between 2012 and " + str(datetime.date.today().year))

print(xl_url_str)
df_sas_utilisation = pd.read_excel(xl_url_str, sheet_name="Utilisation")
print(df_sas_utilisation)
