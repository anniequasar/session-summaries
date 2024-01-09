#!/usr/bin/env python3
"""MeetUp 054 - Beginners' Python and Machine Learning - 07 Apr 2020 - Getting Started 1

Youtube: https://youtu.be/Ypc63yxgAfs
Colab:   https://colab.research.google.com/drive/1iR9ShHjA7-YEqKFapsZwV09-c7GGj86f
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

Learning objectives:
- Interactive python
- Data types: int, float, str, list
- Variables: create, assign, update
- Scripting python
- Program structures: scripts, conditionals, loops

@author D Tim Cummings

Challenge 1: Install Software
- Use a Google account to go to https://colab.research.google.com
 - Doesn't need Python installed on your computer
 - Great for interactive use and data science
 - Not so good for scripting and building apps
- Install Python 3 from https://www.python.org/downloads/
 - necessary for running python on your computer
 - alternatively can install anaconda which includes many third party libraries
- PyCharm Community Edition 2019.3.4 from https://www.jetbrains.com/pycharm/download/
 - Integrated Development Environment (IDE)
 - Easier to write programs

For those interested in my children's Python coding course see https://pythonator.com (makes Python coders out of gamers).
This course would be good for adults too if they could play Minecraft or Minetest as well as the children!
It requires the EduTools plugin for PyCharm https://www.jetbrains.com/help/education/install-edutools-plugin.html?section=PyCharm

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text
- use ? or Help menu for help
- see Tools menu > Keyboard shortcuts
"""
# import commands allow us to use standard libraries in our script - see later
import keyword
import math
import random

# comments in code cells start with a '#'
# try executing ? to bring up IPython help
# help()  # ? works in IPython, help() in Python Console

"""# Variables
Variables are memory locations to store data.
You can name them anything you like as long as you don't use a Python keyword.
Name must start with a letter but can include numbers.
Can't include special characters except underscore _
"""

# to store a number in a variable use equals (=)
a = 3

# to see the value of the variable in Python you can print it
print(a)

# to see the value of a variable in IPython just type the variable name
a

# to see the value of an expression in IPython, just type the expression
a + 4

# to store the result of an expression use equals (=)
b = (a + 15) / 4
b

# Advanced: to see the list of python keywords
# see "import keyword" at beginning of script
print(keyword.kwlist)

"""# Data types"""

# use type() to see the data type of a value
type(a)

# ints are integers or whole numbers
# floats are floating point numbers, ie numbers with a fractional part represented by a decimal point
type(b)

# floating point numbers are stored with a mantissa and an exponent making it
# possible to store very large or very small numbers in a small amount of memory.
# The position of the decimal point "floats" through the number depending on the
# value of the exponent
12345678901234567890.0

0.00000000000001234567890123456789

# Text is stored as strings of unicode characters (in Python 3) or bytes (in Python 2).
# Use quotes to denote strings
s1 = 'A str in single quotes can have embedded "double" quotes'
s2 = "A str in double quotes can have embedded 'single' quotes"
s3 = '''A str in triple single quotes can have embedded
        line feeds and 'single' and "double" quotes'''
s4 = """A str in triple single quotes can have embedded
        line feeds and 'single' and "double" quotes"""
print(s1)
print(s2)
print(s3)
print(s4)
type(s1)

# Advanced: Special characters can be added to strings using the backslash \
sc1 = '\n'  # new line
sc2 = '\r'  # carriage return
sc3 = '\''  # single quote (useful if str denoted by single quotes)
sc4 = "\""  # double quote (useful if str denoted by double quotes)
sc5 = '\\'  # backslash
print(1, sc1, 2, sc2, 3, sc3, 4, sc4, 5, sc5)  # prints each value separated by a space

# Advanced: Strings can have prefixes before the first quote to make it easier to define
pu = u"A unicode str. Default in Python 3 but prefix required in Python 2"
pb = b"A byte string. Default in Python 2 but prefix required in Python 3"
pr = r"A raw str where backslash \ is just a backslash \  \n \r \t \\ \' \" "
pf = f"A format string to include values and expressions {a} + {b} = {a + b}"
print(pu)
print(pb)
print(pr)
print(pf)

"""# Operators

Create expressions using operators between variables or values
"""

# Integer operators
a = 27
b = 5
print(f"{a} +  {b} returns {a + b}   addition")
print(f"{a} -  {b} returns {a - b}   subtraction")
print(f"{a} *  {b} returns {a * b}  multiplication")
print(f"{a} // {b} returns {a // b}    integer division")
print(f"{a} %  {b} returns {a % b}    modulo")
print(f"{a} ** {b} returns {a ** b}  power")

# Floating point operators if either or both values is a float
a = 27.0
b = 5
print(f"{a} +  {b} returns {a + b}  addition")
print(f"{a} -  {b} returns {a - b}  subtraction")
print(f"{a} *  {b} returns {a * b}  multiplication")
print(f"{a} /  {b} returns {a / b}  floating point division")
print(f"{a} // {b} returns {a // b}  whole number division")
print(f"{a} %  {b} returns {a % b}  modulo")
print(f"{a} ** {b} =returns {a ** b}  power")

# Advanced: Bitwise operators work on binary numbers
a = 10
b = 3
print(f"{a} |  3 returns {a | 3:>2} : {a:4b} | {3:0>4b} returns {a | b:4b}  bitwise OR")
print(f"{a} &  3 returns {a & 3:>2} : {a:4b} & {3:0>4b} returns {a & b:0>4b}  bitwise AND")
print(f"{a} ^  3 returns {a ^ 3:>2} : {a:4b} ^ {3:0>4b} returns {a ^ b:0>4b}  bitwise XOR")
print(f" 3 << 2 returns {b << 2:>2} : {b:0>4b} << {2:>3} returns {b << 2:0>4b}  shift left")
print(f"{a+b} >> 2 returns {(a + b) >> 2:>2} : {a+b:4b} >> {2:>3} returns {a+b >> 2:0>4b}  shift right")

# str operators + *
"well, " * 3 + "three holes in the ground"

# adjacent strs don't even need the +
"one " 'two ' """three """ '''four'''

"""# Interesting side effects"""

# ints can have more significant digits than floats (floats are limited to about 17)
e = 250000000000000000000000000000000
print(f"25 / 7 returns {25 / 7}")
print(f"250000000000000000000000000000000 // 7 returns {250000000000000000000000000000000 // 7}")

# floats can't store decimal numbers exactly so good for science but not for accounting
# (use cents in int or dollars in Decimal for accounting)
print(f"1.1 + 2.2 returns {1.1 + 2.2}  (floats don't store decimal numbers exactly)")

"""# Challenge 2"""

# Add 123 to 456 and display the result

# Find the quotient and remainder when dividing 666666 by 235

# Calculate 2 to the power 10

# Find the decimal quotient of 666666 divided by 235

# Store in a variable the name of your favourite programming language as a str
# Construct a new str that starts with "Programming in ", finishes with " is fun"
# and includes the value of the variable in the middle.

# Solutions
print(f"123 + 456 returns {123 + 456}")
print(f"666666 // 235 returns integer quotient {666666 // 235}, 666666 % 234 returns integer remainder {666666 % 235}")
print(f"2**10 returns {2**10}")
print(f"666666 / 235 returns {666666 / 235}")
c1 = "Python"
c2 = "Programming in " + c1 + " is fun"
print(c2)

"""# Data type bool
- Boolean data types store `True` or `False`
- They are the result of using a conditional operator `==, !=, <, >, <=, >=, in, or, and, not, is`
"""

type(True), type(False)

3 == 5 - 2

45 > 23

-10 < -20

c1 == "Python"

"""# Challenge 3: Predict the outcome of the following boolean expressions"""

# Boolean expressions are embedded in format strs to make output understandable
# In IPython you could also type the expression alone in a cell and execute
print(f"c1 == 'python' returns {c1 == 'python'} because c1 is '{c1}'")
print(f"c1 != 'python' returns {c1 != 'python'}")
print(f"253 >= 1518 / 6 returns {253 >= 1518 / 6}")
print(f"253 <= {1518 / 6} returns {253 >= 1518 / 6}")
# see "import math" at beginning of script
print(f"{math.e} < {math.pi} returns {math.e < math.pi}")
print(f"{math.e} < {math.pi * 2} < {math.tau} returns {math.e < math.pi * 2 < math.tau}")
print(f"'a' < 'c' returns {'a' < 'c'} because compares on unicode value")
print(f"'a' < 'C' returns {'a' < 'C'} because upper case characters appear before lower case in unicode")
print(f"'UPPER' < 'lower' returns {'UPPER' < 'lower'}")
print(f"'catch' < 'carriage' returns {'catch' < 'carriage'}")
print(f"[5, 1, 2] >= [6, 0, 3] returns {[5, 1, 2] >= [6, 0, 3]} because list elements are compared left to right")
print(f"'at' in 'catch' returns {'at' in 'catch'}")
print(f"'ac' in 'catch' returns {'ac' in 'catch'}")
print(f"'ta' in 'catch' returns {'ta' in 'catch'}")
print(f"[2, 6] not in [5, 1, 2, 6] returns {[2, 6] not in [5, 1, 2, 6] } because only "
      "one element of a list can be checked with 'in' at a time")
print(f"True or False returns {True or False}")
print(f"True and False returns {True and False}")
print(f"True or False and False returns {True or False and False} because 'and' has precedence over 'or'")
print(f"{1 > 2} and {3 > 5} or {6 < 8} returns {1 > 2 and 3 > 5 or 6 < 8}")
c2 = c1
print(f"c1 is c2 returns {c1 is c2} because they refer to the same location in memory")

"""# More complicated data types - list"""

# define a list with square brackets and a comma separated list of any data types
lst = ["six", 5, 4.0, "3", "two", "one", "zero"]
print(lst)

# lists are zero indexed. Refer to each element using numerical index in square brackets
lst[0]

lst[1]

lst[6]

# can also count index back from end
lst[-1]

lst[-2]

# use len() to find the length of a list
len(lst)

# slice a list using index values around a colon
# example starts from index 2 up to but not including index 5  (will be 5 - 2 = 3 elements)
lst[2:5]

# slice from beginning up to but not including index 4
lst[:4]

# slice from index 3 up to end
lst[3:]

# slice from index 1 up to end stepping in 2s
lst[1::2]

# slice backwards from end back to but not including index 1 stepping in -1s
lst[:1:-1]

lst

# assign item at index 2 with a new value
lst[2] = "FOUR"
lst

lst[-1] = "Blast off"
lst

# strs can do many of the functions of lists for example slicing
s = "abcdefghij"
s[3:7]

"""# Challenge 4: What is something you can do in a list you can't do with a str?"""

# Solution
s = "6543210"
print(f"s = {s}")
print(f"s[0] returns {s[0]}")
print(f"s[1] returns {s[1]}")
print(f"s[6] returns {s[6]}")
print(f"s[-1] returns {s[-1]}")
print(f"s[-2] returns {s[-2]}")
print(f"len(s) returns {len(s)}")
print(f"s[2:5] returns {s[2:5]}")
print(f"s[:4] returns {s[:4]}")
print(f"s[3:] returns {s[3:]}")
print(f"s[1::2] returns {s[1::2]}")
print(f"s[:1:-1] returns {s[:1:-1]}")
print("s[2] = 'F' returns TypeError: 'str' object does not support item assignment")
print("s[-1] = 'Z' returns TypeError: 'str' object does not support item assignment")

# Interesting fact - can convert str to a list using list()
list_from_str = list(s)
list_from_str

# To convert a str to a list use str() but it looks different to the original str
str(list_from_str)

# Advanced: Can use join to return original str
"".join(list_from_str)

"""# Programming - `if then`
- up until now we have been using Python as a calculator
- putting more than one line in a cell executes the lines in sequential order
- sometimes we want to change which lines get executed depending on a condition
- unlike other languages Python defines code blocks by indentation
- colab indents by 2 spaces. Most Python indents by 4 spaces
"""

# see "import random" at beginning of script
die_roll = random.randrange(6) + 1  # randrange(6) returns an int between 0 and 5 inclusive
if die_roll % 2 == 0:
    print(f"You rolled {die_roll} which is an even number")
else:
    print(f"You rolled {die_roll} which is an odd number")

die_rolls = [random.randrange(6) + 1, random.randrange(6) + 1]
print(f"You rolled {die_rolls}. ", end=" ")
if die_rolls[0] == die_rolls[1]:
    print("They are both equal")
elif die_rolls[0] < die_rolls[1]:
    print("First roll is less than the second roll")
else:
    print("First roll is greater than the second roll")

"""# Programming - `for` loop, `while` loop
- sometimes we want to repeat the same code block many times so we use loops
"""

# a for loop repeats for every item in a iterable sequence such as a list or str
for number in ['three', 'two', 'one']:
    print(number)

# a while loop is like an if statement except it repeats the following code block
# until the condition is no longer true
counter = 0
while counter < 10:
    die_rolls = [random.randrange(6) + 1, random.randrange(6) + 1]
    print(f"{counter}: You rolled {die_rolls}. ", end=" ")
    if die_rolls[0] == die_rolls[1]:
        print("They are both equal")
    elif die_rolls[0] < die_rolls[1]:
        print("First roll is less than the second roll")
    else:
        print("First roll is greater than the second roll")
    counter += 1

"""# Challenge 5
Write a program which prints every number from 0 to 20 as digits and its name
in words as well as whether it is even or odd
"""

# Use the following list
numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
           "nineteen", "twenty"]

# Solution
i = 0
while i < len(numbers):
    if i % 2 == 0:
        category = "even"
    else:
        category = "odd "
    print(i, category, numbers[i])
    i += 1
