#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 057 - Beginners' Python and Machine Learning - Tue 28 Apr 2020 - dash plotly

https://youtu.be/zxwSezObVkQ

Learning objectives:
- python scripts (not notebooks)
- virtual environments (python or anaconda)
- dash
- plotly.py

@author D Tim Cummings
"""
# Task 1: Setup environment
# - Install Python 3.8 from https://www.python.org/downloads/release/python-382/
#   - Add python to path when installing, or know where it is for later
#   - (3.6 or later should be fine, anaconda also fine)
# - Install Git from https://git-scm.com/download/
# - Install IDE eg PyCharm Community Edition 2020.1 from https://www.jetbrains.com/pycharm/download/
# - Clone repository and setup virtual environment

# I have put commands to be typed on command line in triple-singled quoted strings to ease copy-pasting.
# Following to be typed in Terminal on Mac/Linux or Git-Bash on Windows
r'''
cd ~/PycharmProjects                                        # use projects directory in home directory
git clone https://github.com/timcu/bpaml-dash-graph.git     # copy repository from github to your computer
cd bpaml-dash-graph                                         # change directory into the project directory
git checkout task1                                          # show git repo as at beginning of task 1 

# Create virtual environment
python -m venv venv                         # Windows
python3 -m venv venv                        # Mac or Linux
conda create --name venv-dash-graph python  # Anaconda

# activate virtual environment
source venv/bin/activate                    # Mac or Linux or Windows Git-Bash
conda activate venv-dash-graph              # Anaconda
venv\Scripts\activate.bat                   # Windows command prompt
venv\Scripts\Activate.ps1                   # Windows powershell

# install requirements
pip install wheel                           # Windows Git-Bash
pip install -r requirements.txt             # Windows, Mac or Linux without Anaconda
conda install --name venv-dash-graph --file requirements.txt       # Anaconda

# checkout task 2
git checkout task2
'''
# Task 2: First dash application
# - See https://dash.plotly.com/layout
# - Create a simple layout with a single <h1> and a single <div> element
# - Run the application from the command line (python bpaml_dash_graph.py) or IDE (ctrl-shift-r)
r'''
# Create a branch to commit your changes
git checkout -b mytask2attempt              # -b creates a branch. GUI: VCS > Git > Branches... > New Branch
git commit -a -m "my task 2 solution"       # -a adds all changes before commit. GUI: Click tick in GUI
# Checkout task 3 and compare differences
git checkout task3                          # check out tag called task3
git diff task2 task3                        # show what has changed between task2 and task3. GUI: Log
'''

# Task 3: Dropdown menu for list of countries
# - Code from meetup053 has been added into a class in data_cache.py. Initialise using:
#     import data_cache
#     data = data_cache.DataCache()
# - Get DataFrame from DataCache.df_for_case_type()
# - Get all unique countries from column "Country/Region" in DataFrame
# - Sort the countries in place
# - Create an html.Label with the text "Country"
# - Create a dash_core_components Dropdown with
#     id="input-country",
#     value="" (initial selection),
#     options= list of dictionaries for the countries. "label" is what is shown, "value" is what is returned to app
#         [{"label": "Australia", "value": "Australia"}, {"label": "New Zealand", "value": "New Zealand"}]
'''
# Create a branch to commit your changes
git checkout -b mytask3attempt
git commit -a -m "my task 3 solution"
# Checkout task 4 and compare differences
git checkout task4
git diff task3 task4
'''

# Task 4: Use callbacks on Dropdown menu to change text in div.
# - See https://dash.plotly.com/basic-callbacks
# - Create a html.Div with the initial text empty and an id of "text-selected-country"
# - Create a function which takes the country name and returns "You have selected {country}"
# - Use the @app.callback decorator to call the function when "value" of "input-country" changes
#   and stores result in "children" of "text-selected-country"
'''
# Commit your changes to your own branch and checkout task5
git checkout -b mytask4attempt
git commit -a -m "my task 4 solution"
git checkout task5
'''

# Task 5: Use selected country to filter Dropdown for state
# - Create an html.Label with the text "State/Province"
# - Create a dash_core_components Dropdown with
#     id="input-state",
#     value="" (initial selection),
#     options= list of dictionaries for the states [{"label": state, "value": state}, ...]
# - Use the @app.callback decorator to call a function when "value" of "input-country" changes
#   and stores result in "options" of "input-state"
# - Also change update_text_selected_country() to take two input values. Use function location_name in utilities.py
# - define a function in utilities.py called location_name(country=None, state=None) which returns location name
'''
# Commit your changes to your own branch and checkout task6
git checkout -b mytask5attempt
git commit -a -m "my task 5 solution"
git checkout task6
'''

# Task 6: Draw covid days doubling chart based on selected country and state
# - figure_cumulative_doubling has been provided from meetup053
# - add a dash_core_components Graph object with id="graph-doubling-days" and a figure=fig_for_location(data=data)
# - define a function update_graph(country, state) which returns a figure based on selected country and state
# - Use the @app.callback decorator to call the function when "value" of "input-country" or "input-state" changes
'''
# Commit your changes to your own branch and checkout task7
git checkout -b mytask6attempt
git commit -a -m "my task 6 solution"
git checkout task7
'''

# Task 7: Provide an input and a callback for Averaged Days select between 1 and 10
# - add a dash_core_components Slider object with id="input-averaged-days", min, max, value, marks {"1":"1", "2":"2", ...}
# - modify update_graph to take an additional argument averaged_days
'''
# Commit your changes to your own branch and checkout task8
git checkout -b mytask7attempt
git commit -a -m "my task 7 solution"
git checkout task8
'''

# Task 8: Provide a callback for Starting Number
# - add a dash_core_components Input object with id="input-num-start", min=1, value=100, type="number"
# - modify update_graph to take an additional argument num_start
# - if num_start is blank then use default value in fig_for_location function
'''
# Commit your changes to your own branch and checkout task9
git checkout -b mytask8attempt
git commit -a -m "my task 8 solution"
git checkout task9
'''

# Task 9: Provide a callbacks for Case Type and Graph Type
# - add dash_core_components RadioItems for id="input-case-type" and id="input-yaxes-type"
# - default case-type is "confirmed", default yaxes-type is "log"
# - options for case_type [{"label": "confirmed", "value": "confirmed"}, ] for confirmed, recovered, deaths
# - options for yaxes-type are linear or log
# - labelStyle={"display": "inline-block"}
# - Divide input fields into 3 divs with style={"breakInside": "avoid"}, all inside one div with style={"columnCount": 3}
'''
# Commit your changes to your own branch and checkout master to see final solution
git checkout -b mytask9attempt
git commit -a -m "my task 9 solution"
git checkout master
'''
