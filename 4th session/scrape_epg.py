# Author: Tim

from bs4 import BeautifulSoup

import re

import datetime


# Needs the following in requirements.txt

# beautifulsoup4

# lxml



# Register for EPG feed at http://au.freepg.tv/Register.aspx

# You will get a url sent to you in email

# http://au.freepg.tv/xmltv/oztivo/QLD.Brisbane.gz?UID=...&K=...

# Load in web browser and then save as plain text (unzipped) file QLD.Brisbane.xml in same directory as this one.

# Change first line from <?xml version="1.0" encoding="ISO-8859-1"?> to <?xml version="1.0" encoding="UTF-8"?>



# Load xml into soup and parse using the xml parser from lxml

# using 'with' when opening files ensures file gets automatically closed immediately it is finished with

with open("QLD.Brisbane.xml") as file:

    soup = BeautifulSoup(file, features="xml")



# Example data in soup

#   <programme start="20190112163000 +0000" stop="20190112170000 +0000" channel="7TWO">

#     <title>Sydney Weekender</title>

#     <desc>Features restaurant reviews, accommodation deals, great ideas for travelling, and entertainment in Sydney and around NSW.</desc>

#     <credits>

#       <actor>Mike Whitney</actor>

#     </credits>

#     <category>Magazine</category>

#     <category>Arts and Living</category>

#     <subtitles type="teletext" />

#     <rating><value>G</value></rating>

#     <star-rating>

#       <value>0/10</value>

#     </star-rating>

#   </programme>





# Find all xml tags called <actor> which have a string which ends in 'Smith' or 'smith' or 'Whitney'

my_list = soup("actor", string=re.compile("([Ss]mith|Whitney)$"))



for actor in my_list:

    # Navigate to <programme> tag. <actor>.parent = <credits>, <credits>.parent = <programme>

    prog = actor.parent.parent

    # Convert date time string to human readable form (Brisbane time) by parsing, changing timezone, and then formatting

    start_time_utc = datetime.datetime.strptime(prog["start"], "%Y%m%d%H%M%S %z")

    start_time_aest = start_time_utc.astimezone(datetime.timezone(datetime.timedelta(hours=10)))

    start_time_str = start_time_aest.strftime("%H:%M %a %d-%b-%Y AEST")

    # Print channel and time for all shows using an actor with name of Smith or smith

    print(actor.string, ":", prog.title.string, ": Channel", prog["channel"], ": Time", start_time_str
