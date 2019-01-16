# After the third session, members were asked to write their own scraping script
# I chose to investigate how to scrape information from a webpage and to extract that information into a .csv file
# To do this I used pandas

from bs4 import BeautifulSoup

from urllib.request import urlopen

page = urlopen("http://www.weatherzone.com.au/qld/brisbane")

soup = BeautifulSoup(page, features="html.parser")

max_temp_list = []
for span in soup.findAll("span", "text_tempmax"):
    max_temp = span.text
    max_temp_list.append(max_temp)
    
location_list = []
for span in soup.findAll("a", "trigger"):
    location = span.text
    location_list.append(location)
    
#build a dictionary [key = columns, values = rows]

out_dict = {'locations':location_list, 'max_temps':max_temp_list}

import pandas as pd

df = pd.DataFrame(out_dict)

print(df)

df.to_csv('myfile.csv')
