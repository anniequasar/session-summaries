#!/usr/bin/env python3
r"""MeetUp 088 - Beginners' Python and Machine Learning - 01 Dec 2020 - Getting Started 3

Youtube: https://youtu.be/JCsvuYstioY
Colab:   https://colab.research.google.com/drive/1j89Xozn7apvOiuFKyG95d3HtKVnN_I20
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online
MeetUp:  https://www.meetup.com/beginners-python-machine-learning/events/274704574/

Learning objectives:
- Interactive python
- Introduction to coding
- Functions, branching, looping

@author D Tim Cummings

Challenge 1: Install Software
- Use a Google account to go to https://colab.research.google.com
 - Doesn't need Python installed on your computer
 - Great for interactive use and data science
 - Not so good for scripting and building apps
- Install Python 3 from https://www.python.org/downloads/
 - necessary for running python on your computer
 - alternatively can install anaconda which includes many third party libraries
- PyCharm Community Edition 2020.2.3 from https://www.jetbrains.com/pycharm/download/
 - Integrated Development Environment (IDE)
 - Easier to write programs

For those interested in my children's Python coding course see https://pythonator.com
(makes Python coders out of gamers). This course would be good for adults too if they
could play Minecraft or Minetest as competently as the children! It requires the
EduTools plugin for PyCharm
https://www.jetbrains.com/help/education/install-edutools-plugin.html?section=PyCharm

There are different ways to write Python.
The language is the same in every case, but the ways users
interact with the program is different in each case.
Today we are using Jupyter Notebooks on Google Colab.
Jupyter Notebooks are an extension of IPython (Interactive Python).
Every exercise could also be done in Python. Python version of this
notebook available in https://github.com/timcu/bpaml-sessions/online

Jupyter Notebooks are a great way to learn because you see the results immediately.
They can also be great for data science. However, they are not suited for some Python
programs such as web applications, database apps, desktop apps, GUI apps, operating
system services.

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text
- use ? or Help menu for help
- see Tools menu > Keyboard shortcuts
"""
import datetime
import pytz

# comments in code cells start with a '#'. They don't do anything. They are just there for you to read.
# try executing ? to bring up IPython help (press <shift><enter> while this cell is selected)
# If you are using Python Console rather than IPython then use help()

# Uncomment following line if using IPython
# ?

# Coding is all about writing commands for a computer to follow
# The only commands a computer can do are rather simple but it can do them very quickly
# For example to display something, use the print() command
print(5)

# In IPython or Python Console we don't even need the print() to display data

# Uncomment following line if using IPython
# 4

# Commands in a cell are executed sequentially
print(4)
print(3)

# Unfortunately in IPython only the data on the last line is displayed so use print() if you need more

# Uncomment following lines if using IPython
# 2
# 1

# Task 1: In the empty cell below write a Python program to count down from five to zero on separate lines

# Solution 1:
print("Solution 1: Counting")
print("five")
print("four")
print("three")
print("two")
print("one")
print("zero")

# Solution 1 shows an alternative way of solving task 1. It shows that when
# using print() with text rather than numbers we need to surround the text with
# quotation marks. Text data is called a string. In Python that is str.
type("abc")

# The numbers we have been using so far have been integers or whole numbers.
# In Python they are called int
type(123)

# Python can also work with real numbers that have a decimal fraction
# They are called floating point numbers or, in Python, float
type(123.45)

# Python can do arithmetic on numbers using operators + - * / // % **
# See Getting Started 1 for more details
# IPython is great for evaluating arithmetic expressions

# Uncomment following line if using IPython
# 1 * 2 + 3 * 4

# We can also save results from expressions in memory locations
# These memory locations are called variables because the values can be changed
# Variables can be named whatever you like. Just avoid the 35 Python keywords.
# Also good if you avoid using names of libraries, functions and data types.
a = 5
print(a)

b = 2**32
c = a * b
print(a, b, c)

# Programming would be very cumbersome if we had to type a line for every command we wanted to execute.
# Repeated commands can be put in a loop
# Loops start with 'while' or 'for'
# Commands to be repeated are called a code block and are indented (4 spaces)
# 'for' loops have a variable which changes value every time through loop
# All the possible values are given after the 'in' keyword
# += means add to the current value
total = 0
for z in (5, 4, 3, 2, 1, 0):
    total += z
    print(z)
print("The total of the above numbers is", total)

# Task 2: Rewrite the loop to showing a running total as it loops through all the numbers

# Solution 2: Shows how to use a 'while' loop rather than a 'for' loop
# 'while' loops have a True/False condition that must be True for the loop to continue looping
# If you don't understand what is happening add more print() commands to log intermediate results
print("Solution 2: Running Total")
total = 0
z = 5
while z >= 0:
    total += z
    print("number", z, "running total", total)
    z -= 1

# Task 3: Write a loop which counts up from 1 to 5 and displays the factorial of each number as it goes
# factorial(n) = 1 x 2 x 3 x ... x (n-2) x (n-1) x n

# Solution 3:
# range(start, stop, [step]) counts from start up/down to but not including stop by step each time
print("Solution 3: Factorials")
factorial = 1
for z in range(1, 20):
    factorial *= z
    print("number", z, "factorial", factorial)

# Task 4: Display the first 20 numbers in the fibonacci sequence
# f1 = 1, f2 = 1, fn = fn-1 + fn-2
# 1, 1, 2, 3, 5, 8, 13

# Solution 4:
# Multiple assignment statements can be done on one line
print("Solution 4: Fibonacci Sequence")
f1, f2 = 1, 1
for i in range(18):
    print(f1, end=' ')
    f1, f2 = f2, f1 + f2
print(f1, f2)

# Task 5: Count down in steps of 2.25 from 10.5 to -3 inclusive

# Solution 5:
print("Solution 5: Counting down")
# range can only work with integers
# fractions are 21/2 to -3 step -9/4
lcd = 4  # lowest common denominator
start_numerator = int(10.5 * lcd)
stop_numerator = int(-3 * lcd)
step_numerator = int(-2.25 * lcd)
for x in range(start_numerator, stop_numerator - 1, step_numerator):
    print(f"{x/lcd :7.2f}")

# Problem with using floating point step
# Fractions where the denominator is a power of two can be represented exactly by float
# All other denominators will leave a small error when converted to binary.
# Count down from 1 to 0 inclusive in 0.1 steps
x = 1.0
while x >= 0:
    print(x)
    x -= 0.1

# Using range with integer arguments
lcd = 10
for x in range(10, -1, -1):
    print(x/lcd)

# list data type is an ordered collection of data values of any type
my_list = [0, 2, 4, 6, 8, 10]
print(my_list)

# lists can be created using a loop
# example of using range() with only one argument. start defaults to 0
my_list = []
for x in range(30):
    my_list.append(2 * x)
print(my_list)

# Task 6: Rewrite the following code using nested loops
print("Examples of range()")
print("range(4) ", end=' ')
for i in range(4):
    print(i, end=' ')
print()
print("range(2, 5) ", end=' ')
for i in range(2, 5):
    print(i, end=' ')
print("\nrange(3, 14, 4) ", end=' ')
for i in range(3, 14, 4):
    print(i, end=' ')
print("""
range(12, 3, -3) """, end=' ')
for i in range(12, 3, -3):
    print(i, end=' ')
r = range(12, 3, -1)
print(f"\n{r} ", end=' ')
for i in r:
    print(i, end=' ')
r = range(12, 3)
print(f"\n{r} ", end=' ')
for i in r:
    print(i, end=' ')
print()

print("Solution 6: Using a loop to display different forms of range")
# tuple (1, 2, 3) is a read only version of list [1, 2, 3]
tpl_ranges = ([4], [2, 5], [3, 14, 4], [12, 3, -3], [12, 3, -1], [12, 3])
for range_args in tpl_ranges:
    # *range_args means explode the list and place each item in the ordered argument positions
    r = range(*range_args)
    print(f"{str(r):20}", end=' ')
    for i in r:
        print(i, end=' ')
    print()


# Functions can be used for lines of code which need to be repeated and called from anywhere in program
def display_range(rng):
    print(f"{str(rng):20}", end=' ')
    for j in rng:
        print(j, end=' ')
    print()


# Call the function using the function name with parentheses. Put arguments inside parentheses
display_range(range(4))
display_range(range(12, 3, -1))

# Task 7: rewrite our loop from before but this time calling the function

print("Solution 7: Using a function in a loop to display different forms of range")
# Notice how Jupyter Notebooks remember tpl_ranges and display_range from before
for range_args in tpl_ranges:
    display_range(range(*range_args))

# Functions don't need to have arguments

# datetime is a standard python library but needs to be imported to use it
# see 'import datetime' at top of file
# datetime.datetime is a class in the datetime library
# datetime.datetime.now() calls a function in the class which returns an object of type datetime
# datetime.datetime.now().strftime() calls a function on the now object of type datetime and formats it the way specified


def show_time():
    print(datetime.datetime.now().strftime("Year: %Y, Month %m, Day %d, Hour: %H, Minute: %M, Second: %S, Microsecond: %f"))


# To call the function we still need to provide the parentheses
show_time()

# Functions can return values
# pytz is not a standard python library.
# see 'import pytz' at top of file
# Colab includes all the python standard libraries + those in anaconda


def timezone_regions():
    regions = set()
    for timezone in pytz.all_timezones:
        # if is like while but only executes once
        if "/" in timezone:
            idx = timezone.index("/")
            regions.add(timezone[:idx])
        else:
            regions.add(timezone)
    sorted_regions = sorted(regions)
    return sorted_regions


# Convert set of regions into a sorted list
lst_regions = timezone_regions()
print(lst_regions)

# Task 8: Define a function which takes one argument, region, and returns the timezones in that region

print("Solution 8: Function returning timezones for a region")


def region_for_timezone(timezone):
    """Extracts the region from a timezone

    By using the same function in timezones_for_region and timezone_regions we
    improve the consistency of data.
    Example: region_for_timezone('Australia/ACT') returns 'Australia'"""
    # First str in a function is the docstring.
    if "/" in timezone:
        idx = timezone.index("/")
        return timezone[:idx]
    else:
        return timezone


def timezones_for_region(region):
    """Return all timezones in a region."""
    # Using region_for_timezone('NZ-CHAT') == 'NZ' more reliable than 'NZ-CHAT'.startswith('NZ')
    # The following method of creating a list is called list comprehension
    return [timezone for timezone in pytz.all_timezones if region_for_timezone(timezone) == region]


def timezone_regions():
    """Return all regions which have a timezone in pytz"""
    # The following method uses set comprehension to create a set
    return sorted({region_for_timezone(timezone) for timezone in pytz.all_timezones})


print(timezones_for_region("Australia"))
print(timezones_for_region("NZ"))
print(timezones_for_region("Etc"))
print(timezones_for_region("UCT"))
print(timezone_regions())
help(region_for_timezone)

# Be careful when using Etc timezones
for tz in ["UTC", "Australia/Brisbane", "Etc/GMT+10", "Etc/GMT-10"]:
    print(f"Timezone: {tz:20} Current time: {datetime.datetime.now(pytz.timezone(tz))}")

help(print)

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

# Task 9: Expand total_seconds to take three arguments hours, minutes, seconds

print("Solution 9: Three named arguments to total_seconds")


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

# Task 10: Define a function which converts temperature in celsius to fahrenheit
# f = c * 1.8 + 32

print("Solution 10: Convert celsius to fahrenheit")


def fahrenheit(celsius):
    """Convert temperature in celsius to fahrenheit"""
    return celsius * 1.8 + 32


for c in [0, 100, -40]:
    print(f"{c:7.2f}°C is equivalent to {fahrenheit(c):7.2f}°F")

# Task 11: Define a function which converts temperature in celsius or rankine to fahrenheit
# f = r - 459.67

print("Solution 11: Convert celsius or rankine to fahrenheit")


def fahrenheit(celsius=None, rankine=None):
    """Convert either celsius or rankine to fahrenheit"""
    if celsius is None:
        if rankine is None:
            # If an error occurs you can "raise an exception" rather than return a special value
            # Compare str.find (returns -1) and str.index (raises ValueError)
            raise ValueError("You must provide exactly one of celsius or rankine, not neither")
        else:
            return rankine - 459.67
    else:
        if rankine is None:
            return celsius * 1.8 + 32
        else:
            raise ValueError("You must provide exactly one of celsius or rankine, not both")


# if you don't want program or notebook to stop at exception, catch it in a try except structure.
try:
    for c in [0, 100, -40]:
        print(f"{c:7.2f}°C is equivalent to {fahrenheit(c):7.2f}°F")
    for r in [0, 100, 459.67]:
        print(f"{r:7.2f}°R is equivalent to {fahrenheit(rankine=r):7.2f}°F")
    print(f"{r:7.2f}°R, {c:7.2f}°C is equivalent to {fahrenheit(rankine=r, celsius=c):7.2f}°F")
    print(f"None is equivalent to {fahrenheit():7.2f}°F")
except ValueError as ve:
    print("There was a problem.", ve)

# Dictionaries (dict in Python) store key:value pairs where
# key can be any hashable value (immutable values are generally hashable)
# value can be any value
forty = 40
d = {10: "ten", 20: "twenty", "thirty": 30, forty: "forty"}
for k in d.keys():
    print(f"d[{k!r}] is {d[k]}")
print(f"len(d) is {len(d)}")


def fahrenheit(**kwargs):
    """convert celsius or rankine to fahrenheit"""
    # **kwargs means to pack all remaining named arguments into a dict
    # where the keys are the keywords or argument names and the
    # values are the argument values
    if len(kwargs) == 1:
        # Convert keys of kwargs to a list and take the first one
        key = list(kwargs)[0]
        value = kwargs[key]
        if key == "celsius":
            return value * 1.8 + 32
        elif key == "rankine":
            return value - 459.67
        else:
            raise TypeError(f"fahrenheit() only accepts celsius or rankine, not {key}")
    else:
        raise ValueError(f"fahrenheit() only accepts one argument, not {len(kwargs)}. {kwargs}")


try:
    for c in [0, 100, -40]:
        # Now fahrenheit can't accept ordered arguments so we need to name it
        print(f"{c:7.2f}°C is equivalent to {fahrenheit(celsius=c):7.2f}°F")
    for r in [0, 100, 459.67]:
        print(f"{r:7.2f}°R is equivalent to {fahrenheit(rankine=r):7.2f}°F")
    print(f"{r:7.2f}°R, {c:7.2f}°C is equivalent to {fahrenheit(rankine=r, celsius=c):7.2f}°F")
    print(f"None is equivalent to {fahrenheit():7.2f}°F")
except ValueError as ve:
    print("There was a ValueError.", ve)
except TypeError as te:
    print("There was a TypeError.", te)

# Task 12: Convert fahrenheit() to accept a third possible argument kelvin
# f = kelvin * 1.8 + 459.67

print("Solution 12: fahrenheit function to accept celsius, rankine or kelvin")


def fahrenheit(**kwargs):
    if len(kwargs) == 1:
        # Convert keys of kwargs to a list and take the first one
        key = list(kwargs)[0]
        value = kwargs[key]
        if key == "celsius":
            return value * 1.8 + 32
        elif key == "rankine":
            return value - 459.67
        elif key == "kelvin":
            return value * 1.8 - 459.67
        else:
            raise TypeError(f"fahrenheit() only accepts celsius, kelvin or rankine, not {key}")
    else:
        raise ValueError(f"fahrenheit() only accepts one argument, not {len(kwargs)}. {kwargs}")


for c in [0, 100, -40]:
    print(f"{c:7.2f}°C is equivalent to {fahrenheit(celsius=c):7.2f}°F")
for r in [0, 100, 459.67]:
    print(f"{r:7.2f}°R is equivalent to {fahrenheit(rankine=r):7.2f}°F")
for k in [0, 273.15, 373.15]:
    print(f"{k:7.2f}K  is equivalent to {fahrenheit(kelvin=k):7.2f}°F")
try:
    print(f"None is equivalent to {fahrenheit():7.2f}°F")
except ValueError as ve:
    print(f"None is equivalent to ValueError {ve}")
try:
    print(f"{r:7.2f}°R, {c:7.2f}°C is equivalent to {fahrenheit(rankine=r, celsius=c):7.2f}°F")
except ValueError as ve:
    print(f"{r:7.2f}°R, {c:7.2f}°C is equivalent to ValueError {ve}")
try:
    print(f" 100 bozos is equivalent to {fahrenheit(bozos=100):7.2f}°F")
except TypeError as te:
    print(f" 100 bozos is equivalent to TypeError {te}")
