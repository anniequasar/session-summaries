#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 049 - Beginners Python Support Sessions - Tue 03 Mar 2020 - list tuple dict
Repeat of Meetup039

First week of month are absolute beginner sessions. This one continues on from MeetUp045

Learning objectives:
    Data types: int float str list tuple dict set
    Structure: if for while import

@author D Tim Cummings

Challenge 1: int : Print the results of the following integer arithmetic
Add 5234 to 317623?
Subtract 23423 from 5490872?
How many times does 123423 divide into 35387384975 and what is the remainder?

Challenge 2: float : What is the floating point result from dividing 35387384975 by 123423
Find the square root of 2

Challenge 3: str : Print the results of the following str manipulation
Concatenate the str '456' to the end of '123'
Convert the strs '456' and '123' to ints and add them together
Convert the ints 123 and 456 to strs and concatenate them

Challenge 4: list : Create a new empty list. Append a str, an int and a float
Loop through the items in the list and print each one and its type.
Create a new list of 3 ints.
Append the new list to the end of the first list.
Change the second item of the new list to be a str.
Print all items in the new list

Challenge 5: tuple : Can challenge 4 be done with tuples rather than lists
Hint: tuples use () while lists use []

Challenge 6: Find the three most common words in this module's docstring (__doc__)
Create lst_word, a list of all the words in __doc__ using .split()
Create a dict using the word as the key and the count as the value using a loop and d[word] += 1
Advanced: Sort the dict based on the count in descending order using sorted(iterable, key, reverse)
Compare with collections.Counter(lst_word)

Challenge 7: set : Simulate rolling a die 100 times each time adding result into a set
"""
# Challenge 1: int : Print the results of the following integer arithmetic
# Add 5234 to 317623?
# we can store the integers in variables
a = 5234
b = 317623
# we can store the result in a variable
c = a + b
# we can print using format strings f"" (Python 3.6 or later)
print(f"{a} + {b} = {c}")

# use the type() function to find out the data type of an object
print(f"type(a) = {type(a)}\ntype(b) = {type(b)}\ntype(c) = {type(c)}\ntype(5234.0) = {type(5234.0)}")

# Subtract 23423 from 5490872?
# we don't have to use variables
print(f"5490872 - 23423 = {5490872 - 23423}")

# How many times does 123423 divide into 35387384975 and what is the remainder?
# integer arithmetic uses // for divide and % for modulo (remainder)
a = 35387384975
b = 123423
print(f"{a} divided by {b} equals {a//b} remainder {a%b} or {divmod(a,b)}")

# Challenge 2: float : What is the floating point result from dividing 35387384975 by 123423
# floating point arithmetic uses / for divide
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
# other ways of converting ints
print(f"int('77', 8) = {int('77', 8)} (octal to decimal)")
print(f"int('ff', 16) = {int('ff', 16)} (hexadecimal to decimal)")
print(f"int('0110', 2) = {int('0110', 2)} (binary to decimal)")
print(f"6 formatted as binary is {6:b} (decimal to binary)")
print(f"255 formatted as hexadecimal is {255:x} (decimal to hexadecimal)")
print(f"int('10000110',2) formatted as hexadecimal is {int('10000110',2):x} (binary to hexadecimal)")
# Convert the ints 123 and 456 to strs and concatenate them
a = 123
b = 456
print(str(a) + str(b))
#
# Challenge 4: list : Create a new empty list. Append a str, an int and a float
# create an empty list
lst = []
# alternative way of creating an empty list (supposed to be clearer)
lst = list()
# append a str an int and a float
lst.append('abc')
lst.append(123)
lst.append(45.0)
print(lst)
# can concatenate lists like we concatenate strs
lst = lst + ['def', 456, 78.0]
print(lst)

# Loop through the items in the list and print each one and its type.
# example while loop
i = 0
while i < len(lst):
    x = lst[i]
    print(f"{i:2}  {x:>5}  {type(x)}")
    i += 1
# example for loop if you need to know which item in list
for i in range(len(lst)):
    print(f"{i:2}  {lst[i]:>5}  {type(lst[i])}")
# example for loop if you don't need to know which item in list
for x in lst:
    print(f"    {x:>5}  {type(x)}")

# Create a new list of 3 ints.
lst2 = [1, 2, 3]
# Append the new list to the end of the first list.
lst3 = lst + lst2  # this concatenates lists rather than appends
print(f"Concatenated list: {lst3}")
lst.append(lst2)
print(f"Appended list:     {lst}")
# Change the second item of the new list to be a str. Print all items in the new list
lst[1] = str(lst[1])
print(f"Second item should be a str: {lst}")

# Challenge 5: tuple : Can challenge 4 be done with tuples rather than lists
# Hint: tuples use () while lists use []

# can create a tuple using parentheses
tpl = ()
# alternatively can create a tuple from the constructor
tpl = tuple()
# can't append items to tuple because immutable. Can create a new tuple with data
tpl = ('anything', 3000, 3.1)
# can loop through anything iterable like lists, tuples, sets, etc
for x in tpl:
    print(f"    {x:>5}  {type(x)}")
# create a new tuple with 3 ints
tpl2 = (4, 5, 6)
# concatenate two tuples to create a new tuple
tpl3 = tpl + tpl2
print(f"Concatenated tuple:   {tpl3}")
# can't append to tuple but can create a new tuple based on existing tuple
# * before a tuple or list expands the tuple or list to its elements
tpl3 = (*tpl, tpl2)
print(f"New 'appended' tuple: {tpl3}")
# can't change second item of tuple because immutable
# convert tuple to a list so can make the change and then convert back to tuple
lst4 = list(tpl3)
lst4[1] = str(lst4[1])
tpl3 = tuple(lst4)
print(f"Second item should be a str: {tpl3}")

# Challenge 6: Find the three most common words in this module's docstring (__doc__)
# Create lst_word, a list of all the words in __doc__ using .split()
# Create a dict using the word as the key and the count as the value using a loop and d[word] += 1
# Advanced: Sort the dict based on the count in descending order using sorted(iterable, key, reverse)
# Compare with collections.Counter(lst_word)
lst_word = __doc__.split()
print(f"lst_word {lst_word}")
import collections
print(f"collections {collections.Counter(lst_word)}")
dct_word = {}
for word in lst_word:
    if word in dct_word:
        dct_word[word] += 1
    else:
        dct_word[word] = 1
print(f"dct_word {dct_word}")
lst_counts = sorted(dct_word.values(), reverse=True)
print(f"lst_counts {lst_counts}")
dct_word_sorted = {}
d = dct_word.copy()
while len(lst_counts) > 0:
    for k, v in d.items():
        if v == lst_counts[0]:
            dct_word_sorted[k] = v
            del(d[k])  # deletes item from dictionary d with key k
            del(lst_counts[0])  # deletes element from list lst_counts at index 0
            break  # exits enclosing loop (for loop)
print(f"lst_counts {lst_counts}")
print(f"dct_word_sorted while for if {dct_word_sorted}")
# Advanced: using dict comprehension, sorted() with key parameter, loop through dct_word.items()
dct_word_sorted = {k: v for k, v in sorted(dct_word.items(), key=lambda item: item[1], reverse=True)}
print(f"{{k: v for k, v in sorted(dct_word.items(), key=lambda item: item[1], reverse=True)}} {dct_word_sorted}")
# Advanced: using dict comprehension, sorted() with key parameter, loop through dct_word.keys()
dct_word_sorted = {k: dct_word[k] for k in sorted(dct_word, key=dct_word.get, reverse=True)}
print(f"{{k: dct_word[k] for k in sorted(dct_word, key=dct_word.get, reverse=True)}} {dct_word_sorted}")

# Challenge 7: set : Simulate rolling a die 100 times each time adding result into a set
# Advanced: count how many times each value was rolled
from random import randrange
st_roll = set()
dct_roll = {}
for i in range(100):
    r = randrange(1, 7)
    st_roll.add(r)
    dct_roll[r] = dct_roll.get(r, 0) + 1
print(f"st_roll shows which die values occurred at least once in the 100 rolls  {st_roll}")
print(f"dct_roll shows how many rolls for each value (advanced)                 {dct_roll}")

