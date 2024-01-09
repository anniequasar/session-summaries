#!/usr/bin/env python3
r"""MeetUp 128 - Beginners' Python and Machine Learning - 14 Dec 2021 - Functions (intermediate)

Learning objectives:
- dict
- Function arguments with different data types
- Functions with variable number of arguments 

Links:
- Colab:   https://colab.research.google.com/drive/1p5M01TeyHy95gxb3xmnDopXd3JanhsB6
- Youtube: https://youtu.be/9Z94ZQOUEU4
- Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/282356833/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

There are different ways to write Python. 
The language is the same in every case, but the ways users
interact with the program is different in each case.
Today we are using Jupyter Notebooks on Google Colab. 
Jupyter Notebooks are an extension of IPython (Interactive Python). Every exercise could also be done in Python. Python version of this notebook available in https://github.com/timcu/bpaml-sessions/online

Jupyter Notebooks are a great way to learn because you see the results immediately. They can also be great for data science. However, they are not suited for some Python programs such as web applications, database apps, desktop apps, GUI apps, operating system services.

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text
- use ? or Help menu for help
- see Tools menu > Keyboard shortcuts

# To run this python script on your own computer you will need Python 3.8 or later and install third party libraries in virtual environment
 - run the following from command line to set up and run virtual environment Mac or Linux
    python3 -m venv venv
    source venv/bin/activate
    pip install plotly pandas numpy sympy
 - run the following from command line to set up and run virtual environment Windows
    py -m venv venv
    venv\Scripts\Activate
    pip install plotly pandas numpy sympy

"""

# Last week we defined a function with one argument
def f(a):
    return a * a - 4 * a + 4

# We can use a third party library to plot x and y in a scatter chart
import plotly.express as px

# Create our data using list comprehension
lst_x = [i/10 for i in range(41)]
lst_y = [f(i/10) for i in range(41)]
fig = px.line(x=lst_x, y=lst_y)
fig.show()

# As well as int and float our argument can take Decimal from decimal standard library 
from decimal import Decimal
x = Decimal("1.1")
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")
x = 1.1
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")

# Task 1: Try other data types for argument to function. eg complex number 5-2j

print("\nSolution 1: In Python, complex numbers use j to represent square root of -1")
x = 5-2j
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")

print("\nSolution 1: Using ndarray from third party library numpy https://numpy.org")
# Third party libraries normally have to be installed although anaconda and colab include many by default
# pip install numpy
import numpy as np
x = np.arange(0, 2.1, 0.2)
print(type(x))
print(x)

# ndarray understands operators *, -, +
x * x

# Hence we can pass an ndarray as argument to our function which only uses *, -, +
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")

print("\nSolution 1: Using rational numbers from the standard library fractions https://docs.python.org/3/library/fractions.html")
from fractions import Fraction
x = Fraction('1/3')
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")

print("\nSolution 1: Using rational numbers from third party library sympy")
import sympy as sym
x = sym.Rational("2/3")
y = f(x)
print(f"type(x)={type(x).__name__:7s}: type(y)={type(y).__name__:7s} f({x})={y}")

# Sympy can also produce nicely formatted output using Latex or Unicode or Matplotlib or MathJax
y

# Sympy is useful if you want the exact values of expressions with irrational numbers 
x = sym.sqrt(2) + sym.pi
f(x)

# Solution 1: Using symbols from third party library sympy https://www.sympy.org
x = sym.symbols('x')
y = f(x)
y

# Sympy can be used to do calculus on functions
sym.diff(y)

# It can factorise polynomials
sym.factor(y)

# It can solve symbolic equations for 0
sym.solve(y)

# Use sympy to generate the latex which you can use in notebook markdown surrounded by $
# eg $x^{2} - 4 x + 4$
sym.latex(y)

"""$x^{2} - 4 x + 4$

Task 2: Create a function for the sigmoid function using exp from math standard library and plot function with x values from -5 to 5

$S(x) = \frac{1}{1 + e^{-x}}$
"""

# Solution 2
import math
def sigmoid(a):
    return 1 / (1 + math.exp(-a))

lst_x = [i/10 for i in range(-50, 51)]
lst_y = [sigmoid(i/10) for i in range(-50, 51)]
fig = px.line(x=lst_x, y=lst_y)
fig.show()

# Task 3: Try calling sigmoid on numpy array
x = np.arange(-5, 5.1, 0.2)

print("\nSolution 3:")
try:
    y = sigmoid(x)
    print(y)
except TypeError as te:
    print(te)

# Python math.exp only understands Python scalars
# scalar = single value
# vector = one dimensional array of values
# matrix = two dimensional array of values
# tensor = three or more dimensional array of values

# Task 4. Try using numpy.exp

print("\nSolution 4:")
def sigmoid(a):
    return 1 / (1 + np.exp(-a))

print(f"scalar: sigmoid(-2) = {sigmoid(2)}\n")
x = np.arange(-3, 3.1, 0.5)
x.resize(3, 4)
print(f"matrix: sigmoid(\n{x}\n) = \n{sigmoid(x)}\n")
x = np.arange(-10, 10.1, 0.5)
y = sigmoid(x)
print(f"vector: sigmoid(\n{x}\n) = \n{y}")
fig = px.line(x=x, y=y)
fig.show()

# Task 5: Define a function which converts temperature in celsius to fahrenheit
# f = c * 1.8 + 32

print("\nSolution 5: Convert celsius to fahrenheit")
def fahrenheit(celsius):
    """Convert temperature in celsius to fahrenheit"""
    return celsius * 1.8 + 32

for c in [0, 100, -40]:
    print(f"{c:7.2f}°C is equivalent to {fahrenheit(c):7.2f}°F")

# Functions can have more than one argument
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
print(f"min(4., 87., 2.5)    : {min(4., 87., 2.5)}")
print(f"sum((4, 76, 3.4))    : {sum((4, 76, 3.4))}")
print(f"max('a', 'c', 'G')   : {max('a', 'c', 'G')}")
print(f"max(['a', 'c', 'G']) : {max(['a', 'c', 'G'])}")

# When wanting the function rather than calling the function, omit the parentheses ()
# help(sum)

# Methods are functions attached to classes. 
# Call them by referencing them from the <object name>.<method name>()
my_str = "Methods: upper and lower case characters: aBcDeF"
print(f"my_str.upper()  : {my_str.upper()}")
print(f"my_str.lower()  : {my_str.lower()}")
print(f""""bob's diner".title() : {"bob's diner".title()}""")
print(f""""bob's diner".split() : {"bob's diner".split()}""")

# Advanced: Extra information can be provided for docstring
# Defining a function a second time overrides original definition
# Type hinting is currently rare but gaining in use.
# It is used by IDEs to generate warnings
def fahrenheit(celsius: float) -> float:
    """Returns the temperature in °F given temperature in °C
    
    Many paragraphs of description describing what this
    function does and how to use it
    """
    return celsius * 1.8 + 32

# help(fahrenheit)

print(f"{fahrenheit.__doc__=}")

# Function still 'works' with wrong types eg Complex. Python still dynamically typed
print(f"(24+5j)°C  : {fahrenheit(24+5j)}°F")

# Task 6: Define a function which converts temperature in celsius or rankine to fahrenheit
# f = r - 459.67

print("\nSolution 6: Convert celsius or rankine to fahrenheit")
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
for key in d.keys():
    print(f"d[{key!r}] is {d[key]}")
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

# Task 7: Convert fahrenheit() to accept a third possible argument kelvin
# f = kelvin * 1.8 + 459.67

print("\nSolution 7: fahrenheit function to accept celsius, rankine or kelvin")
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

# Task 8: Expand total_seconds to take three arguments hours, minutes, seconds

print("\nSolution 8: Three named arguments to total_seconds")
def total_seconds(hours=0, minutes=0, seconds=0):
    """returns the total number of seconds in the given hours, minutes and seconds

    hours: the number of hours(default 0)
    minutes: the number of minutes (default 0)
    seconds: the number of seconds (default 0)"""
    return hours * 3600 + minutes * 60 + seconds

print(f"total_seconds(0, 32, 15)={total_seconds(0, 32, 15)}. (calling by order)")
print(f"total_seconds(seconds=15, minutes=32)={total_seconds(seconds=15, minutes=32)}. (calling by name)")
print(f"total_seconds(0, seconds=15, minutes=32)={total_seconds(0, seconds=15, minutes=32)}. (calling by order and name. order has to come first)")
print(f"total_seconds(seconds=15, hours=1, minutes=32)={total_seconds(seconds=15, hours=1, minutes=32)}. (calling by name)")

# Functions can be defined with unnamed arguments using * notation to pack arguments
def unnamed(*args):
    print("Example of packing unnamed positional arguments 'def unnamed(*args):'")
    print(args)

unnamed(4, 'foobar')
# unnamed(args=4)  # fails

# Task 9: Given a tuple of 3 numbers, call total_seconds
tpl = (1, 32, 15)

print("\nSolution 9: * unpacks when calling a function, packs when defining a function")
print(f"{total_seconds(*tpl)=}")

# Advanced: Python 3.8 and later can define pos only or kwd only arguments using / and *
def standard_arg(arg):
    print(arg)


def pos_only_arg(arg, /):
    print(arg)


def kwd_only_arg(*, arg):
    print(arg)


def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)