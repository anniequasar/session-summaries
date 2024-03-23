r"""MeetUp 197 - Beginners' Python and Machine Learning - 07 Feb 2024 - Introduction to Coding

Colab:   https://colab.research.google.com/drive/1gZLIjtaV7iW_5bMsAtZb1yU07NLSDpZt
Youtube: https://youtu.be/2-BWNFXp5EM
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/298771967/
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

Learning objectives:
- Interactive python
- Introduction to coding
- Branching, looping and list comprehension

@author D Tim Cummings

Challenge 1: Install Software
- Use a Google account to go to https://colab.research.google.com
 - Doesn't need Python installed on your computer
 - Great for interactive use and data science
 - Not so good for scripting and building apps
- Install Python 3.11.3 from https://www.python.org/downloads/
 - necessary for running python on your computer
 - alternatively can install anaconda which includes many third party libraries
 - Additionally install IDE such as PyCharm Community Edition 2023.1.2 from https://www.jetbrains.com/pycharm/download/
  - Integrated Development Environment (IDE)
  - Easier to write programs

For those interested in my children's Python coding course see https://pythonator.com (makes Python coders out of gamers). This course would be good for adults too if they could play Minecraft or Minetest as competently as the children! It requires the JetBrains Academy (previously named EduTools) plugin for PyCharm https://plugins.jetbrains.com/plugin/10081-jetbrains-academy/docs/jetbrains-academy-plugin.html

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
"""

# comments in code cells start with a '#'. They don't do anything. They are just there for you to read.
# try executing ? to bring up IPython help (press <shift><enter> while this cell is selected)
# If you are using Python Console rather than IPython then use help()
# ?

# Coding is all about writing commands for a computer to follow
# The only commands a computer can do are rather simple but it can do them very quickly
# For example to display something, use the print() command
print(5)

# In IPython or Python Console we don't even need the print() to display data
4

# Commands in a cell are executed sequentially
print(4)
print(3)

# Unfortunately in IPython only the data on the last line is displayed so use print() if you need more
2
1

# Task 1: In the empty cell below write a Python program to count down from five to zero on separate lines



# Solution 1:
print("\nSolution 1: Counting")
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
1 * 2 + 3 * 4

# We can also save results from expressions in memory locations
# These memory locations are called variables because the values can be changed
# Variables can be named whatever you like. Just avoid the 35 Python keywords.
# Also good if you avoid using names of libraries, functions and datatypes.
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
print("\nSolution 2: Running Total")
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
print("\nSolution 3: Factorials")
factorial = 1
for z in range(1, 20):
    factorial *= z
    print("number", z, "factorial", factorial)

# Task 4: Display the first 20 numbers in the fibonacci sequence
# f1 = 1, f2 = 1, fn = fn-1 + fn-2
# 1, 1, 2, 3, 5, 8, 13



# Solution 4: 
# Multiple assignment statements can be done on one line
print("\nSolution 4: Fibonacci Sequence")
f1, f2 = 1, 1
for _ in range(18):
    print(f1, end=' ')
    f1, f2 = f2, f1 + f2
print(f1, f2)

# Task 5: Count down in steps of 2.25 from 10.5 to -3 inclusive



# Solution 5:
print("\nSolution 5: Counting down")
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

# Task 6: Create a list of numbers from 20 to 0 stepping down by 4 each time

print("\nSolution 6: Using list constructor which can take any iterable value")
list6 = list(range(20, -1, -4))
print(list6)

# Task 7: Create a list of the square numbers from 0**2 to 10**2

print("\nSolution 7 using list comprehension")
list7 = [i**2 for i in range(11)]
print(list7)

# Task 8: Create a list of tuples (i, i**2) for i from 0 to 10

print("\nSolution 8:")
list8 = [(i, i**2) for i in range(11)]
print(list8)

print("\nConditionals in Python use keywords if, elif, else")
for i in range(10):
    if i % 3 == 0:
        print(f"{i} is divisible by three")
    elif i % 3 == 1:
        print(f"{i} is one more than a multiple of three")
    else:
        print(f"{i} is one less than a multiple of three")

# Task 9: Create a list of numbers from 20 to 0 stepping down by 4 each time excluding numbers divisible by 3 

print("\nSolution 9: Using list comprehension with conditional")
list9 = [i for i in range(20, -1, -4) if i % 3 != 0]
print(list9)

print("\nStoring range objects in variables")
r = range(3, 14, 4)
print(r)

print("\nCreating a list object from r")
print(list(r))

# Task 10: Rewrite the following code using nested loops
print("\nTask 10: Examples of range()")
print("range(4) ", end=' ')
for i in range(4):
    print(i, end=' ')
print()

print("range(2, 5) ", end=' ')
for i in range(2, 5):
    print(i, end=' ')
print()

print("range(3, 14, 4) ", end=' ')
for i in range(3, 14, 4):
    print(i, end=' ')
print()

print("range(12, 3, -3) ", end=' ')
for i in range(12, 3, -3):
    print(i, end=' ')
print()

r = range(12, 3, -1)
print(r, end=' ')
for i in r:
    print(i, end=' ')
print()

r = range(12, 3)
print(r, end=' ')
for i in r:
    print(i, end=' ')
print() 

print("\nSolution 10: Using a loop to display different forms of range")
# tuple (1, 2, 3) is a read only version of list [1, 2, 3]
tpl_ranges = ([4], [2, 5], [3, 14, 4], [12, 3, -3], [12, 3, -1], [12, 3])
for range_args in tpl_ranges:
    # *range_args means explode the list and place each item in the ordered argument positions 
    r = range(*range_args)
    print(f"{str(r):20}", end=' ')
    for i in r:
        print(i, end=' ')
    print()
