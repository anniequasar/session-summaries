# -*- coding: utf-8 -*-
"""MeetUp 141 - Beginners' Python and Machine Learning - 05 Apr 2022 - Getting Started 3

Learning objectives:
- Interactive python
- Using builtin functions
- Scripting python
- Program structures: scripts, conditionals, loops

Links:
- Colab:   https://colab.research.google.com/drive/1jJGVXCfZIv9qBZTZOc7-ar0-GhfgdrYi
- Youtube: https://youtu.be/gY_puqn964M
- Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/284934591/
- Github:  https://github.com/anniequasar/session-summaries/tree/master/online

@author D Tim Cummings

This session will show you how to use the builtin functions which come with Python. https://docs.python.org/3/library/functions.html

It is the third in the series targeted at absolute beginners after meetup 136.

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text
- use ? or Help menu for help
- see Tools menu > Keyboard shortcuts
"""

# First we will start with some code to get the list of builtin functions 
# Code is too advanced for beginners but shows what a Python script looks like

# built-in functions are not keywords so they can be overridden but are still available by default (without import)
# However we need to import builtins if we want to see the list of built-in functions ;) 
import builtins
import pydoc
print("Meetup 141 Built-in functions and classes\n")
lst_functions = [f for f in dir(builtins) if f[0].upper() != f[0]]
lst_classes = [f for f in dir(builtins) if f[0].lower() != f[0]]
lst_privates = [f for f in dir(builtins) if f[0] == '_']
col_width = max([len(s) for s in dir(builtins)])
cols = 7
for group, lst in zip(['Classes', 'Private', 'Functions'], [lst_classes, lst_privates, lst_functions]):
    print(group)
    # We have to print in rows but make it look like we are printing in columns
    rows = len(lst) // cols + 1
    for row in range(rows):
        print()
        for col in range(cols):
            idx = row + col * rows
            if idx < len(lst):
                print(f"{lst[idx]:{col_width}} ", end=' ')
    print('\n')

# Most important built in function is help. You can even call help on itself
# To call interactive help - decomment the following line
# help()

# To call help on another function (eg the all function)
# Decomment following line to get paged output requiring user to press <space> to page and q to quit
# help(all)

# To get help functionality in a Python script without script paging output
print(pydoc.render_doc(all, "Help on %s"))

# IPython will display the result of the last expression in a cell. Python requires a call to print 
# all([True, True, False, True])             # IPython - doesn't need print
print(f"{all([True, True, False, True])=}")  # Python or IPython - uses logging function of f-strings

print(f"{all([True, True, True, True])=}")

# The list can contain conditional expressions which evaluate to True or False
# all([True, True, 3==3, 5>1])                    # IPython
print(f"{(v := all([True, True, 3==3, 5>1]))=}")  # Python >= 3.8 or IPython >= 3.8

# IPython stores the results of the last expression evaluated in a special variable called _
# In Python >= 3.8 use walrus operator to achieve similar effect
# lst_conditions = [len("all")==3, "c" > "a", True, 5>5, _]  # IPython
lst_conditions = [len("all")==3, "c" > "a", True, 5>5, v]    # Python >= 3.8 or IPython >= 3.8
print(f"{lst_conditions=}")
print(f"{all(lst_conditions)=}")

# Challenge 1 - Get help on 'any' function and come up with an example where it would be used

# Solution 1
# help('any')  # can use str name of function rather than function itself. Useful for keywords
print("\nSolution 1")
pydoc.render_doc('any', "Help on %s")
# Example: If you had a list of components and any one of them is considered to be dangerous goods then then the whole item is considered dangerous
# Code example (beginner). If any of a list of switches are on
print(f"{any([False, True, False, False])=}")
# Code example (advanced). You have a word and want to check if any of a group of letters are in the word
print("\nSolution 1 - advanced")
word = "beginners' python"
print(f"{any(l in word for l in 'abcd')=}")
print()

"""# Data type functions"""

# types: bool, bytearray, bytes, complex, dict, float, frozenset, int, list, memoryview, object, set, str, tuple

# Data type functions can create a new object of the given type
# For example a new empty list can be created using lst = list(), or lst = [] 
lst = list()
print(f"{lst=}")

# These functions can be used to convert from one type to another
print(f"{int(12)=}, {float(12)=}, {complex(12)=}, {str(12)=}")

print(f"{tuple([1, 2, 3, 2])=}, {list((1, 2, 3, 2))=}, {set((1, 2, 3, 2))=}, {frozenset((1, 2, 3, 2))=}")

# Argument to these collection functions is an iterable which includes str
set('kayak'), list('kayak')

# Challenge 2 - create a list of the unique characters in "beginners' python and machine learning"

# Solution 2 - introducing sorted()
print(f"\nSolution 2")
print(f"""{sorted(set("beginners' python and machine learning"))=}""")
print()

# mutable types = bytearray, dict, list, set
# immutable types = bool, bytes, complex, float, frozenset, int, memoryview, object, str, tuple

"""## `dict`"""

# As well as help, you can use __doc__ attribute on any function to get the docstring of that function
print(dict.__doc__)
print()

# different ways of creating a dict. First is using kwargs
print(f"{dict(a='alfa', b='bravo', c='charlie')=}")

# creating a dict using iterable
print(f"{dict([('p', 'papa'), ('y', 'yankee'), ])=}")

# Challenge 3 - Create a dictionary of the following roman numerals
# 1=I, 5=V, 10=X, 50=L, 100=C, 500=D, 1000=M

# Solution 3 - introducing zip
print("\nSolution 3")
dct_roman = dict(zip([1, 5, 10, 50, 100, 500, 1000], "IVXLCDM"))
print(f"{dct_roman=}")
print()

"""# Iterables and iterators

`all`
`any`
`enumerate`
`filter`
`iter`
`len`
`map`
`max`
`min`
`next`
`range`
`reversed`
`slice`
`sorted`
`sum`
`zip`

Iterable - an object you can iterate over

Iterator - the object which iterates (can only call next() on an iterator)

Confusing because iterators are iterable but many iterables are not iterators
"""

# max, min, sum can perform mathematical operations over iterable
print(f"{max(dct_roman.keys())=}")

# When a dict is used as an iterable it is assumed that iterator will use keys
print(f"{min(dct_roman)=}")

print(f"{sum(dct_roman)=}")

# for loop creates an iterator from the iterable dct_roman.keys()
print("\nfor i in dct_roman")
for i in dct_roman:
    print(i)
# other examples of iterables are list, tuple, set, str, dict.values(), dict.items()

# We can do that manually
print("\nprint(next(iter_roman))")
iter_roman = iter(dct_roman)
print(next(iter_roman))
print(next(iter_roman))
print(next(iter_roman))
print(next(iter_roman))
print(next(iter_roman))
print(next(iter_roman))
print(next(iter_roman))
# if I call next() one more time I will get StopIteraction exception which is how for loop knows when to stop
# print(next(iter_roman))

print(pydoc.render_doc(iter, "Help as %s"))

# Challenge 4 - convert dct_roman into a list of key value tuple pairs
# [(1, 'I'), (5, 'V'), ...] without using dct_roman.items()
# Instead use dct_roman.keys() and dct_roman.values()
# You would use a ist of key value tuple pairs rather than dict if there is a chance there are duplicates in the keys
# For example pymongo uses this for specifying sort order

# Solution 4:
print("\nSolution 4")
print(f"{list(zip(dct_roman.keys(), dct_roman.values()))=}")

# enumerate in for loops
print("for loop using values without counter")
for v in lst_privates:
    print(v)
print("for loop using counter - using len() to get length of the iterable and range() to get sequence of integers")
for i in range(len(lst_privates)):
    print(i, lst_privates[i])
print("for loop using counter and values")
for i, v in enumerate(lst_privates):
    print(i, v)

# Challenge 5: Print all the builtin functions from lst_functions 6 per row

# Solution 5:
print("\nSolution 5")
for i, v in enumerate(lst_functions):
    if i%6 == 0:
        print()
    print(f"{v:20s}", end=' ')
print()
print()

# filter allows us to define a function will return True or False and filter out the Falses
# For example to only show functions which start with a vowel
def starts_with_vowel(s):
    return s[0] in 'aeiou'
print(f"{list(filter(starts_with_vowel, lst_functions))=}")

# map is used to convert values to a new values. eg to convert roman numerals to hexadecimal
print(f"{list(map(hex, dct_roman))=}")

# map is used to convert values to a new values. eg to convert roman numerals to hexadecimal
dct_hex_roman = dict(zip(map(hex, dct_roman), dct_roman.values()))
print(f"{dct_hex_roman=}")

"""# Math functions

- `abs` : absolute value (convert negative values to positive)
- `divmod` : `d, m = divmod(i, j)` is equivalent to `d, m = i // j, i % j`
- `pow` : `pow(base,exp)` is equivalent to `base**exp`, `pow(base,exp,mod)` is equivalent to `base**exp % mod` but faster
- `round` : `round(number[,ndigits])` rounds to ndigits precision after decimal point (round half even)
"""

# Challenge 6: Find the quotient and remainder from integer division of dividend 25 divisor 7

# Solution 6
print("\nSolution 6")
print(f"{divmod(25, 7)=}\n")

"""# Classes and Object Oriented Programming

`callable` `classmethod` `delattr` `dir` `getattr` `hasattr` `isinstance` `issubclass` `property` `setattr` `staticmethod` `super` `type`

Most of the class functions are beyond the scope of today's session. However we will look at how to check the type of a value.
"""

# callable classmethod delattr dir getattr hasattr isinstance issubclass property setattr staticmethod super type

# Can check for types using the built-in type function (exact match) or isinstance function (class or subclass) 
print(f"{type(3) == int=}")

print(f"{type(3) == bool=}")

print(f"{type(False) == bool=}")

print(f"{type(False) == int=}")

print(f"{isinstance(True, bool)=}")

print(f"{isinstance(True, int)=} because bool is a subclass of int")  

print(f"{isinstance(3, bool)=}")

"""# Functions are objects too"""

print(pydoc.render_doc(callable, "Help on %s"))

# callable functions are called by using the function name followed by parentheses. 
print(f"{callable(print)=}")

print(f"{callable(__doc__)=}")

print("Hence we can call print using print() but we can't call __doc__ using __doc__()")
