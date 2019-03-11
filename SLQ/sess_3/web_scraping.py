from bs4 import BeautifulSoup

from urllib.request import urlopen

page = urlopen("https://spreets.com.au/deals/sydney")

soup = BeautifulSoup(page, features="html.parser")


# a for loop that prints all the deals greater than 70% and its link from the website onto a new line

divlist = soup.find_all("div", "deal-list-wrapper")

for div in divlist:

    em = div.em

    a = div.a

    if em and "%" in em.string:

        percentage = int(em.string[6:8])

        if percentage > 70:

            print(em.string)

            print("here is a link to the deal")

            print(a.get("href"))
