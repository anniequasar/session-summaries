#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MeetUp 061 - Beginners' Python and Machine Learning - Tue 26 May 2020 - duck typing

Youtube: https://youtu.be/5xTKbYRnvuw
Colab:   https://colab.research.google.com/drive/1tFnyZJ5_Jj8Ol8fIlycn0Eulq1KWus2D
Github:  https://github.com/anniequasar/session-summaries/tree/master/online

Learning objectives:
- duck typing
- exceptions
- overloading operators

@author D Tim Cummings
"""

import sys
from collections import deque, namedtuple, defaultdict, Counter, ChainMap, UserString
from collections.abc import Mapping
import inspect


# Data types
i = 35  # int
f = 4.6  # float
s = "my string"  # str
lst = [5, 7, 9]  # list
t = (3, 'a', 2.3)  # tuple
tf = True  # bool
d = {0: 'a', 2: 'b', 'o': 'value'}  # dict

# find type of a value using type()

print(type(i), type(f), type(s), type(lst), type(t), type(tf), type(d))

# can check type using conditional (!r means print as it is represented internally repr())
if type(s) == str:
    print(f"{s!r} is a str")
else:
    print(f"{s!r} is not a str")

# Task 1: Loop through all the values and find which ones are ints


# Solution 1
for v in (i, f, s, lst, t, tf, d):
    print(f"{v!r} is{' not' if type(v) != int else ''} an int. It is a {type(v).__name__}")

# types are also called classes
print(type(tf))

# classes inherit from super classes. To find the super classes use attribute __bases__
# bool inherits from int so can be used like an int
print(f"base classes or super classes of bool are {bool.__bases__}")
print(f"bool is a subclass of int where True=={True:d} and False=={False:d}")

# Example of using a bool like an int
print(f"5 - True  : {5 - True}")

# Example of using a bool like an int
print(f"4 + False : {4 + False}")

# can use isinstance(obj, class_or_tuple) to check class and super classes
print(f"isinstance(tf, int) : {isinstance(tf, int)}")

# There are more data types in the collections library
# https://docs.python.org/3/library/collections.html

dq = deque('double ended queue')
print(f"dq : {dq}")
Point = namedtuple('Point', ['x', 'y'])
p = Point(123, 456)
print(f"p  : {p}")
dd = defaultdict(list)
for v in (deque, defaultdict, Counter, ChainMap, Point):
    for k in v.__bases__:
        dd[k.__name__].append(v.__name__)
print(f"dd : {dd}")
ctr = Counter('indooroopilly')
print(f"ctr: {ctr}")
cm = ChainMap(dict(dd), dict(ctr))  # ChainMap won't work with dicts which return default values ;)
print(f"cm : {cm}")

# Task 2: Loop through values of dq, p, dd, ctr, cm and find which ones are instances of dict

# Solution 2:
for var_name in ('dq', 'p', 'dd', 'ctr', 'cm'):
    var = globals()[var_name]
    if isinstance(var, dict):
        print(f"instance of dict: {var_name:3} {var}")

# Problem with isinstance is it didn't identify ChainMap as a dict like object
# even though we can lookup a value using a str index key
print(f"cm['o'] : {cm['o']}")

# This is where we use duck typing
# If it quacks like a duck and walks like a duck then, as far as we are concerned, it is a duck (paraphrased)
# Easier to ask for forgiveness later than permission first
# Try to use given datatype assuming it is the correct datatype
# If that doesn't work do something else

# defaultdict is a dict subclass so we expect to be able to use a str index on it
# ChainMap is not a dict subclass but is designed so we can also use a str index
print(f"dd['object']             : {dd['object']}")
print(f"cm['object']             : {cm['object']}")

# Using a str index doesn't work on lists because they need a numerical index
# Gives a TypeError
# print(f"lst['object'] : {lst['object']}")

# To use duck typing we catch the error and perform a different action
# https://docs.python.org/3/tutorial/errors.html
try:
    print(f"lst['object']: {lst['object']}")
except TypeError:
    print(f"lst is a {type(lst).__name__} and so we can't use a str index")

# We often us duck typing in function definitions because we have no control
# over what data types other programmers send to our function

# Task 3: Write a function o_value which returns dict value with index 'o', or if not dict like, value with index 0


# Solution 3:
def o_value(dict_or_list):
    try:
        return dict_or_list['o']
    except TypeError:
        return dict_or_list[0]


for var_name in ('lst', 'dd', 'cm', 'dq', 's'):
    var = globals()[var_name]
    print(f"o_value({var_name:3}): {str(o_value(var)):3} : {var!r}")

# Task 4: Problem with our o_value function is that it won't work with something which can't be indexed eg int
# For some situations this will be the desired behaviour
# However, we will modify our design spec to handle other types, convert to a str and return the first character
# o_value(i)


# Solution 4:
def o_value(dli):
    try:
        return dli['o']
    except TypeError:
        pass
    try:
        return dli[0]
    except TypeError:
        return str(dli)[0]


v1 = None
v2 = ''
v3 = []
for var_name in ('lst', 'dd', 'cm', 'dq', 's', 'i', 'd', 'v1', 'v2', 'v3'):
    var = globals()[var_name]
    try:
        print(f"o_value({var_name:3}): {str(o_value(var)):5} : {var!r}")
    except Exception:
        # be very careful about catching exceptions this way
        # errors will go unnoticed
        # if you do this, often best to re-raise exception
        print(f"o_value({var_name:3}): {sys.exc_info()[0].__name__:12} {str(sys.exc_info()[1]):30} : {var!r}")
        # raise

# If index key doesn't exist can throw a KeyError or provide a default value
print(f"dd['objext'] : {dd['objext']}")  # This does works
# print(f"cm['objext'] : {cm['objext']}")  # This doesn't work

# Task 5: o_value should return None in case of KeyError, IndexError


# Solution 5:
def o_value(dli):
    try:
        return dli.get('o', dli.get(0, None))
    except AttributeError:
        pass
    try:
        return dli[0]
    except TypeError:
        return str(dli)[0]
    except IndexError:
        return None


for var_name in ('lst', 'dd', 'cm', 'dq', 's', 'i', 'd', 'v1', 'v2', 'v3'):
    var = globals()[var_name]
    try:
        print(f"o_value({var_name:3}): {str(o_value(var)):5} : {var!r}")
    except Exception:
        # if you catch all errors this way, often best to re-raise exception
        print(f"o_value({var_name:3}): {sys.exc_info()[0].__name__:12} {str(sys.exc_info()[1]):30} : {var!r}")
        raise


# Full structure of try except
# 1 try, followed by 0 or more excepts each with 0 or more error types
# optional else if no exceptions raised
# optional finally which will always run regardless
def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError as zde:
        # subclass of ArithmeticError
        print("division by zero!", zde)
    except (AttributeError, ArithmeticError):
        print("either an attribute error or arithmetic error other than zero division")
    else:
        print("result is", result)
    finally:
        print("executing finally clause")


divide(5, 2)
divide(5, 0)
# divide("5", "1")
# Other languages (eg Java) use interfaces.
# Python has some concept of interfaces but they are considered not as reliable as duck typing
# collections.abc.Mapping is an interface which looks for existance of __getitem__
for var_name in ('dq', 'p', 'dd', 'ctr', 'cm'):
    var = globals()[var_name]
    if isinstance(var, Mapping):
        print(f"instance of Mapping: {var_name:3} {var}")

# Square brackets [] are just shorthand for calling the __getitem__() method
# To enable [], the writers of ChainMap provided a __getitem__ method
print(f"cm['object']             : {cm['object']}")
print(f"cm.__getitem__('object') : {cm.__getitem__('object')}")

# Task 6: Define a function stutter(v) which returns a str made of every iterable item doubled
# If not iterable then convert to str first. To test for iterable create an iterator using iter()
# stutter('hello'): 'hheelllloo'
# stutter(['ab', 4, 2.3]): 'abab442.32.3'
# stutter(345): '334455'


# Solution 6:
def stutter(arg):
    try:
        iterator = iter(arg)
    except TypeError:
        return stutter(str(arg))
    lst_stutter = []
    for i in iterator:
        s = str(i)
        lst_stutter.append(s)
        lst_stutter.append(s)
    return ''.join(lst_stutter)


print(f"stutter('hello'): {stutter('hello')}")
print(f"stutter(['ab', 4, 2.3]): {stutter(['ab', 4, 2.3])}")
print(f"stutter(345): {stutter(345)}")
print(f"stutter('345'): {stutter('345')}")
print(f"stutter(None): {stutter(None)}")

# Task 7: Create a subclass of str called JavaString which can be used in expressions like JavaString + int
# hint: implement __add__(self, other) to override +


# Solution 7:
class JavaString(str):
    def __add__(self, other):
        try:
            return JavaString(super().__add__(other))
        except TypeError:
            return JavaString(f"{self}{other}")

    def __repr__(self):
        return f"JavaString({super().__repr__()})"


js = JavaString('leading')
print(f"{js!r} + 5 + 4: {js + 5 + 4!r}")

# Task 8: Enhance JavaString to handle expressions like int + JavaString
# hint: implement __radd__(self, other) in JavaString which will be called if int.__add__(JavaString) fails


# Solution 8:
def radd(self, other):
    return JavaString(f"{other}{self}")


JavaString.__radd__ = radd
js = JavaString("trailing")
print(f"89 + {js!r}: {89 + js!r}")

# Problem with what we have done is that all the str methods in the super class return str not JavaString.
print(f"js.upper() : {js.upper()} : type(js.upper()) : {type(js.upper())}")


# collections provides UserString to make subclassing str easier
class MyUserString(UserString):
    def __repr__(self):
        return f"MyUserString({super().__repr__()})"


mus = MyUserString('leading')
# UserString handles types for return values from functions
print(f"mus.upper() : {mus.upper()} : type(mus.upper()) : {type(mus.upper())}")

# Unfortunately for this demo, UserString also adds the JavaString functionality
print(f"{mus!r} + 5 + 4: {mus + 5 + 4!r}")

# However, we can inspect the code for UserString to see how they did it
print(inspect.getsource(UserString.__add__))
print()
print(inspect.getsource(UserString.__radd__))
