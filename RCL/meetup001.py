"""
MeetUp 001 - Beginners Python Support Sessions - Data types, Variables, Console, Program

Learning objectives:

    Data types: int, float, str, list

    Variables: create, assign, update

    Console: using the console for immediate response

    Program: putting multiple python commands in a script to run them all at once, for/while loop, if else

@author: D Tim Cummings

Challenge 1: Install Software

    Python 3 from https://www.python.org/downloads/

    PyCharm Edu 2018.3 from https://www.jetbrains.com/education/download/#section=pycharm-edu


    For those interested in my children's Python coding course

    see https://pythonator.com (makes Python coders out of gamers)

    This course would be good for adults too if they could play

    Minecraft or Minetest as well as the children!

Challenge 2: Browse courses in PyCharm Edu for "pythonator b1 easy" and do while waiting for others' installations 
"""

# Challenge 3: Using Python console to work with numbers and operators

#     Enter simple sums (eg 5+5) and press <enter> to see answer

#     Determine what each of the following operators do: + - * / // ** %

#     Advanced: Determine what these bitwise operators do: | & << >>



27 + 5   # 32  : addition

27 - 5   # 22  : subtraction

27 * 5   # 135 : multiplication

27 / 5   # 5.4 : floating point division

27 // 5  # 5   : integer division

27 % 5   # 2   : remainder after integer division (modulo)

27 ** 5  # 14348907 : raised to the power of

1*2+3*4  # 14  : order of operations

(1*2+3)*4  # 20 : order of operations with parentheses


14 | 7   # 15  : bitwise OR  1110 | 0111 = 1111 = 15

14 & 7   # 6   : bitwise AND 1110 & 0111 = 0110 = 6

5 << 1   # 10  : bitwise shift left 0101 << 1 = 1010 = 10

5 >> 1   # 2   : bitwise shift right 0101 >> 1 == 0010 = 2


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



# Challenge 5: Using operators with text

#     Determine what each of the following operators do on text: + * (str + str and str * int)


print("well " * 3 + " three holes in the ground")


# Challenge 6: Create a list. (comma separated sequence of values surrounded by square brackets)

#     Show the first item in the list. (use [0])

#     Show the last item in the list. (use len())

#     Change the third item.

#     Change the last item.

#     Advanced: What do the following slicing operations do? [1:4], [:3], [-3:]

#     Advanced: Try all these operations on a str and see which ones work



my_list = [6, 5, 4, 3, 2, 1, 0]

print(my_list[0])

print(len(my_list))

print(my_list[len(my_list) - 1])

my_list[2] = "four"

my_list[len(my_list) - 1] = 'blast off'

print(my_list[1:4])  # items with index 1 to 3

print(my_list[:3])  # items with index up to but not including 3

print(my_list[3:])  # items from index 3 on

print(my_list[-3:])  # items starting from 3 from right hand end to the right hand end



s = 'abcdefg'

print(s[0])

print(len(s))

print(s[len(s) - 1])

# s[len(s) - 1] = 'b'  # strings don't support item assignment because they are immutable

print(s[1:4])  # chars with index 1 to 3

print(s[:3])  # chars with index up to but not including 3

print(s[3:])  # chars from index 3 on

print(s[-3:])  # chars starting from 3 from right hand end to the right hand end


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


# Solution to challenge 7 using while loop

i = 0

while i < len(my_list):

    print(my_list[i])

    i += 1


# Solution to challenge 7 using for loop

for v in my_list:

    print(v)


# Solution to challenge 7 advanced

for i in range(0, len(my_list), 2):

    print(my_list[i])




# Challenge 8: What do the conditional operators mean: >, <, ==, !=, >=, <= (Advanced is)

# == is equal to

# != is not equal to

# >  is greater than

# <  is less than

# >= is greater than or equal to

# <= is less than or equal to

# is is identical to


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

while i < len(numbers):

    print(str(i) + " " + numbers[i])

    print(i, numbers[i])

    i += 1



# Challenge 11: Print out the names of all numbers up to 29 using the same list

i = 0

while i < 30:

    if i < len(numbers):

        print(i, numbers[i])

    else:

        print(i, numbers[20] + "-" + numbers[i-20])

    i += 1



# Advanced Challenge 12: What are the numbers between one and twenty-nine where

# the number of letters in the number is a factor of the number

# Should print out

# 4 four 4 FACTOR

# 6 six 3 FACTOR

# 12 twelve 6 FACTOR

i = 0

while i < 30:

    if i < len(numbers):

        number_name = numbers[i]

    else:

        number_name = numbers[20] + "-" + numbers[i-20]

    letters = len(number_name)

    print(i, number_name, letters, end=' ')

    if i % letters == 0:

        print("FACTOR")

    else:

        print()

    i += 1
