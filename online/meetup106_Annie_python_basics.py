"""
Created on Fri Apr 30 10:38:52 2021

@author: nnguyen

BPSS Meetup 106
"""


# python is a high-level object-oriented programming language 
# python is used in many applications including Google search engine, instagram, spotify & netflix algorithms, 
# NASA's software and hardware is programmed using python

# intro to the IDE interface



# D A T A   T Y P E S 

# S T R I N G S

# These are examples of strings
s1 = 'my first string uses single quotes'
s2 = "my second string uses double quotes"

print(s1)
print(s2)

'''Strings can go over several lines 
if they start and end with 3 single quotes'''

"""Similarly multiline strings 
        with new lines and tabs can
            start and end with 3 double quotes"""

# If you place a string literal as the first statement in a module, function, class
# or method definition then it becomes a docstring (Documentation string) and is accessible at runtime. 
# Docstrings are used to describe what a module/class/function does. 

# Some people use strings as multiline comments but it is safer to use multiple
# single line comments. For example, the following creates an empty dict

my_dict1 = {
	# I want my_dict to be an empty dict for now.
	# When I know what to put in it I will put it here
} 

# The following example uses multiline strings to achieve the same but instead creates
# a set containing the string

my_dict2 = {
	"""
	I want my_dict to be an empty dict for now.
	When I know what to put in it I will put it here
	"""
}
print(my_dict1)
print(my_dict2)

print("Hello World!")
# the print function simply prints words to the python console, which is useful for displaying results 
# you can print results without the variable being previously defined 

print(('Hello ' * 3) + 'World')
# you can concatenate strings together by using the + symbol.
# note that I had to add in the white space between words manually

x = 'I am a string with 11 words, how long are you?'

''' 
x is a variable that I can call again later. x is something that is subject to changes
a string is a type of data (str). 
Other data types are floating point numbers (float) and integers (int).

You can do many things with strings such as len() which gives you the length of the string

.upper() and .lower() which return a new string with all characters in lower or upper case 

you can get the string equivalent of integers and floats using the function str(), int(), float()

variables must start with a letter or an underscore
names are case sensitive
str, int and float are immutable data types which means they cannot be changed.
A variable containing an immutable data type can replace its value with a new value

you can name your variable anything except the following keywords:
    
False   class 	    finally 	   is 	        return
None 	  continue    for 	       lambda 	    try
True 	  def 	      from 	       nonlocal 	  while
and 	  del 	      global       not 	        with
as 	    elif 	      if 	         or 	        yield
assert 	else 	      import       pass 	 
break 	except 	    in 	         raise
    
'''
    
print(x)
# this is an example where I have used the print function to call on the variable x



# N U M B E R S 

a = -5
print (type(a))
# the variable a is an integer, it can be any positive or negative whole number, including 0

pi = 3.147
print(type(pi))
# the variable pi is a float which is a number followed by a decimal
# you can do many mathematic operations on integers and floats 
# for instance +, -, *, /, //, ^

# libraries are a group of functions/classes/modules that have been pre-defined and packaged together

import math

help(math)




# L I S T S 

animals = ["dog", 3, "cat", 5, "hens", 12.7]

# animals is an example of a list
# a list can contain any class type, e.g., another list, a tuple, strings and numbers
print(len(animals))  # returns the number of items in the list called animals

print(animals[2])  # returns the item at index i (the first item has index 0),

# animal[i:j] returns a new list, containing the objects between i and j.
# to get the full list of methods type help(list)


# T U P L E S 

reds = "maroon", "crimson", "ochre"

rainbow = ('red', 'yellow', 'green', 'blue')

# tuples can be defined using no brackets or round brackets () , lists use square brackets [], dictionaries use curly brackets {}
# tuples are like lists but tuples are immutable (cannot be changed after creation)
# hence it will have fewer functions e.g., pop(), drop() and insert() which can be used to alter elements in a list but won't work on a tuple
# benefits - retains its value regardless of functions applied


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

cities = {
        'Australia':'Canberra',
        'Germany':'Berlin',
        'Spain':'Madrid'
}

cities['Australia'] = 'Brisbane'  # update existing entry

cities['Antarctica'] = 'None'  # Adding new entry

# dictionaries associate each key with a value, while a list, a tuple and a set just contain values
# a list keeps order, dict and set don't
# a set is an unordered collection of items. Every element is unique (no duplicates) and must be immutable (cannot be changed). However, the set itself is mutable.
# a list and dict may have duplicates and is mutable
# to get the full list of functions and methods type help(dict)



# if statements 

# if statements use Boolean logic 
# analyzing problems that breaks them down into questions answerable by True or False
# if statements will only execute if the condition outputs to True. 
# don't forget to end each conditional statement with a colon : and indent the code below the conditional statement
# the elif statement allows you to check multiple expressions for TRUE and execute a block of code as soon as one of the conditions evaluates to TRUE.
# else and elif statements are optional. However, there can be at most one else statement; and an arbitrary number of elif statements following an if.    
  
score = 87

if score > 90:
    print('Well done! A+ for you!')
elif score > 50:
    print('You passed the exam!')
elif score > 40:
    print('Close, but no cigar!')
else:
    print('Haha..you FAILED!')




    
# for loops 

# Structure of for loops

# for item in list:
#    execute this statement

    
planets = ["Earth", "Jupiter", "Mercury", "Uranus", "Pluto", "Venus", "Mars", "Neptune", "Saturn"]     

for p in planets:
    print(p)
    if p == "Venus":
        break
    
# for loops are for iterating through “iterables”. Iterables include lists, strings and dictionaries 
# for loops will go through each item in an iterable and execute the statement and move on to the next item until there is no more next item; hence for loops are perfect for processing repetitive programming tasks! 
# with the break statement we can stop the loop even if the statement is true
# in the above example I have specified the loop to break if the item is equvalent to the value "Venus"
# you can do many fantastic things with for loops as long as you understand the logic behind it
# you can use a for loop inside another for loop (a nested loop; more on that later)
# here is another for loop example

word = "pyramid"

x = 0

for letter in word:
    x = x + 1
    print(letter, word[0:x])

for letter in word:
    x = x - 1
    print(letter, word[0:x])

# what do you think the result is?


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

# you can use a while loop with an else statement, example as follows. The else statements
# are only executed if the loop concludes normally. They are not executed if the loop was
# aborted with a break or exception. It is fairly rare to use else with a while loop.

count = 0
while count < 5:
   print(count, " is less than 5")
   count = count + 1
else:
   print(count, " is not less than 5") 
   

# we can use break, continue and pass in for and while statements 
# with the continue statement we can stop the current iteration, and continue with the next
# the difference in using the continue statement rather than a break statement is that our code will continue to the next iteration despite the disruption when the loop encounters a trigger. 
# when an external condition is triggered, the pass statement allows you to handle the condition without the loop being impacted in any way; all of the code will continue to be read unless a break or other statement occurs. 
# the pass statement is a null operation; nothing happens when it executes. 
# the pass is useful in places where your code will eventually go, but has not been 
# written yet or it is helpful when you have created a code block but it is no longer 
# required. You need to put something in a code block to manage the indentation. 
# Indentation of comments is ignored so the pass command has to be used.
# example of continue in while loop
   
number = 0

while number in range(10):
   number = number + 1

   if number == 5:
      continue    # pass here

   print('Number is ' + str(number))

print('Loop complete!')
