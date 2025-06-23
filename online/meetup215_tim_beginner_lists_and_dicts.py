r"""MeetUp 215 - Beginners' Python and Machine Learning - 04 Jun 2025 - lists tuples and dicts for absolute beginners

Learning objectives:
- Interactive python
- Data types: list, tuple and dict
- Scripting python
- Program structures: scripts, conditionals, loops

Links:
- Colab:   https://colab.research.google.com/drive/18dzfIiNAD5D1v7jDs_DwQF1gkpH45a3f
- Youtube: https://youtu.be/SJ0wG85J3mM
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/307933111/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

This session will show you how to use the python data types `list`, `tuple` and `dict`, including using them in simple Python scripts.

It is the second in the series targeted at absolute beginners after meetup 180.

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text
- use ? or Help menu for help
- see Tools menu > Keyboard shortcuts
"""

import random  # random is a standard library so we need to import it but don't need to install it

"""# Data type - `list`"""

# define a list with square brackets and a comma separated list of any data types
lst = ["six", 5, 4.0, "3", "two", "one", "zero"]
print(f"{lst=}")

# lists are zero indexed. Refer to each element using numerical index in square brackets
print(f"{lst[0]=}")

# can also count index back from end
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

print(f"{lst=}")

# assign item at index 2 with a new value
lst[2] = "FOUR"
print(f"After \"lst[2] = 'FOUR'\", {lst=}")

# You can delete an element from the list using the del keyword
del lst[4]
print(f"After \"del lst[4]\", {lst=}")

# j is square root of negative one (complex number type)
lst.append(1j)
print(f"After \"lst.append(1j)\", {lst=}")

"""# Data type - `tuple`
A `tuple` is like a `list` except it is immutable (can't be changed in place)
"""

# define a tuple with parentheses and a comma separated list of any data types
tpl = ("six", 5, 4.0, "3", "two", "one", "zero")
print(f"{tpl=}")

print(f"{tpl[0]=}")

"""# Challenge 1: What is something you can do in a list you can't do with a tuple?"""

print("\nSolution 1 - using f-strings anything in {} is evaluated as an expression")
print(f"tpl = {tpl}")
print(f"tpl[0] returns {tpl[0]}")
print(f"tpl[1] returns {tpl[1]}")
print(f"tpl[6] returns {tpl[6]}")
print(f"tpl[-1] returns {tpl[-1]}")
print(f"tpl[-2] returns {tpl[-2]}")
print(f"len(tpl) returns {len(tpl)}")
print(f"tpl[2:5] returns {tpl[2:5]}")
print(f"tpl[:4] returns {tpl[:4]}")
print(f"tpl[3:] returns {tpl[3:]}")
print(f"tpl[1::2] returns {tpl[1::2]}")
print(f"tpl[:1:-1] returns {tpl[:1:-1]}")
print(f"tpl[2] = 'F' returns TypeError: 'tuple' object does not support item assignment")
print(f"tpl[-1] = 'Z' returns TypeError: 'tuple' object does not support item assignment")
print(f"del tpl[2] returns TypeError: 'tuple' object doesn't support item deletion")

# can convert tuple to a list using list()
list_from_tuple = list(tpl)
print(f"{list_from_tuple=}")

# To convert a list to tuple use tuple() (just like other datatypes int(a), float(a), str(a))
print(f"{tuple(list_from_tuple)=}")

"""# Programming - `if`
- up until now we have been using Python as a calculator
- putting more than one line in a cell executes the lines in sequential order
- sometimes we want to change which lines get executed depending on a condition
- unlike other languages Python defines code blocks by indentation
- Python convention is indent by 4 spaces. Fix in Tools > Settings > Editor
"""

# randrange(6) returns an int between 0 and 5 inclusive - pythonic but confusing for dice rolls
# randint(1, 6) returns an int between 1 and 6 inclusive - not pythonic but perfect fit for dice rolls
die_roll = random.randint(1, 6)
if die_roll % 2 == 0:
    print(f"You rolled {die_roll} which is an even number")
else:
    print(f"You rolled {die_roll} which is an odd number")

# Challenge 2 - Roll two dice and report whether the first die rolls are a greater number than the second

print("\nSolution 2 - and introducing elif")
dice_roll = [random.randint(1, 6), random.randint(1, 6)]
print(f"You rolled {dice_roll}. ", end=" ")  # how to print without a newline at the end of the line
if dice_roll[0] > dice_roll[1]:
    print("First roll is greater than the second roll")
elif dice_roll[0] < dice_roll[1]:
    print("First roll is less than the second roll")
else:
    print("They are both equal")

# Challenge 3 - for an element of tuple say whether str, int, other
# Hint check an element is a str using "type(tpl[idx]) == str" or "isinstance(tpl[idx], str)"

print("\nSolution 3 - and introducing the for loop")
for a in tpl:
    if type(a) == str:
        print("str", a)
    elif type(a) == int:
        print("int", a)
    else:
        print("other", a, type(a))
print()

"""# Programming - `for` loop, `while` loop
- sometimes we want to repeat the same code block many times so we use loops
"""

# a for loop repeats for every item in an iterable sequence such as a list, tuple or str
for number in ('three', 'two', 'one'):
    print(number)

# a while loop is like an if statement except it repeats the following code block 
# until the condition is no longer true
counter = 0
while counter < 10:
    dice_roll = [random.randrange(6) + 1, random.randrange(6) + 1]
    print(f"{counter}: You rolled {dice_roll}. ", end=" ")
    if dice_roll[0] == dice_roll[1]:
        print("They are both equal")
    elif dice_roll[0] < dice_roll[1]:
        print("First roll is less than the second roll")
    else:
        print("First roll is greater than the second roll")
    counter += 1

"""# Challenge 4

Write a program which prints every number from 0 to 20 as digits and its name 
in words as well as whether it is even or odd

"""

# Use the following tuple 
numbers = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
           "nineteen", "twenty")

print("\nSolution 4 - introducing enumerate()")
for i, value in enumerate(numbers):
    if i % 2 == 0:
        category = "even"
    else:
        category = "odd"
    print(f"{i:3}  {numbers[i]:15} {category}")
print()

# The problem with this code is it doesn't scale well. 
# We could make a tuple with 100 elements for the numbers 0-99
# Or we could have two tuples. One for the first 20 numbers and one for the tens
tens = ("twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")
i = 30
print(f"{i=} {tens[i // 10 - 2]=}")

"""# Data type - `dict`

Allows us to specify index (or key) as well as value
"""

tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
print(f"{i=}, {tens[i]=}")

# keys are most commonly ints or strs 
alphabet = {'a': 'alfa', 'b': 'bravo', 'c': 'charlie', 'd': 'delta', 'e': 'echo', 'f': 'foxtrot', 'g': 'golf', 
            'h': 'hotel', 'i': 'india', 'j': 'juliett', 'k': 'kilo', 'l': 'lima', 'm': 'mike', 'n': 'november', 
            'o': 'oscar', 'p': 'papa', 'q': 'quebec', 'r': 'romeo', 's': 'sierra', 't': 'tango', 'u': 'ukelele', 
            'v': 'victor', 'w': 'whiskey', 'x': 'xray', 'y': 'yankee', 'z': 'zulu'}
word = 'python'
# we can iterate over letters in a str just like iterating over elements in a list or tuple
for letter in word:
    print(alphabet[letter], end=' ')
print()

# Challenge 5 - write a Python script to write a number in words for any number between 0 and 99
# Consider the following conditions
# a) number ≤ 20
# b) number > 20 and divisible by 10
# c) number > 20 and not divisible by 10


print("\nSolution 5 - introducing range()")
for i in range(100):
    if i < len(numbers):
        print(i, numbers[i])
    elif i % 10 == 0:
        print(i, tens[i])
    else:
        value_ones = i % 10
        value_tens = i - value_ones
        print(i, f"{tens[value_tens]}-{numbers[value_ones]}")
print()
