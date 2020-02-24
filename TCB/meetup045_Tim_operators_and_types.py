#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 045 - Beginners Python Support Sessions - 4th Feb 2020 - Data types, Variables, Console, Program
Repeat of RCL meetups 001, 018, 030

Learning objectives:
    Data types: int, float, str, list
    Variables: create, assign, update
    Console: using the console for immediate response
    Program: putting multiple python commands in a script to run them all at once, for/while loop, if else

@author D Tim Cummings

Challenge 1: Install Software
    Python 3 from https://www.python.org/downloads/
    PyCharm Community 2019.3.2 (free) https://www.jetbrains.com/pycharm/download/
    EduTools plugin (optional) https://www.jetbrains.com/help/education/install-edutools-plugin.html?section=PyCharm

    For those interested in my children's Python coding course
    see https://pythonator.com (makes Python coders out of gamers)
    This course would be good for adults too if they could play
    Minecraft or Minetest as well as the children can!

Challenge 2: Browse courses in PyCharm Edu for "pythonator b1 easy" and do while waiting for others' installations

Challenge 3: Using Python console to work with numbers and operators
    Enter simple sums (eg 5+5) and press <enter> to see answer
    Determine what each of the following operators do: + - * / // ** %
    Advanced: Determine what these operators do: | & << >> ^ ~

Challenge 4: Storing values in variables in console
    Store numbers in variables (using =)
    What is the difference between int and float number types
    Store text in variables (Using "" or '' or """""" or '''''')
    Store results of formula in variable
    Display contents of variable
    Replacing contents of variable with another value (eg increment by 1)
    Advanced: What do type(), str(), repr() tell you about a variable eg type(my_var)

Challenge 5: Using operators with text
    Determine what each of the following operators do on text: + * (str + str and str * int)

Challenge 6: Create a list. (comma separated sequence of values surrounded by square brackets)
    Show the first item in the list. (use [0])
    Show the last item in the list. (use [-1])
    Change the third item.
    Change the last item.
    Advanced: What do the following slicing operations do? [1:4], [:3], [-3:], [1:6:2]
    Advanced: Try all these operations on a str and see which ones work

Challenge 7: Write a program which displays each member of a list on a new line (use print())
    Advanced: Write program to display every second member of the list on a new line

Challenge 8: What do the conditional operators mean: >, <, ==, !=, >=, <=, in, is, and, or, not, is not

Challenge 9: Write a while loop which will print out the numbers 0 to 20

Challenge 10: Create a list of numbers as text ["zero", "one", "two", ..., "twenty"].
Write a program which prints the index of each element in the list and its name.
Should print out
0 zero
1 one
2 two
...
20 twenty

Challenge 11: Print out the names of all numbers up to 29 using the same list

"""

# Challenge 3: Using Python console to work with numbers and operators
#     Enter simple sums (eg 5+5) and press <enter> to see answer
#     Determine what each of the following operators do: + - * / // ** %
#     Advanced: Determine what these bitwise operators do: | & << >> ^ ~

27 + 5   # 32  : addition
27 - 5   # 22  : subtraction
27 * 5   # 135 : multiplication
27 / 5   # 5.4 : floating point division
27 // 5  # 5   : integer division
27 % 5   # 2   : remainder after integer division (modulo)
27 ** 5  # 14348907 : raised to the power of

14 | 7   # 15  : bitwise OR  1110 | 0111 = 1111 = 15
14 & 7   # 6   : bitwise AND 1110 & 0111 = 0110 = 6
14 ^ 7   # 9   : bitwise XOR 1110 ^ 0111 = 1001 = 9
5 << 1   # 10  : bitwise shift left 0101 << 1 = 1010 = 10
5 >> 1   # 2   : bitwise shift right 0101 >> 1 == 0010 = 2
~5       # -6  : bitwise NOT bin(5 & 0xF) == 0b0101, bin(~5 & 0xF) == 0b1010

# Challenge 4: Storing values in variables in console
#     Store numbers in variables (using =)
#     What is the difference between int and float number types
#     Store text in variables (Using "" or '' or """""" or '''''')
#     Store results of formula in variable
#     Display contents of variable
#     Replacing contents of variable with another value (eg increment by 1)
#     Advanced: What do type(), str(), repr() tell you about a variable eg type(my_var)

a = 12   # int
b = 29   # int
c = 3.14  # float
d = 3.0   # float
# int are integers or whole numbers so they have no decimal places
e = 250000000000000000000000000000000
f = 25 / 7
i = e // 7
i += 1
# ints can have more significant digits than floats (about 17)
# floats can't store decimal numbers exactly so good for science but not for accounting (use cents for accounting)
g = 1.1 + 2.2  # 3.3000000000000003

s1 = "hello"
s2 = 'world'
s3 = """pythonistas"""  # you can also include new lines in triple double quoted string
s4 = '''rejoice'''      # you can also include new lines in triple single quoted string
s5 = "Don't fret"
s6 = '''He said "Why don't you?"'''
s7 = 'He said "Why don\'t you?"'
s1  # displays contents of s1 in console (not when run from a program) as internally represented (surrounded by quotes)
print(s1)  # displays contents as non technical user would want it displayed.
print(type(s1))  # displays the type of the data stored in s1 eg <class 'str'>
print(repr(s1))  # displays internal representation of variable, In the console print(repr(v)) should be same as v
print(str(g))  # converts data to string before printing

# Escape characters - used to change meaning of character
# \' changes ' from end of string mark to single quote (when string starts with single quote)
# \" changes " from end of string mark to double quote (when string starts with double quote)
# \\ changes \ from escape character to back slash
# \n changes n from the letter n to a new line
# \r changes r from the letter r to a carriage return
# \t changes t from the letter t to a tab
# \<newline> where <newline> is a newline character ignores back slash and <newline>
# \xhh is 8-bit character with hexadecimal hh
# \uxxxx is 16-bit unicode character with hexadecimal xxxx
# \Uxxxxxxxx is 32-bit unicode character with hexadecimal xxxxxxxx
# \N{name} unicode character by name eg '\N{WEIERSTRASS ELLIPTIC FUNCTION} '

# Thai digits. Could also use '\N{THAI DIGIT ONE}\N{THAI DIGIT TWO}...'
s = '\u0e51\u0e52\u0e53\u0e54\u0e55\u0e56\u0e57\u0e58\u0e59\u0e50'
print(s, int(s))

# String types
sb = b'string of bytes which is the default for Python 2'
su = u'string of unicode characters which is the default for Python 3'
sr = r'raw string in which \ has no special meaning. useful for regular expressions'
sf = f'format string to show values 2 + 3 = {2+3}'

# Challenge 5: Using operators with text
#     Determine what each of the following operators do on text: + * (str + str and str * int)

print("well " * 3 + " three holes in the ground")

# Challenge 6: Create a list. (comma separated sequence of values surrounded by square brackets)
#     Show the first item in the list. (use [0])
#     Show the last item in the list. (use len())
#     Change the third item.
#     Change the last item.
#     Advanced: What do the following slicing operations do? [1:4], [:3], [-3:], [1:6:2]
#     Advanced: Try all these operations on a str and see which ones work

my_list = [6, 5, 4, 3, 2, 1, 0]
my_list[0]
print(my_list[0])
print(len(my_list))
print(my_list[len(my_list) - 1])
print(my_list[-1])
my_list[2] = "four"
my_list[-1] = 'blast off'
print(my_list[1:4])  # items with index 1 to 3
print(my_list[:3])  # items with index up to but not including 3
print(my_list[3:])  # items from index 3 on
print(my_list[-3:])  # items starting from 3 from right hand end to the right hand end
print(my_list[1:6:2])  # items starting from index 1 up to but excluding index 6 taking every second item

s = 'abcdefg'
print(s[0])
print(len(s))
print(s[-1])
# s[len(s) - 1] = 'b'  # strings don't support item assignment because they are immutable
print(s[1:4])  # chars with index 1 to 3
print(s[:3])  # chars with index up to but not including 3
print(s[3:])  # chars from index 3 on
print(s[-3:])  # chars starting from 3 from right hand end to the right hand end
print(s[1:6:2])  # chars starting from 3 from right hand end to the right hand end

# Challenge 7: Write a program which displays each member of a list on a new line (use print())
#     Advanced: Write program to display every second member of the list on a new line

my_list = [6, 5, 4, 3, 2, 1, 'blast off']

print(my_list[0])
print(my_list[1])
print(my_list[2])
print(my_list[3])
print(my_list[4])
print(my_list[5])
print(my_list[6])

# Solution to challenge 7 using for loop
for v in my_list:
    print(v)

for v in my_list[::2]:
    print(v)

for my_var in ['one', 'two', 'three']:
    print(my_var)

print(my_var)

# Challenge 8: What do the conditional operators mean: >, <, ==, !=, >=, <=, in, is, and, or, not, is not. What data type do they return

# == is equal to
# != is not equal to
# >  is greater than
# <  is less than
# >= is greater than or equal to
# <= is less than or equal to
# in is in the sequence
# is is identical to

# Compare numbers
3 < 5  # True (ints)
3.7 < 4  # True (float compared to int)
4.0 == 4  # True (float compared to int)
6+5j == 5j+6  # True
6+5j > 6  # (Type error. Can't compare complex with int but can check equality)
complex(6, 0) == 6  # True (complex and int)
7 in [4, 7, 9]  # True
True and False   # False
True or False   # True
not False   # True
n = None
n is None   # True
lst1 = [2, 5, 8]
lst2 = lst1
lst3 = lst1.copy()
lst1 is lst2  # True (Same list in memory. change to one affects the other)
lst1 is lst3  # False (lst3 occupies different memory to lst1)
lst1 is not lst3  # True

# Comparing letters <, >  compares unicode values
'a' > 'd'  # False
'a' > 'D'  # True  (comparison of unicode values. lower case ascii after upper case ascii)
'A' > 'd'  # False
'd' in 'abracadabra'  # True
'e' in 'abracadabra'  # False
'cad' in 'abracadabra'  # True

# Challenge 9: Write a while loop which will print out the numbers 0 to 20

i = 0
while i <= 20:
    print(i)
    i += 1

# Challenge 10: Create a list of numbers as text ["zero", "one", "two", ..., "twenty"].
# Write a program which prints the index of each element in the list and its name.
# Should print out
# 0 zero
# 1 one
# 2 two
# ...
# 20 twenty

numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
           "nineteen", "twenty"]
i = 0
while i <= 20:
    print(i, numbers[i])
    i += 1

# Demonstrate if else statement
i = 0
while i <= 20:
    if i % 2 == 0:
        print("even", end=' ')
    else:
        print("odd ", end=' ')
    print(i, numbers[i])
    i += 1

# Challenge 11: Print out the names of all numbers up to 29 using the same list
i = 0
while i < 30:
    if i <= 20:
        print(i, numbers[i])
    else:
        print(i, numbers[-1] + "-" + numbers[i-20])
    i += 1

