#!/usr/bin/env python3
r"""MeetUp 132 - Beginners' Python and Machine Learning - 01 Feb 2022 - Getting Started 1

Colab:   https://colab.research.google.com/drive/1MTKVmaERigiE0TbPozGoZjefrRolzPyu
Youtube: https://youtu.be/Y6l9PyWEAXk
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/292298959/
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

Learning objectives:
- Interactive python
- Data types: int, float, str, list
- Variables: create, assign, update
- Scripting python

@author D Tim Cummings

Challenge 1: Install Software
- Use a Google account to go to https://colab.research.google.com
 - Doesn't need Python installed on your computer
 - Great for interactive use and data science
 - Not so good for scripting and building apps
 - Currently uses Python 3.9.16
- Install Python 3.11.2 from https://www.python.org/downloads/
 - necessary for running python on your computer
 - alternatively can install anaconda which includes many third party libraries
- PyCharm Community Edition 2022.3 from https://www.jetbrains.com/pycharm/download/
 - Integrated Development Environment (IDE)
 - Easier to write programs

For those interested in my children's Python coding course see https://pythonator.com (makes Python coders out of gamers). This course would be good for adults too if they could play Minecraft or Minetest as competently as the children! It requires the JetBrains Academy plugin for PyCharm https://plugins.jetbrains.com/plugin/10081-jetbrains-academy/docs/install-jetbrains-academy-plugin.html

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text
- use ? or Help menu for help
- see Tools menu > Keyboard shortcuts
"""
# import statements allow us to use standard libraries, third-party libraries and our own libraries
import decimal
import keyword
import math
import sys

from decimal import Decimal
from decimal import Decimal as D

# comments in code cells start with a '#'
# try executing ? to bring up IPython help
# help()  # works in Python console()
# ?       # works in IPython

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

# to see the value of an expression in IPython, just type the expression. This does nothing in Python
a + 4

# to store the result of an expression use equals (=)
b = (a + 15) / 4

# Challenge 2
# Add 123 to 456 and display the result
print("Solution 2: Works in ipython or python because python doesn't automatically display results of expression")
print(123 + 456)

# Advanced: to see the list of python keywords
# import keyword
# import sys
print("keywords", keyword.kwlist)
# We will cover 14 of the keywords in this session
print(f"There are {len(keyword.kwlist)} keywords in Python {sys.version}")
# Python 3.9 adds '__peg_parser__" which is just there to show which parser is being used and will be removed in Python 3.10

# None is a value to give to a variable if you don't want it to have a value
n = None
print(f"n is {n} which means it doesn't have a value")

# pass is a keyword which does nothing
# you need it sometimes when code is expecting indented code block but you don't actually want to do anything
pass

# Use long variable names to make code easier to read and avoid clashing with keywords
# Convention is all lower case separated by underscores
a_long_variable_name = 345
print(f"a_long_variable_name has the value {a_long_variable_name}")

"""# Data types"""

# use type() to see the data type of a value
print("The type of a is", type(a), "The value of a is", a)

print("The type of 456 is", type(456))

# ints are integers or whole numbers
# floats are floating point numbers, ie numbers with a fractional part represented by a decimal point
print("The type of b is", type(b), "The value of b is", b)

# floating point numbers are stored with a mantissa and an exponent making it
# possible to store very large or very small numbers in a small amount of memory.
# The position of the decimal point "floats" through the number depending on the
# value of the exponent
large_float = 12345678901234567890.0

small_float = 0.00000000000001234567890123456789

# Text is stored as strings of unicode characters (in Python 3) or bytes (in Python 2).
# Use quotes to denote strings
s1 = 'A str in single quotes can have embedded "double" quotes'
s2 = "A str in double quotes can have embedded 'single' quotes"
s3 = '''A str in triple single quotes can have embedded
        line feeds and 'single' and "double" quotes'''
s4 = """A str in triple double quotes can have embedded
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
print(f"{a} // {b} returns {a // b}    integer division (floor division)")
print(f"{a} %  {b} returns {a % b}    modulo (remainder)")
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
print(f"{a} ** {b} returns {a ** b}  power")

# Challenge 3: Store in variable c the number one hundred and twenty-three million four hundred and fifty-six thousand seven hundred and eighty-nine. 
# Display double the value of c.

# Solution 3: Underscores can be used in numbers to make them easier to read
c = 123_456_789
d = c + c
print(f"Solution 3 using f-string: double c = {d}")
print(f"f-strings can also evaluate expressions {{2 * c}}={2 * c}")
print(f"Formats can be placed after a colon  {{d:_}}={d:_}  {{d:,}}={d:,}  {{d:17,.3f}}={d:17,.3f}")

# Challenge 4: Find the remainder after integer dividing an odd number by 2. Then try an even number
print("Solution 4: loop through odd and even numbers from 0 to 4")
for i in range(5):
    print(f"{i} % 2 = {i%2}")

# Advanced: Bitwise operators work on binary numbers
a = 10
b = 3
print(f"{a} |  3 returns {a | 3:>2} : {a:4b} | {3:0>4b} returns {a | b:4b}  bitwise OR")
print(f"{a} &  3 returns {a & 3:>2} : {a:4b} & {3:0>4b} returns {a & b:0>4b}  bitwise AND")
print(f"{a} ^  3 returns {a ^ 3:>2} : {a:4b} ^ {3:0>4b} returns {a ^ b:0>4b}  bitwise XOR")
print(f" 3 << 2 returns {b << 2:>2} : {b:0>4b} << {2:>3} returns {b << 2:0>4b}  shift left")
print(f"{a+b} >> 2 returns {(a + b) >> 2:>2} : {a+b:4b} >> {2:>3} returns {a+b >> 2:0>4b}  shift right")

# str operators + *
print("well, " * 3 + "three holes in the ground")

# adjacent strs don't even need the +
print("one " 'two ' """three """ '''four''')

"""# Interesting side effects"""

# ints can have more significant digits than floats (floats are limited to about 17)
e = 250000000000000000000000000000000
print(f"25 / 7 returns {25 / 7}")
print(f"250000000000000000000000000000000 // 7 returns {250000000000000000000000000000000 // 7}")

# floats can't store decimal numbers exactly so good for science but not for accounting
# (use cents in int or dollars in Decimal for accounting)
print(f"1.1 + 2.2 returns {1.1 + 2.2}  (floats don't store decimal numbers exactly)")

# Challenge 5
# Find the integer quotient and remainder when dividing 666666 by 235
# Calculate 2 to the power 10
# Find the decimal quotient of 666666 divided by 235
# Store in a variable the name of your favourite programming language as a str
# Construct a new str that starts with "Programming in ", finishes with " is fun"
# and includes the value of the variable in the middle.

# Solutions
print(f"Solution 5: 123 + 456 returns {123 + 456}")
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
# Type the following in Python Console to see the results
type(True), type(False)

print(f"3 == 5 - 2  returns  {3 == 5 - 2}")

print(f"45 > 23  returns  {45 > 23}")

print(f"-10 < -20  returns  {-10 < -20}")

print(f"c1 == 'Python' returns  {c1 == 'Python'}")

"""# Challenge 6: Predict the outcome of the following boolean expressions"""

# Boolean expressions are embedded in format strs to make output understandable
# In IPython you could also type the expression alone in a cell and execute
print("Solution 6:")
print(f"c1 == 'python' returns {c1 == 'python'} because c1 is '{c1}'")
print(f"c1 != 'python' returns {c1 != 'python'}")
print(f"253 >= 1518 / 6 returns {253 >= 1518 / 6}")
print(f"253 <= {1518 / 6} returns {253 <= 1518 / 6}")
# import math
print(f"{math.e} < {math.pi} returns {math.e < math.pi}")
print(f"{math.e} < {math.pi * 2} < {math.tau} returns {math.e < math.pi * 2 < math.tau}")
print(f"'a' < 'c' returns {'a' < 'c'} because compares on unicode value")
print(f"'a' < 'C' returns {'a' < 'C'} because upper case characters appear before lower case in unicode")
print(f"'UPPER' < 'lower' returns {'UPPER' < 'lower'}")
print(f"'catch' < 'carriage' returns {'catch' < 'carriage'}")
print(f"'at' in 'catch' returns {'at' in 'catch'}")
print(f"'ac' in 'catch' returns {'ac' in 'catch'}")
print(f"'ta' in 'catch' returns {'ta' in 'catch'}")
print(f"True or False returns {True or False}")
print(f"True and False returns {True and False}")
print(f"True or False and False returns {True or False and False} because 'and' has precedence over 'or'")
print(f"{1 > 2} and {3 > 5} or {6 < 8} returns {1 > 2 and 3 > 5 or 6 < 8}")
c2 = c1
print(f"c1 is c2 returns {c1 is c2} because they refer to the same location in memory")

"""# More complicated data types - list"""

# define a list with square brackets and a comma separated list of any data types
lst = ["six", 5, 4.0, "3", "two", "one", "zero"]
print(f"{lst=}")

# lists are zero indexed. Refer to each element using numerical index in square brackets
print(f"{lst[0]=}")

print(f"{lst[1]=}")

print(f"{lst[6]=}")

# can also count index back from end
print(f"{lst[-1]=}")

print(f"{lst[-2]=}")

# use len() to find the length of a list
print(f"{len(lst)=}")

# slice a list using index values around a colon
# example starts from index 2 up to but not including index 5  (will be 5 - 2 = 3 elements)
print(f"{lst[2:5]=}")

# I think of indexes as counting positions between elements
# lst = ["six", 5, 4.0, "3", "two", "one", "zero"]
#       0     1  2    3    4      5      6       7   positive indexes
#      -7    -6 -5   -4   -3     -2     -1           negative indexes

# slice from beginning up to but not including index 4
print(f"{lst[:4]=}")

# slice from index 3 up to end
print(f"{lst[3:]=}")

# slice from index 1 up to end stepping in 2s
print(f"{lst[1::2]=}")

# slice backwards from end back to but not including index 1 stepping in -1s
print(f"{lst[-1:1:-1]=}")

print(f"{lst=}")

# assign item at index 2 with a new value
lst[2] = "FOUR"
print(f"{lst=} after assigning lst[2]")

lst[-1] = "Blast off"
print(f"{lst=} after assigning lst[-1]")

# strs can do many of the functions of lists for example slicing
s = "abcdefghij"
print(f"{s[3:7]=}")


# For accounting applications we can use the Decimal type from the decimal standard library
# import decimal
print("After importing whole decimal library")
print(f'decimal.Decimal("1.1") + decimal.Decimal("2.2") = {decimal.Decimal("1.1") + decimal.Decimal("2.2")!r}')

# The Decimal type (class) is all we need from decimal library so we can import just it
# from decimal import Decimal
print("After importing just the Decimal class from decimal library")
print(f'Decimal("1.1") + Decimal("2.2") = {Decimal("1.1") + Decimal("2.2")!r}')

# We can save on typing by giving an alias
# from decimal import Decimal as D
print("After aliasing Decimal class to D")
print(f'D("1.1") + D("2.2") = {D("1.1") + D("2.2")!r}')

# alias can be used on entire library. Two common ones in data science are:
# import pandas as pd
# import numpy as np

# keywords covered above
lst_keywords_covered = 'False|None|True|and|as|del|elif|else|for|from|if|import|in|is|not|or|pass|while'.split('|')
print(f"keywords covered {len(lst_keywords_covered)}")
