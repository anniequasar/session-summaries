Webscraping is a way of extracting data from a website.

There are a few different library options to choose from such as requests and scrapy.
However, we have chosen to scrape using beautifulsoup4.

To explore ways of using beautifulsoup, go directly to the documentation:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

In this session the aim was to scrape the website https://spreets.com.au/deals/sydney and to get the python console to only print a link to deals with greater than 70% off.

see webscraping.py

First go to the website https://spreets.com.au/deals/sydney and right click to Inspect Element.

To get a handle on the tag terms a useful reference can be found here:

https://www.w3schools.com/tags/default.asp

In the top left corner of Inspect Element, there is a small mouse icon that allows you to hover over an element on the website and the corresponding html cde is highlighted accordingly.

Using this, we were able to identify the tags correlated with the deal %

To make the soup:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/#making-the-soup


We then used the function soup.find_all

https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all

To get beautiful soup to extract the link from the website, we used the function a.get("href"):

    From Beautifulsoup doucmentation:

    One common task is extracting all the URLs found within a page’s <a> tags:

    for link in soup.find_all('a'):
    print(link.get('href'))
    # http://example.com/elsie
    # http://example.com/lacie
    # http://example.com/tillie
