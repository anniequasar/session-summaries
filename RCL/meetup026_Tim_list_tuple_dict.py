# coding=utf-8
"""
MeetUp 026 - Beginners Python Support Sessions - Wed 04 Sep 2019 - collection types

Learning objectives:
    Data types: int float str list tuple dict set
    Structure: def if for

@author D Tim Cummings
"""
# Challenge 1: int : Print the results of the following integer arithmetic
# Add 5234 to 317623?
a = 5234 + 317623
print(a)
print("The result of adding 5234 to 317623 = ", a)
# Subtract 23423 from 5490872?
print("The result of subtracting 23423 from 5490872 is", 5490872 - 23423)
# How many times does 123423 divide into 35387384975 and what is the remainder?
print("35387384975 divided by 123423 is", 35387384975 // 123423, "remainder", 35387384975 % 123423)

# Challenge 2: float : What is the floating point result from dividing 35387384975 by 123423
# Find the square root of 2
print("35387384975 divided by 123423 is", 35387384975 / 123423)
import math
print("Square root of 2 is 2**0.5", 2**0.5, "math.sqrt(2)", math.sqrt(2))


# Challenge 3: str : Print the results of the following str manipulation
# Concatenate the str '456' to the end of '123'
s = '123'
f = '456'
print(s+f)
# Convert the strs '456' and '123' to ints and add them together
print(int(s)+int(f))
# Convert the ints 123 and 456 to strs and concatenate them
a=123
b=456
print(str(a)+str(b))

# Challenge 4: list : Create a new empty list. Append a str, an int and a float
lst = []
lst = list()
lst.append('anything that you are ')
lst.append(3000)
lst.append(3.1)
# Loop through the items in the list and print each one and its type.
for i in lst:
    print(i, type(i))
# Create a new list of 3 ints.
lst2 = [1,2,3]
# Append the new list to the end of the first list.
lst3 = lst + lst2
# Change the second item of the new list to be a str.
lst3[1] = 'three thousand'
# Print all items in the new list
print(lst3)

# Challenge 5: tuple : Can challenge 4 be done with tuples rather than lists
# Hint: tuples use () while lists use []
tpl = ('anything', 3000, 3.1)
# Loop through the items in the tuple and print each one and its type.
for i in tpl:
    print(i, type(i))
# Create a new tuple of 3 ints.
tpl2 = (1,2,3)
# Append the new tuple to the end of the first tuple.
tpl3 = tpl + tpl2
# Change the second item of the new tuple to be a str.
# lst3[1] = 'three thousand'  # won't work with tuples
# Print all items in the new tuple
print(tpl3)

# Challenge 6: Specify length of side (eg side = 4) and then store a square of that size in
# a 2D list.
# Check program still works when side = 10
# [['S', 'S', 'S', 'S'],
# ['S', ' ', ' ', 'S'],
# ['S', ' ', ' ', 'S'],
# ['S', 'S', 'S', 'S']]
# Advanced: Add a diagonal to shape in 2D list and print out contents of array
# where lst[0][0] is in lower left corner
# S S S /
# S   / S
# S /   S
# / S S S

side = 10
square = []
row = []
for i in range(side):
    if i in (0, side-1):
        row = ['S'] * side
    else:
        row = ['S'] + [' '] * (side-2) + ['S']
    square.append(row)
for i in range(side):
    square[i][i] = '/'
for i in range(side-1, -1, -1):
    print(square[i])

# Challenge 7: Repeat challenge 6 using a dict rather than a 2D list. Key for dict will be tuples with x,y coordinates.
# {(0, 0): 'S', (3, 0): 'S', (0, 3): 'S', (3, 3): 'S',
#  (0, 1): 'S', (3, 1): 'S', (1, 0): 'S', (1, 3): 'S',
#  (0, 2): 'S', (3, 2): 'S', (2, 0): 'S', (2, 3): 'S'}

# Challenge 8: set : Simulate rolling a die 100 times each time adding result into a set

# Challenge 9: Write a function to find all the factors of a number. A factor is an integer which divides into another
# integer with no remainder.

