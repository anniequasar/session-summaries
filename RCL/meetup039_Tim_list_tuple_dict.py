#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 039 - Beginners Python Support Sessions - Wed 04 Dec 2019 - collection types
Repeat of Meetup026

Wednesday sessions are absolute beginner sessions

Learning objectives:
    Data types: int float str list tuple dict set
    Structure: def if for

@author D Tim Cummings
"""
# Challenge 1: int : Print the results of the following integer arithmetic
# Add 5234 to 317623?
a = 5234
b = 317623
c = a + b
print(c)
print(type(a))
print(type(5234.0))


# Subtract 23423 from 5490872?
print(5490872-23423)
# How many times does 123423 divide into 35387384975 and what is the remainder?
a = 35387384975
b = 123423
print(f"{a} divided by {b} equals {a//b} remainder {a%b} or {divmod(a,b)}")
#
# Challenge 2: float : What is the floating point result from dividing 35387384975 by 123423
print(f"{a} divided by {b} equals {a/b}")
# Find the square root of 2
from math import sqrt
print(f"Square root using math library {sqrt(2)}")
print(f"Square root not using math library {2**0.5}")
#
# Challenge 3: str : Print the results of the following str manipulation
# Concatenate the str '456' to the end of '123'
print('123' + '456')
# Convert the strs '456' and '123' to ints and add them together
print(int('123') + int('456'))
print(int('77', 8))  # octal to decimal
print(int('ff', 16))  # hexadecimal to decimal
print(int('0110', 2)) # binary to decimal
print(f"{6:b}")   # decimal to binary
print(f"{255:x}")  # decimal to hexadecimal
print(f"{int('10000110',2):x}")  # binary to hexadecimal
# Convert the ints 123 and 456 to strs and concatenate them
a = 123
b = 456
print(str(a) + str(b))
#
# Challenge 4: list : Create a new empty list. Append a str, an int and a float
lst = []
lst = list()
lst.append('abc')
lst.append(123)
lst.append(45.0)
print(lst)
lst = lst + ['def', 456, 78.0]
print(lst)

i = 0
while i < len(lst):
    x = lst[i]
    print(i, x, type(x))
    i += 1
for x in lst:
    print(x, type(x))
for i in range(len(lst)):
    print(i, lst[i], type(lst[i]))
# Loop through the items in the list and print each one and its type.

# Create a new list of 3 ints.
lst2 = [1, 2, 3]
# Append the new list to the end of the first list.
lst3 = lst + lst2
print(lst3)
lst.append(lst2)
print(lst)
# Change the second item of the new list to be a str.
lst[1] = str(lst[1])
# Print all items in the new list
print(lst)
#
# Challenge 5: tuple : Can challenge 4 be done with tuples rather than lists
# Hint: tuples use () while lists use []
tpl = ()
tpl = tuple()
tpl = ('anything', 3000, 3.1)
for x in tpl:
    print(f"{x} {type(x)}")
tpl2 = (4, 5, 6)
tpl3 = tpl + tpl2
lst4 = list(tpl3)
lst4[1] = str(lst4[1])
tpl3 = tuple(lst4)
print(tpl3)
# Challenge 6: Specify length of side (eg side = 4) and then store a square of that size in a 2D list.
#  Check program still works when side = 10
# [['S', 'S', 'S', 'S'],
#  ['S', ' ', ' ', 'S'],
#  ['S', ' ', ' ', 'S'],
#  ['S', 'S', 'S', 'S']]
side = 10
square = []
for i in range(side):
    if i not in (0, side - 1):
        row = ['S'] + [' '] * (side - 2) + ['S']
    else:
        row = ['S'] * side
    # row[side - 1 - i] = '/'
    square.append(row)
    square[i][side - 1 - i] = '/'
from pprint import pprint
pprint(square)
# Advanced: Add a diagonal to shape in 2D list and print out contents of array where lst[0][0] is in lower left corner
# S S S /
# S   / S
# S /   S
# / S S S
#
# Challenge 7: Repeat challenge 6 using a dict rather than a 2D list. Key for dict will be tuples with x,y coordinates.
# {(0, 0): 'S', (3, 0): 'S', (0, 3): 'S', (3, 3): 'S',
#  (0, 1): 'S', (3, 1): 'S', (1, 0): 'S', (1, 3): 'S',
#  (0, 2): 'S', (3, 2): 'S', (2, 0): 'S', (2, 3): 'S'}
#
# Challenge 8: set : Simulate rolling a die 100 times each time adding result into a set
#
# Challenge 9: Write a function to find all the factors of a number. A factor is an integer which divides into another
# integer with no remainder.

