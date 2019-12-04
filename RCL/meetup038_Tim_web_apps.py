
"""
Created on Wed Dec  4 17:55:14 2019
meetup038_Tim_web_applications

On Tuesday night (26th Nov) we looked at creating web applications using Flask.

We will be using git so make sure you have git installed
https://git-scm.comFor pre-reading please attempt the tutorial at

https://flask.palletsprojects.com/en/1.1.x/tutorial/I  will show you how to run the sas-select application developed by students at bpss.

Then we will start developing an application to browse the Prime Ministers of Australia.# How to run sas-select app:

git clone https://github.com/timcu/sas-select.git

cd sas-select

python3 -m venv venv

# Mac or Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

pip install -r requirements.txt

flask init-db

flask run

# Load data using http://localhost:5000/fetch-data

# Test sas-select app

python -m pytest# Prime Ministers Database App

git clone https://github.com/timcu/bpss-prime-minister.git

git checkout task1


Challenge 1: Add a page for view_prime_ministers
Challenge 2: List all people in database in list_person.html
Challenge 3: Show list of recreations in view_person.html
Challenge 4: Add functionality for view_deputy_prime_ministers
Challenge 5: Add authentication to application so users can log in.
Challenge 6: Keep search form populated after clicking search button

"""

