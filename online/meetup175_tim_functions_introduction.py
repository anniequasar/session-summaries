#!/usr/bin/env python3
r"""MeetUp 175 - Beginners' Python and Machine Learning - 01 Mar 2023 - Getting Started 3b

Learning objectives:
- Interactive python
- Introduction to coding
- Functions

Links:
- Colab:   https://colab.research.google.com/drive/1qsw1g8yX1_bGmI2iIbIope8Mq6VQgXur
- Youtube: https://youtu.be/6jVpG_vsYf4
- Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/291695159/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

Install Software
- Use a Google account to go to https://colab.research.google.com
 - Doesn't need Python installed on your computer
 - Great for interactive use and data science
 - Not so good for scripting and building apps
- Install Python 3.11.2 from https://www.python.org/downloads/
 - necessary for running python on your computer 
 - run the following from command line to set up and run virtual environment Mac or Linux

    python3 -m venv venv175
    source venv175/bin/activate
    pip install plotly pytz pandas

 - run the following from command line to set up and run virtual environment Windows

    py -m venv venv175
    venv175\Scripts\Activate
    pip install plotly pytz pandas

- Alternatively can install anaconda which includes many third party libraries including plotly
- Integrated Development Environment (IDE), easier to write programs
 - PyCharm Community Edition 2022.3 from https://www.jetbrains.com/pycharm/download/
 - Visual Studio Code from https://code.visualstudio.com

For those interested in my children's Python coding course see https://pythonator.com (makes Python coders out of gamers). This course would be good for adults too if they could play Minecraft or Minetest as competently as the children! It requires the EduTools plugin for PyCharm https://www.jetbrains.com/help/education/install-edutools-plugin.html?section=PyCharm

There are different ways to write Python. 
The language is the same in every case, but the ways users
interact with the program is different in each case.
Today we are using Jupyter Notebooks on Google Colab. 
Jupyter Notebooks are an extension of IPython (Interactive Python). Every exercise could also be done in Python. Python version of this notebook available in https://github.com/anniequasar/session-summaries/online

Jupyter Notebooks are a great way to learn because you see the results immediately. They can also be great for data science. However, they are not suited for some Python programs such as web applications, database apps, desktop apps, GUI apps, operating system services.

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text
- use ? or Help menu for help
- see Tools menu > Keyboard shortcuts
"""

# comments in code cells start with a '#'. They don't do anything. They are just there for you to read.
# try executing ? to bring up IPython help (press <shift><enter> while this cell is selected)
# If you are using Python Console rather than IPython then use help()
# ?

# Coding is all about writing commands for a computer to follow
# The only commands a computer can do are rather simple but it can do them very quickly
# For example to display something, use the print() command
print("Beginners' Python And Machine Learning 175")
print("Printing numbers")
print(5 + 3)

# In IPython or Python Console we don't even need the print() to display data
# In Python scripts (like this one) the following line does nothing
4 + 5

# Commands in a cell are executed sequentially
print(4)
print(3)

# Unfortunately in IPython only the data on the last line is displayed so use print() if you need more
2
1

# Assume we have two variables x and y, and y is calculated from a formula of x
x = 3
y = x * x - 4 * x + 4
print("\nPrint using f-string")
print(f"{x=}, {y=}")

# We can calculate y for different values of x and put all the x and y values into lists
print("\nPrint from a loop")
lst_x = []
lst_y = []
for i in range(41):
    x = i / 10
    y = x * x - 4 * x + 4
    lst_x.append(x)
    lst_y.append(y)
    if i < 10:
        print(f"x={x}, y={y}")

print(f"{lst_x=}")
print(f"{lst_y=}")

# We can use a third party library to plot x and y in a scatter chart
# plotly.express requires pandas so make sure you installed pandas also
import plotly.express as px

fig = px.line(x=lst_x, y=lst_y)
fig.show()

# It becomes cumbersome (and error prone) to type "x * x - 4 * x + 4" every time we want to calculate y 
# so we store it in a function
# def and return are keywords
# f is the function name
# a is the argument
def f(a):
    return a * a - 4 * a + 4

# To call the function we use the function name followed by parentheses. 
# If the function has arguments they should be supplied within the parentheses
x = 5
y = f(x)

# Task 1: Call the function using an argument of 2.5

# Solution 1: Calling the function and storing the result in a variable. Printing the answer using an f-string
x = 2.5
y = f(x)
print(f"\nSolution 1: f({x})={y}")

# Python is dynamically typed language. We can call our function with any data type that understands *, -, + operators
x = 3
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")
x = 3.
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")

# Let's create a function to make printing return value and type easier
def print_function_result(fun, x):
    y = fun(x)
    print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")

x = 3
print_function_result(f, x)
x = 3.
print_function_result(f, x)

# Task 2: Try calling function with argument of different data type eg decimal.Decimal("1.1") from standard library decimal (which needs to be imported)
import decimal

print("\nSolution 2: Can also import class Decimal from decimal library")
from decimal import Decimal
x = Decimal("1.1")
print_function_result(f, x)
x = 1.1
print_function_result(f, x)

# Task 3: rewrite our loop from before which created lst_x and lst_y but this time calling the function

print("\nSolution 3: Using a function and list comprehension to create lists")
lst_x = [i/10 for i in range(41)]
lst_y = [f(i/10) for i in range(41)]
print(f"{lst_x=}")
print(f"{lst_y=}")

# Built in functions are just like functions we create. 
# They are called by entering their name followed by parentheses 
# Any arguments need to be included in the parentheses
print()  # with no arguments prints a blank line to the console

print("hello")  # with one argument prints a display view of the value on a line by itself

# Task 4: What other built-in functions have we already used?



# Solution 4
# range(stop)  # one argument, stop value when iterating from 0 upwards
# type(val)    # one argument, value of which we want to know the current type

# px.line(x=lst_x, y=lst_y)  # two named arguments. Not a built-in function. Comes from third party library so needs to be installed then imported

# Decimal(value as str)  # This is not really a function. Decimal is a class and Decimal() is the constructor. As part of creating instance it may call a function
# Decimal is not built-in but part of a standard library so it can be imported without installing.

# By convention classes use TitleCase while function names use lower_case_with_underscores. Not followed 100%

# Functions don't need to have arguments
import datetime  
# datetime is a standard python library but needs to be imported to use it
# datetime.datetime is a class in the datetime library
# datetime.datetime.now() calls a function in the class which returns an object of type datetime
# datetime.datetime.now().strftime() calls a function on the now object of type datetime and formats it the way specified

def show_time():
    print(datetime.datetime.now().strftime("Year: %Y, Month %m, Day %d, Hour: %H, Minute: %M, Second: %S, Microsecond: %f"))

# To call the function we still need to provide the parentheses
show_time()

# Functions can return values
import pytz  
# pytz is not a standard python library.
# dateutil.tz recommended over pytz but doesn't provide list of all timezones
# Colab includes all the python standard libraries + those in anaconda

def timezone_regions():
    regions = set()
    for tz in pytz.all_timezones:
        if "/" in tz:
            idx = tz.index("/")
            regions.add(tz[:idx])
        else:
            regions.add(tz)
    sorted_regions = sorted(regions)
    return sorted_regions


# Convert set of regions into a sorted list
lst_regions = timezone_regions()
print(lst_regions)

# Task 5: Define a function which takes one argument, region, and returns the timezones in that region

print("\nSolution 5: Function returning timezones for a region")
def region_for_timezone(tz):
    """Extracts the region from a timezone
    
    By using the same function in timezones_for_region and timezone_regions we
    improve the consistency of data.
    Example: region_for_timezone('Australia/ACT') returns 'Australia'"""
    # First str in a function is the docstring.
    if "/" in tz:
        idx = tz.index("/")
        return tz[:idx]
    else:
        return tz 

def timezones_for_region(region):
    """Return all timezones in a region."""
    # Using region_for_timezone('NZ-CHAT') == 'NZ' more reliable than 'NZ-CHAT'.startswith('NZ')
    # The following method of creating a list is called list comprehension
    return [tz for tz in pytz.all_timezones if region_for_timezone(tz) == region]

def timezone_regions():
    """Return all regions which have a timezone in pytz"""
    # The following method uses set comprehension to create a set
    return sorted({region_for_timezone(tz) for tz in pytz.all_timezones})

print(timezones_for_region("Australia"))
print(timezones_for_region("NZ"))
print(timezones_for_region("Etc"))
print(timezones_for_region("UCT"))
print(timezone_regions())
# Try the following command to see help on our custom function
# help(region_for_timezone)

# Be careful when using Etc timezones
for tz in ["UTC", "Australia/Brisbane", "Etc/GMT+10", "Etc/GMT-10"]:
    print(f"Timezone: {tz:20} Current time: {datetime.datetime.now(pytz.timezone(tz))}")

# help() can be called on built-in functions
# help(print)

# Arguments to a function can have default values eg sep, end, file, flush
# Arguments to a function can be either or both of by order or by name 
# eg sep is first named argument
# all the preceding arguments are unnamed and depend on order only

# You will normally write functions with named arguments
# which will accept both by order or by name
def total_seconds(minutes=0, seconds=0):
    """returns the total number of seconds in the given minutes and seconds

    minutes: the number of minutes (default 0)
    seconds: the number of seconds (default 0)"""
    return minutes * 60 + seconds

print(f"total_seconds(32, 15)={total_seconds(32, 15)}. (calling by order)")
print(f"total_seconds(seconds=15, minutes=32)={total_seconds(seconds=15, minutes=32)}. (calling by name)")
print(f"total_seconds(32, seconds=15)={total_seconds(32, seconds=15)}. (calling by order and name. order has to come first)")

# Task 6: Expand total_seconds to take three arguments hours, minutes, seconds

print("\nSolution 6: Three named arguments to total_seconds")
def total_seconds(hours=0, minutes=0, seconds=0):
    """returns the total number of seconds in the given hours, minutes and seconds

    hours: the number of hours(default 0)
    minutes: the number of minutes (default 0)
    seconds: the number of seconds (default 0)"""
    return hours * 3600 + minutes * 60 + seconds

print(f"total_seconds(0, 32, 15)={total_seconds(0, 32, 15)}. (calling by order)")
print(f"total_seconds(seconds=15, minutes=32)={total_seconds(seconds=15, minutes=32)}. (calling by name)")
print(f"total_seconds(0, 32, seconds=15)={total_seconds(0, 32, seconds=15)}. (calling by order and name. order has to come first)")
print(f"total_seconds(seconds=15, hours=1, minutes=32)={total_seconds(seconds=15, hours=1, minutes=32)}. (calling by name)")

# Task 7: Define a function which converts temperature in celsius to fahrenheit
# f = c * 1.8 + 32

print("\nSolution 7: Convert celsius to fahrenheit")
def fahrenheit(celsius):
    """Convert temperature in celsius to fahrenheit"""
    return celsius * 1.8 + 32

for c in [0, 100, -40]:
    print(f"{c:7.2f}°C is equivalent to {fahrenheit(c):7.2f}°F")
