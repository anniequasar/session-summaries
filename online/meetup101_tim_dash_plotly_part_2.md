# Beginners' Python and Machine Learning
This file describes the setup and tasks for meetups 57, 100, 101 and youtube videos 
- https://youtu.be/zxwSezObVkQ   (macOS: tasks 1-9, meetup 57)
- https://youtu.be/78RaVmb-c30   (Windows: tasks 1-6, meetup 100)
- https://youtu.be/0vcT2tB7iZ4   (Windows: tasks 7-10, meetup 101)

The project will show how to create an interactive chart plotting cases of COVID-19 by country or state using live data from Johns Hopkins.

## Task 1: Setup environment
- Install Python 3.9.2 from https://www.python.org/downloads/release/python-392/
  - Add python to path when installing, or know where it is for later
  - (3.6 or later should be fine, anaconda also fine) 
- Install Git 2.31 from https://git-scm.com/download/
- Install IDE eg PyCharm Community Edition 2020.3.5 from https://www.jetbrains.com/pycharm/download/
- Clone repository and setup virtual environment

### Command line - clone git repository
    cd ~/PycharmProjects
    git clone https://github.com/timcu/bpaml-dash-graph.git
    cd bpaml-dash-graph
    git checkout challenge1

### PyCharm - clone git repository
- Get from VCS >
  - URL = https://github.com/timcu/bpaml-dash-graph.git
- Git > Branches... > Checkout tag or revision
  - challenge1

### Command line - create virtual environment
    python -m venv venv                         # Windows
    python3 -m venv venv                        # Mac or Linux
    conda create --name venv-dash-graph python  # Anaconda

### Command line - Activate virtual environment
    source venv/bin/activate                    # Mac or Linux
    conda activate venv-dash-graph              # Anaconda
    source venv/Scripts/activate                # Windows Git-Bash
    venv\Scripts\activate.bat                   & :: Windows command prompt
    venv\Scripts\Activate.ps1                   & :: Windows powershell

### Command line - Install requirements
    pip install -r requirements.txt             # Windows, Mac or Linux without Anaconda
    conda install --name venv-dash-graph --file requirements.txt       # Anaconda

### PyCharm + Python - create and activate virtual environment and install requirements
- PyCharm > Preferences > Project > Python Interpreter
  - Project Interpreter > Show all > +
    - Virtualenv: New environment
      - Location: ./venv
      - Base Interpreter: ...bin/python3.9 or AppData\Local\Programs\Python\Python39\python.exe

### PyCharm + Anaconda + Windows - create and activate virtual environment and install requirements
- PyCharm > Preferences > Project > Python Interpreter
  - Project Interpreter > Show all > +
    - Conda: New environment
      - Location: ~\Anaconda3\envs\venv-dash-graph       # ~ means home directory
      - Python version: 3.9
      - Conda executable: ~\Anaconda3\Scripts\conda.exe  # ~ means home directory

### Tasks
Tasks are listed in file tasks.txt and are visible on each branch. 
Tasks are listed in README.md in master branch but not on other branches.

### Final step of task 1: checkout task 2 by switching to git branch challenge2

Command line:

    git switch challenge2  

PyCharm GUI: 
- Git > Branches... > Checkout tag or revision > challenge2

### Task 2: First dash application
- See https://dash.plotly.com/layout
- Create a simple layout with a single `<h1>` and a single `<div>` element
- Run the application from the command line (python bpaml_dash_graph.py)
- Run the application from PyCharm using ctrl-shift-F10 (PC) or ctrl-shift-r (macOS)
- Create a branch to commit your changes
  
      git checkout -b mytask2attempt              # -b creates a branch. GUI: Git > Branches... > New Branch
      git commit -a -m "my task 2 solution"       # -a adds all changes before commit. GUI: Commit tab (top left).
  
  - If GUI commit tab is not visible in top left then might need to turn on new behaviour in PyCharm. GUI: File > Settings... > Version Control > Commit > Non-modal commit

- Checkout task 3 and compare differences
  
      git checkout challenge3                     # check out branch called challenge3 (similar to switch)
      git diff challenge2 challenge3              # show what has changed between challenge2 and challenge3. GUI: Log

### Task 3: Dropdown menu for list of countries
- Code from meetup053 has been added into a class in data_cache.py. Initialise using:
  
      import data_cache
      data = data_cache.DataCache()
  
- Get DataFrame from DataCache.df_for_case_type()
- Get all unique countries from column "Country/Region" in DataFrame
- Sort the countries in place
- Create an `html.Label` with the text "Country"
- Create a dash_core_components `Dropdown` with
  - id="input-country",
  - value="" (initial selection),
  - options= list of dictionaries for the countries. "label" is what is shown, "value" is what is returned to app
    - [{"label": "Australia", "value": "Australia"}, {"label": "New Zealand", "value": "New Zealand"}]
  
- Create a branch to commit your changes
  
      git checkout -b mytask3attempt
      git commit -a -m "my task 3 solution"
  
- Checkout task 4
  
      git switch challenge4

### Task 4: Use callbacks on Dropdown menu to change text in div.
- See https://dash.plotly.com/basic-callbacks
- Create a `html.Div` with the initial text empty and an id of "text-selected-country"
- Create a function which takes the country name and returns "You have selected {country}"
- Use the `@app.callback` decorator to call the function when "value" of "input-country" changes
  and stores result in "children" of "text-selected-country"
- Commit your changes to your own branch and checkout challenge 5
  
      git checkout -b mytask4attempt
      git commit -a -m "my task 4 solution"
      git switch challenge5
  
### Task 5: Use selected country to filter Dropdown for state
- Create an `html.Label` with the text "State/Province"
- Create a dash_core_components `Dropdown` with
  - id="input-state",
  - value="" (initial selection),
  - options= list of dictionaries for the states [{"label": state, "value": state}, ...]
- Use the `@app.callback decorator` to call a function when "value" of "input-country" changes
  and stores result in "options" of "input-state"
- Define a function in `utilities.py` called location_name(country=None, state=None) which returns location name
- Also change `update_text_selected_country()` to take two input values. Use function `location_name` in `utilities.py`
- Commit your changes to your own branch and checkout task6
  
      git checkout -b mytask5attempt
      git commit -a -m "my task 5 solution"
      git switch challenge6

### Task 6: Draw covid days doubling chart based on selected country and state
- `figure_cumulative_doubling` has been provided from meetup053
- add a dash_core_components `Graph` object with id="graph-doubling-days" and a figure=fig_for_location(data=data)
- define a function `update_graph(country, state)` which returns a figure based on selected country and state
- Use the `@app.callback` decorator to call the function when "value" of "input-country" or "input-state" changes
- Commit your changes to your own branch and checkout 7

      git checkout -b mytask6attempt
      git commit -a -m "my task 6 solution"
      git switch challenge7

### Task 7: Provide an input and a callback for Averaged Days select between 1 and 10
- add a dash_core_components `Slider` object with id="input-averaged-days", min, max, value, marks {"1":"1", "2":"2", ...}
- modify `update_graph` to take an additional argument `averaged_days`
- Commit your changes to your own branch and checkout challenge 8

      git checkout -b mytask7attempt
      git commit -a -m "my task 7 solution"
      git switch challenge8

### Task 8: Provide a callback for Starting Number
- add a dash_core_components `Input` object with id="input-num-start", min=1, value=100, type="number"
- modify `update_graph` to take an additional argument `num_start`
- if `num_start` is blank then use default value in `fig_for_location` function
- Commit your changes to your own branch and checkout challenge 9

      git checkout -b mytask8attempt
      git commit -a -m "my task 8 solution"
      git switch challenge9

### Task 9: Provide a callbacks for Case Type and Graph Type
- add dash_core_components `RadioItems` for id="input-case-type" and id="input-yaxes-type"
- default `case_type` is "confirmed", default `yaxes_type` is "log"
- options for `case_type` [{"label": "confirmed", "value": "confirmed"}, ] for confirmed, recovered, deaths
- options for `yaxes_type` are linear or log
- labelStyle={"display": "inline-block"}
- Divide input fields into 3 divs with style={"breakInside": "avoid"}, all inside one div with style={"columnCount": 3}
- Commit your changes to your own branch and checkout challenge 10

      git checkout -b mytask9attempt
      git commit -a -m "my task 9 solution"
      git switch challenge10

### Task 10: Add "active" as another case type. Add checkboxes for doubling guides
- `data_cache.py` has been modified to accept "active" as a case type (from meetup096). 
- `figure_cumulative_doubling.py` has been modified to accept list of days for drawing doubling guides
- https://dash.plotly.com/dash-core-components/checklist
- add case type "active" to RadioItems "input-case-type"
- add dash_core_components CheckList for id="input-doubling-guides"
- options for doubling guides [{"label": str(days), "value": days}, ] for 4, 5, 6, 8, 10, 12
- use inline-block labels
- initial value [6, 12]
- Commit your changes to your own branch and checkout master to see the solution

      git checkout -b mytask10attempt
      git commit -a -m "my task 10 solution"
      git switch master

