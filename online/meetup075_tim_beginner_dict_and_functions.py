#!/usr/bin/env python3
r"""MeetUp 075 - Beginners' Python and Machine Learning - 01 Sep 2020 - Getting Started 2

Youtube: https://youtu.be/IYEC6EmsUSQ
Colab:   https://colab.research.google.com/drive/1GYRTTiBYH77M56Uy4_PYEPmA5b9F42Ck
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

Learning objectives:

Learn how to use a Python `dict` (short for dictionary). A Python `dict` is like
a `list` on steroids. Not only can you store values of any data type in a `dict` (just like a `list`)
but you can specify what index key to retrieve the data later. This can be used to look up data and
save relationships of data.

You will also learn how to define functions so you can reuse code without retyping.

Follows on from Meetup 067 - Getting Started 1

@author D Tim Cummings

### Recap: Jupyter notebooks
    <shift><enter>  (to run a cell)
    Tools > Keyboard shortcuts  (to see other commands)
"""

# To find out what python version is currently being run
import sys  # gives us access to the standard library sys
print(sys.version)  # displays the value of version from the sys module

# Recap: How to store different data types in variables
my_int = 5
my_float = 5.
my_bool = True
my_str = "Beginners' Python and Machine Learning"
my_list = [my_int, my_float, my_bool, my_str]
# tuple is an immutable form of a list
my_tuple = tuple(my_list)

# How to display contents of variable in Jupyter Notebooks, Interactive Python (IPython) or Python Console
# The value of the last line is displayed in its repr() form
my_str  # won't be displayed
my_list  # will be displayed

# I will normally use print() so people using Python and IPython will see the same results
# How to use format strings to display contents of variables (Python 3.6 or later)
# Format strings have f before the quotation marks.
# Inside the string use {curly braces} to enclose an expression and the result of the expression will be included in the string
print("Printing using format strs")
print(f"my_int   : {my_int}")
print(f"my_float : {my_float}")
print(f"my_bool  : {my_bool}")
# !r is equivalent to repr(). displays internal representation. useful to distinguish data type such as str in this case
print(f"my_str   : {my_str!r}")
print(f"my_list  : {my_list}")
print(f"my_tuple : {my_tuple}")
# How to display contents of variable using print() without format str
print("\nPrinting without using format strs, but using str.format")
print(my_str, "True has value 1", "({0} + {1})/{0}".format(my_int, my_bool), (my_int + my_bool) / my_int, sep=" : ")

# Recap: Convert numbers (0 - 20) to text using a list
numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
           "nineteen", "twenty"]
i = 0
while i < len(numbers):
    print(f"{i:>4} : {numbers[i]}")
    i += 1

# We want to write a python program to convert numbers to text from a bigger range than 0 to 20
# We could increase numbers list
numbers += ["twenty-one", "twenty-two", "twenty-three"]
print(numbers)

# This works but doesn't scale very well
i = 22
print(f"{i:>4d} : {numbers[i]}")

# Delete the last three numbers from the list
del(numbers[-3:])
print(numbers)

# I want to store tens in variable called 'tens' and 0 - 20 in variable called 'numbers'
tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
print(f"tens = {tens}")

# We can split up the number and construct the name
for i in [27, 52, 5, 12, 30]:
    right = i % 10
    left = i - right
    print(f"{i:>4d} : {left:>2d} + {right:1d} : {tens[left//10-2]}-{numbers[right]}")

"""### Task 1:
Fix the above code so that all the names of numbers display correctly.
Need to check for numbers less than 20, and numbers evenly divisible by 10

    if condition1:
        do this if condition1 is True
    elif condition2:
        do this if condition1 is False and condition2 is True
    else:
        do this if condition1 is False and condition2 is False
"""

print("\nSolution 1: Converting numbers to words 0 - 99")
for i in [27, 52, 5, 12, 30]:
    right = i % 10
    left = i - right
    if i < len(numbers):
        print(f"{i:>4d} : {left:>2d} + {right:1d} : {numbers[i]}")
    elif right == 0:
        print(f"{i:>4d} : {left:>2d} + {right:1d} : {tens[left//10-2]}")
    else:
        print(f"{i:>4d} : {left:>2d} + {right:1d} : {tens[left//10-2]}-{numbers[right]}")

# The expression 'left//10-2' is a bit complicated
# It would be good if we could say tens[20] and it would give us 'twenty'
# We could use a sparse list but that is very inefficient from a memory perspective
# Python has a dict data type where you can set keys and values
tens = {20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'}
print("\nCreating dict")
print(f"tens[40] : {tens[40]}")

d = {'a': 'alpha', 'b': 'bravo', 'c': 'charlie'}
print(f"Keys can be str\n{d}")

d2 = {(1, 4): "bottom-left", (1, 8): "top-left", (5, 8): "top-right", (5, 4): "bottom-right"}
print("Keys can be tuple or any immutable hashable type\n", d2)

# d2 = {[1,4]: "bottom-left"}
print("Keys can't be mutable or unhashable such as list or dict")

# Add new keys and values. Keys have to be unique or they will overwrite previous value
d['d'] = 'delta'
d['e'] = 'epsilon'
# Merge
d.update({'e': 'echo', 'f': 'foxtrot'})
print(f"Updated and merged dict\n{d}")

# functions to list the keys and values in a dict
print(f"Keys   in dict : d.keys()   : {d.keys()}")
print(f"Values in dict : d.values() : {d.values()}")
print(f"Items  in dict : d.items()  : {d.items()}")

# How to loop through a dict. 'in dict' is same as 'in dict.keys()'
print("Looping using dict.keys()")
for k in d:
    v = d[k]
    print(k, v)

# Alternatively
print("Looping using dict.items()")
for k, v in d.items():
    print(k, v)

"""### Task 2:
Redo task 1 using a dict for tens
"""

print("\nSolution 2: Converting numbers to words 0-99 using dict")
for i in [27, 52, 5, 12, 30]:
    right = i % 10
    left = i - right
    if i < len(numbers):
        print(f"{i:>4d} : {left:>2d} + {right:1d} : {numbers[i]}")
    elif right == 0:
        print(f"{i:>4d} : {left:>2d} + {right:1d} : {tens[left]}")
    else:
        print(f"{i:>4d} : {left:>2d} + {right:1d} : {tens[left]}-{numbers[right]}")

"""### Task 3
Expand solution to task 2 to handle numbers up to 999. Test on 100, 112, 300, 999
"""

print("\nSolution 3: Converting numbers to words 0-999")
for i in [27, 52, 5, 12, 30, 100, 112, 300, 999]:
    hundreds_number = i // 100
    if hundreds_number > 0:
        # First handle greater than or equal to 100
        hundreds_name = numbers[hundreds_number] + " hundred"
        conjunction = " and "
    else:
        # Then handle less than 100
        hundreds_name = ""
        conjunction = ""
    remainder = i - hundreds_number * 100
    right = remainder % 10
    left = remainder - right
    breakdown = f"{hundreds_number}00 + {left:0>2d} + {right:1d}"
    if remainder == 0 and hundreds_name != "":
        print(f"{i:>4d} : {breakdown} : {hundreds_name}")
    elif remainder < len(numbers):
        print(f"{i:>4d} : {breakdown} : {hundreds_name}{conjunction}{numbers[remainder]}")
    elif right == 0:
        print(f"{i:>4d} : {breakdown} : {hundreds_name}{conjunction}{tens[left]}")
    else:
        print(f"{i:>4d} : {breakdown} : {hundreds_name}{conjunction}{tens[left]}-{numbers[right]}")

# Now we have some code which works for numbers from 0 to 999.
# We don't want to have to copy 18 lines of code every time we want to use it.
# We can put the code in a function and then call the function when needed.

# FUNCTIONS
print("\n\nFUNCTIONS")

# Some functions just run the same code every time they are run
# Examples are built-in functions help(), print(), license(), copyright()
# help()

print()

# All functions return a value but for functions which are called procedures or
# subroutines in other languages, this return value can be None
# The return value can be used in an expression or saved to a variable
return_value = copyright()
print(f"The return value from copyright() is {return_value}")

# Functions can take arguments. (Arguments can also be called parameters)
# Arguments can be identified by their position in ()
# You have seen print() function used with arguments
print("Example of print() with 3 arguments", 2, "three")

s1 = "Example"
print(f"{s1} of print() with {3-2} argument. This argument is a str which is result of format str being evaluated")

# Functions can also have named arguments. Named arguments must be used after positional arguments, and can be in any order
print("Example", "of", "print")
print("with", "no", "named", "arguments")
print("Example", "of", "print", sep="-", end=' ')
print("with", "named", "arguments", end="<<\n<<\n", sep="_")

# Examples of built-in functions with positional arguments
# (max on text looks at unicode values of text. lowercase higher than uppercase)
print(f"min(4, 87, 2.5)      : {min(4, 87, 2.5)}")
print(f"sum((4, 76, 3.4))    : {sum((4, 76, 3.4))}")
print(f"max('a', 'c', 'G')   : {max('a', 'c', 'G')}")
print(f"max(['a', 'c', 'G']) : {max(['a', 'c', 'G'])}")

# When wanting the function rather than calling the function, omit the parentheses ()
help(sum)

# Methods are functions attached to classes.
# Call them by referencing them from the <object name>.<method name>()
print(f"my_str.upper()  : {my_str.upper()}")
print(f"my_str.lower()  : {my_str.lower()}")
print(f""""bob's diner".title() : {"bob's diner".title()}""")
print(f""""bob's diner".split() : {"bob's diner".split()}""")

# Defining our own functions
# Function which returns None but prints current time


def show_now():
    """Simple example of a function which prints the current time"""
    import datetime
    print(f"The time is now {datetime.datetime.now()}")


show_now()


# Defining function with one argument and returns a float
def deg_fahrenheit(deg_celsius):
    return deg_celsius * 1.8 + 32


print("\n  Celsius    Fahrenheit")
for c in (0, 100, -40):
    print(f"{c:>7.2f}°C  {deg_fahrenheit(c):>10.2f}°F")


# Advanced: Extra information can be provided for docstring
# Defining a function a second time overrides original definition
# Type hinting is currently rare but gaining in use.
# It is used by IDEs to generate warnings
def deg_fahrenheit(deg_celsius: float) -> float:
    """Returns the temperature in °F given temperature in °C

    Many paragraphs of description describing what this
    function does and how to use it
    """
    return deg_celsius * 1.8 + 32


help(deg_fahrenheit)

deg_fahrenheit.__doc__

# Function still 'works' with wrong types eg Complex. Python still dynamically typed
print(f"(24+5j)°C  : {deg_fahrenheit(24+5j)}°F")

"""### Task 4
Convert code from task 3 into a function and return a str
"""

print("\nSolution 4: Function to convert number to name")


def number_name(number: int) -> str:
    """Returns the name of any integer between 0 and 999"""
    hundreds = number // 100
    if hundreds > 0:
        # First handle greater than or equal to 100
        hundreds_name = numbers[hundreds] + " hundred"
        conjunction = " and "
    else:
        # Then handle less than 100
        hundreds_name = ""
        conjunction = ""
    number -= hundreds * 100
    right = number % 10
    left = number - right
    if number == 0 and hundreds_name != "":
        return hundreds_name
    elif number < len(numbers):
        return hundreds_name + conjunction + numbers[number]
    elif right == 0:
        return hundreds_name + conjunction + tens[left]
    else:
        return hundreds_name + conjunction + tens[left] + "-" + numbers[right]


for i in [27, 52, 5, 12, 30, 100, 112, 300, 999]:
    print(f"{i:>4d} : {number_name(i)}")

# Task 5
# Expand Solution 4 to handle thousands up to 20999

print("\nSolution 5: Function to convert number to name 0 - 20999")


def number_name(number: int) -> str:
    """Returns the name of any integer between 0 and 20999"""
    s = ""
    thousands = number // 1000
    if thousands > 0:
        s += numbers[thousands] + " thousand "
        number -= thousands * 1000
    hundreds = number // 100
    if hundreds > 0:
        s += numbers[hundreds] + " hundred "
        number -= hundreds * 100
    if s != "" and number > 0:
        conjunction = "and "
    else:
        conjunction = ""
    right = number % 10
    left = number - right
    if number == 0 and s != "":
        return s
    elif number < len(numbers):
        return s + conjunction + numbers[number]
    elif right == 0:
        return s + conjunction + tens[left]
    else:
        return s + conjunction + tens[left] + "-" + numbers[right]


for i in [27, 52, 5, 12, 30, 112, 300, 999, 3200, 4020, 20999]:
    print(f"{i:>7,d} : {number_name(i)}")

# Task 6: Advanced: Expand solution 5 to handle numbers up to billions
# Hint: Start with expanding range to 999,999

print("\nSolution 6: Function to convert number to name 0-999 trillion")
powers = {1000000000000: "trillion", 1000000000: "billion", 1000000: "million", 1000: "thousand", 100: "hundred"}


def number_name(number: int) -> str:
    """Returns the name of any integer between 0 and 1 trillion"""
    s = ""
    # dicts retain order since Python 3.6
    for power, name in powers.items():
        count = number // power
        if count > 0:
            # recursive call of number_name from within number_name
            s += f"{number_name(count)} {name} "
            number -= count * power
    if s != "" and number > 0:
        conjunction = "and "
    else:
        conjunction = ""
    right = number % 10
    left = number - right
    if number == 0 and s != "":
        return s
    elif number < len(numbers):
        return s + conjunction + numbers[number]
    elif right == 0:
        return s + conjunction + tens[left]
    else:
        return s + conjunction + tens[left] + "-" + numbers[right]


for i in [0, 27, 5, 300, 999, 3200, 4020, 20999, 12345678901234]:
    print(f"{i:>7,d} : {number_name(i)}")

# Task 7: Define a better function than str.title for example BOB's diner -> Bob's Diner

"BOB's diner".title()

print("\nSolution 7: better function than str.title")


def title(sentence):
    words = sentence.split()
    capitalised_words = [w[0].upper() + w[1:].lower() for w in words]
    return ' '.join(capitalised_words)


print(title("BOB's diner"))

# functions can have default values for their arguments
# If no default value exists in function def then argument must be supplied
help(str.split)

# Task 8: Rewrite solution 7 to have a named argument sep with default value None which gets passed through to split

print("\nSolution 8: function with named argument which has a default value")


def title(sentence, sep=None):
    words = sentence.split(sep=sep)
    # list can be constructed using list comprehension
    capitalised_words = [w[0].upper() + w[1:].lower() for w in words]
    if sep is None:
        return ' '.join(capitalised_words)
    else:
        return sep.join(capitalised_words)


print(title("BOB's d_in_er", sep="_"))

# If you have all the arguments in an iterable sequence (eg list or tuple)
# you can unpack the arguments using the * notation
print("\nExamples of unpacking positional arguments ")
list_args = ['\t', 4]
tsv = "first one\tsecond\t3rd\t4th\t5th\t6th"
print(f"tsv                                   : {tsv}\nlist_args                             : {list_args}")
print(f"tsv.split(list_args[0], list_args[1]) : {tsv.split(list_args[0], list_args[1])}")
print(f"tsv.split(*list_args)                 : {tsv.split(*list_args)}")
args = ('my', 'favourite')
print(f"args                                  : {args}")
print('print( args, sep=":")                 : ', end='')
print(args, sep=":")
print('print(*args, sep=":")                 : ', end='')
print(*args, sep=":")


# Functions can be defined with unnamed arguments using * notation to pack arguments
def unnamed(*args):
    print("Example of packing unnamed positional arguments 'def unnamed(*args):'")
    print(args)


unnamed(4, 'foobar')
# unnamed(args=4)  # fails

# ** notation can also be used to unpack named arguments from mapping eg dict
print("Examples of unpacking named arguments ")
kwargs = {'maxsplit': 3, 'sep': '\t'}
tsv = "first one\tsecond\t3rd\t4th\t5th\t6th"
print(f"tsv                 : {tsv!r}\nkwargs              : {kwargs}")
print(f"tsv.split(**kwargs) : {tsv.split(**kwargs)}")


# Functions can be defined with non-positional named arguments using ** notation to pack keyword arguments
def named(**kwargs):
    for k, v in kwargs.items():
        print(k, v)


print("Example of packing named arguments 'def named(**kwargs)'")
named(a='alpha', b='bravo', c='charlie')


# Advanced: Python 3.8 and later can define pos only or kwd only arguments using / and *
def standard_arg(arg):
    print(arg)


def pos_only_arg(arg, /):
    print(arg)


def kwd_only_arg(*, arg):
    print(arg)


def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)
