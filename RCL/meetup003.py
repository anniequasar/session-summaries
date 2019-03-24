"""
MeetUp 003 - Beginners Python Support Sessions 20-Mar-2019

Learning objectives:
    Data types: tuple, 2D list
    Built-in functions: str() int() float() tuple() input()
    Structure: try except

@author D Tim Cummings

Challenge 1: Use input() to ask someone their name and then say hello to them.

Challenge 2: Use input() and int() to ask for the amount of change in last week's Challenge 2.
Advanced: Catch the exception if user enters a number which is not an integer

Challenge 3: Specify length of side (eg side = 4) and then store a square of that size in a 2D list.
 Check program still works when side = 10
[['S', 'S', 'S', 'S'],
 ['S', ' ', ' ', 'S'],
 ['S', ' ', ' ', 'S'],
 ['S', 'S', 'S', 'S']]
Advanced: Add a diagonal to shape in 2D list and print out contents of array where lst[0][0] is in lower left corner
S S S /
S   / S
S /   S
/ S S S

Challenge 4: Repeat challenge 7 using a dict rather than a 2D list. Key for dict will be tuples with x,y coordinates.
{(0, 0): 'S', (3, 0): 'S', (0, 3): 'S', (3, 3): 'S',
 (0, 1): 'S', (3, 1): 'S', (1, 0): 'S', (1, 3): 'S',
 (0, 2): 'S', (3, 2): 'S', (2, 0): 'S', (2, 3): 'S'}

Challenge 5: Read csv file containing three columns of data
    'race' = the date of the race
    'runner' = the name of the runner running in the race
    'time' = the time in seconds the runner took to run 5 km.
    Find each runners fastest time
    Find the winner of each race
Advanced:
    If more than one winner of a race show all of the winners for that race
    Check first row to see which column is which
    Find the race each runner had their fastest time
    Show places for each runner in each race

# DICTS REVIEW

results = {'Annie': 1350, 'Ben': 1425, 'Cameron': 1325, 'Des': 1375, 'Ellen': 1325}
fastest_time = min(results.values())
for runner, time in results.items():
    if fastest_time == time:
        print('Fastest runner is {} with a time of {}'.format(runner, fastest_time))

results.keys() : list of keys
results.values() : list of values
results.items() : dict items iterable set of key value pairs

# Example: store the names of American coins in a dict
coin = {1: 'penny', 5: 'nickel', 10: 'dime', 25: 'quarter'}
coin = {1: 'cent', 2: 'two cent', 5: 'sixpence', 10: 'shilling', 20: 'florin', 50: 'crown' }

# Create an empty dict
my_dict = {}  # or my_dict = dict()
# Add new value to the dict or update existing value
my_dict[100] = "dollar"
# key must be unique can be any immutable (hashable) value (str, int, float, etc. Not list or dict)
postcode['Indooroopilly'] = 4068
# Remove from the dict
del my_dict["key"]
# Update values in one dict with values from another dict (equivalent to concatenation if no keys the same)
my_dict.update(other_dict)
# Test if dict has a key
25 in coin  # True
50 in coin  # False
# Loop through all keys in dict
for amount in coin:
for amount in coin.keys():
for name in coin.values():
for amount, name in coin.items():
sorted(coin, reverse=True)  # [25, 10, 5, 1]  sorted returns list of keys

# TUPLES

# Can't use list as key for dict. Can use a tuple because tuples are immutable

# Rule of thumb for lists or tuples: Use tuples unless you need mutability

# Create an empty tuple
my_tuple = ()  # or my_tuple = tuple()
# Add a new value
my_tuple += (1,)  # have to add comma for single element tuple
# Delete a tuple
del my_tuple
# Assign variables based on contents of tuple
a, b, c = (1, 2, 3)
a, b, c = 1, 2, 3
d = 4, 3, 2  # equivalent to d = (4, 3, 2)
# Loop through all values in tuple
for v in my_tuple:

# Get user input from keyboard - input()

# Conversion between data types
str() int() float() list() tuple() dict()


"""

# Challenge 1: Use input() to ask someone their name and then say hello to them.
#

name = input("What is your name? ")
print("Hello", name)

# Challenge 2: Use input() and int() to ask for the amount of change in last week's Challenge 2.
# Advanced: Catch the exception if user enters a number which is not an integer
#
coin_us = {1: 'penny', 5: 'nickel', 10: 'dime', 25: 'quarter'}
coin_au = {1: 'cent', 2: 'two cent', 5: 'sixpence', 10: 'shilling', 20: 'florin', 50: 'crown' }
coin = coin_au
coin_values = sorted(coin, reverse=True)

change = None
while change is None:
    try:
        change = int(input("Enter amount of change? "))
    except ValueError:
        print("Please enter an integer.")
for coin_value in coin_values:
    count, change = divmod(change, coin_value)
    if count > 0:
        print("{:<8s} x {:>2d} = {:0>4d}".format(coin[coin_value], count, coin_value * count))


# Challenge 3: Specify length of side (eg side = 4) and then store a square of that size in a 2D list.
#  Check program still works when side = 10
# [['S', 'S', 'S', 'S'],
#  ['S', ' ', ' ', 'S'],
#  ['S', ' ', ' ', 'S'],
#  ['S', 'S', 'S', 'S']]
# Advanced: Add a diagonal to shape in 2D list and print out contents of array where lst[0][0] is in lower left corner
# S S S /
# S   / S
# S /   S
# / S S S
side = 10
shape = []
for i in range(side):
    row = [' '] * side
    shape.append(row)
for i in range(side):
    shape[0][i] = shape[i][0] = shape[-1][i] = shape[i][-1] = 'S'
for i in range(side):
    shape[i][i] = '/'
for j in range(side):
    y = side - j - 1
    for i in range(side):
        x = i
        print(shape[x][y], end=' ')
    print()

# Challenge 4: Repeat challenge 3 using a dict rather than a 2D list.
# Key for dict will be tuples with x,y coordinates.
# {(0, 0): 'S', (3, 0): 'S', (0, 3): 'S', (3, 3): 'S',
#  (0, 1): 'S', (3, 1): 'S', (1, 0): 'S', (1, 3): 'S',
#  (0, 2): 'S', (3, 2): 'S', (2, 0): 'S', (2, 3): 'S'}
shape = {}
side = 7
for i in range(side):
    for n in range(side):
        if i == n:
            shape[(i, n)] = '/'
        elif i == 0 or i == side - 1 or n == 0 or n == side - 1:
            shape[(i, n)] = 'S'
for j in range(side):
    y = side - j - 1
    for i in range(side):
        x = i
        if (x, y) in shape:
            print(shape[(x, y)], end=' ')
        else:
            print(' ', end = " ")
    print()
