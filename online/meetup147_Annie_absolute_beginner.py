# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 14:18:22 2022

@author: nnguyen3

Beginner's Python & Machine Learning Support Session #147: absolute beginners

Youtube: https://youtu.be/R3Dkwv8ANXc
Github:  https://github.com/timcu/session-summaries/raw/master/online/meetup147_Annie_absolute_beginner.py
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/286826367/


"""

# S T R I N G S

s1 = 'my first string uses single quotes'

print(s1)

s2 = "my second string uses double quotes"

print(s2)

my_multiline = '''Strings can go over 
several lines \n
if they start and \n 
end with 3 single quotes'''

# notice the difference between putting \n and not in the console
print(my_multiline)


print("Hello World!")
# the print function simply prints words to the python console, which is useful for displaying results 
# you can print results without the variable being previously defined 

# check the class of an object
print(type(s1))

# to capitalise a string
print(s1.capitalize())

# all upper case
s3 = s2.upper()

print(s3)

# all lower case
s4 = s3.lower()

# len() used to check the length of an object 
print(len(s4))

# you can do operations on strings
print(s4 * 2)

# concatenating strings using +, I've added an empty space in a string using single quotes
print(s1+ " " + s3)

# variables
x = 'a variable is used to store data'

print(x)
# this is an example where I have used the print function to call on the variable x

''' 
x is a variable that I can call again later. 
x is something that is subject to changes
a string is a type of data (str). 
Other data types are floating point numbers (float) and integers (int).

variables must start with a letter or an underscore
names are case sensitive
str, int and float are immutable data types which means they cannot be changed.
A variable containing an immutable data type can replace its value with a new value

you can name your variable anything except the following keywords:
    
False   class 	    finally 	   is 	        return
None 	continue    for 	       lambda 	    try
True    def 	    from 	       nonlocal     while
and	    del 	    global         not 	        with
as 	    elif        if 	          or 	        yield
assert  	       else           import        pass 	 
break   	       except         in 	        raise
    
'''
    

# N U M B E R S 

# integer
a = -5
print (type(a))
# the variable a is an integer, it can be any positive or negative whole number, including 0


# float
pi = 3.147
print(type(pi))
# the variable pi is a float which is a number followed by a decimal
# you can do many mathematic operations on integers and floats 
# for instance +, -, *, /, //, ^

# will return a float
n1 = 10/3
print(n1)

# floor division will round the operation and return an integer with no remainder
n2 = 10//3
print(n2)

# modulo % will give remainder only
n3 = 10%3
print(n3)

# libraries are a group of functions/classes/modules that have been pre-defined and packaged together

#import math
# help(math)


# L I S T S 

# index   [  0,   1,   2,   3,   4,     5  ]
animals = ["dog", 3, "cat", 5, "hens", 12.7]

# animals is an example of a list
# a list can contain any class type, e.g., another list, a tuple, strings and numbers
# you can put a list inside another list

print(len(animals))  # returns the number of items in the list called animals

print(animals[2])  # returns the item at index i (in python the first item has index 0),

# animal[i:j] returns a new list, containing the objects between i and j.
# to get the full list of methods type help(list)

animals[1] = "bears"

print(animals)


# T U P L E S 

reds = "maroon", 4, "crimson", animals, "ochre",

type(reds)

# here we saved animals (a list) inside a tuple
print(reds[3])

rainbow = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')

# tuples can be defined using no brackets or round brackets () , lists use square brackets [], dictionaries use curly brackets {}
# tuples are like lists but tuples are immutable (cannot be changed after creation)
# tuples will have fewer functions e.g., pop(), drop(), and insert() which can be used to alter elements in a list 
# but won't work on a tuple
# benefits - retains its value regardless of functions applied

animals.append("rabbit")

print(animals)

# you can't change tuples
rainbow.append('pink')
# AttributeError: 'tuple' object has no attribute 'append'



# D I C T I O N A R I E S 

# structure of a dictionary

# d = {
#     <key>: <value>,
#     <key>: <value>,
#      .
#      .
#     <key>: <value>
# }

# for example Cities is an example of a dictionary

Cities = {
        'Australia':'Canberra',
        'Germany':'Berlin',
        'Spain':'Madrid'
}

type(Cities)
# Out[91]: dict

Cities['Australia'] = 'Brisbane'  # update existing entry

Cities['Antarctica'] = 'None'  # Adding new entry

print(Cities)

# dictionaries associate each key with a value, while a list, a tuple and a set just containing values
# a list keeps order, dict and set does not
# a set is an unordered collection of items. 
# Every element is unique (no duplicates) and must be immutable (cannot be changed). 
# However, the set itself is mutable.
# a list and dict may have duplicates and is mutable

# help(dict)

fruits = {"tomatoes", "pumpkins", "cherries", "peas"}

# a set, elements can't be replaced, only .add() and .remove()
type(fruits)

fruits.add("eggplants")

print(fruits)

# help(set)


# B O O L E A N

# True or False, using <, >, >=, <= , == 

print(10 <= 9)

print(s2.isnumeric())

# you can store a boolean in a variable
my_fact = 5 == len(fruits)

# this will print True
print(my_fact)

# bool
type(my_fact)


# I F   S T A T E M E N T S

# if statements use Boolean logic 
# if statements will only execute if the condition outputs to True. 
# don't forget to end each conditional statement with a colon : and indent the code below the conditional statement
# the elif statement allows you to check multiple expressions for TRUE and execute another block of code
# else and elif statements are optional. 
# you can have many elif but only one else at the end of your conditional if statement.    

# Structure of an if statement

# if item boolean operator condition:
#    execute this statement


coffee = 2

if coffee < 1:                    # true, keep going to the next condition
    print("need more caffeine!")
else:
    print("2 cups is enough!")



# F O R  L O O P S 

# Structure of a for loop

# for item in object:
#    execute this statement


planets = ["Earth", "Jupiter", "Mercury", "Uranus", "Pluto", "Venus", "Mars", "Neptune", "Saturn"]     

for p in planets:
    print(p)
    if p == "Venus":
        break
    
# for loops are for iterating through “iterables”. Iterables include lists, strings and dictionaries 
# for loops will go through each item in an iterable and execute the statement and move on to the next item until there are no more items; 
# hence for loops are perfect for processing repetitive programming tasks! 
# with the break statement we can stop the loop even if the statement is true
# in the above example I have specified the loop to break if the item is equvalent to the value "Venus"
# you can do many fantastic things with for loops as long as you understand the logic behind it
# you can use a for loop inside another for loop (a nested loop; more on that later)

# here is another for loop example

# dict , by default both keys and values will be strings
results = {'Annie':(44),
           'Tim':(97),
           'Arun':(82),
           'John':(32)
}


for v in results.values():    
    if v > 90:
        print('Well done! A+ for you!')
    elif v > 50:
        print('You passed the exam!')
    elif v > 40:
        print('Close, but no cigar!')
    else:
        print('Haha..you FAILED!')
    

# W H I L E   L O O P S

# while loops executes a piece of code while a condition is True. 
# the loop continues until the while statement evaluates to False.
# unlike a for loop, the while loop will not run n times, but until a defined condition is no longer met.
# if the condition is initially False, the while loop will not be executed at all.     
# example of a while loop is as follows

count = 10
while count > 0:
   print(count)
   count -= 1
print("Lift off!")

# note that in this example, the print("Lift off!") command is not part of the while loop as it is not indented

# you can use a while loop with an else statement
# The else statements are only executed if the loop concludes normally. They are not executed if the loop was
# aborted with a break or exception. It is fairly rare to use else with a while loop.

count = 0
while count < 5:
   print(count, " is less than 5")
   count = count + 1
else:
   print(count, " is not less than 5") 
   

# we can use break, continue and pass in for loops and while statements 

# with the continue statement we can stop the current iteration, and continue with the next
# the difference in using the continue statement rather than a break statement is that our code will continue to the next iteration 
# despite the disruption when the loop encounters a trigger. 
# when an external condition is triggered, the pass statement allows you to handle the condition without the loop being impacted in any way; 
# all of the code will continue to be read unless a break or other statement occurs. 

# the pass statement is a null operation; nothing happens when it executes. 
# the pass is useful in places where your code will eventually go, but has not been written yet 
# or it is helpful when you have created a code block but it is no longer required. 

# example of continue in while loop

number = 0

while number in range(10):
   number = number + 1
   if number == 5:
      continue    # pass here, note 5 is not operated on
   print('Number is ' + str(number))
