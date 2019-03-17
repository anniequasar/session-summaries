"""
MeetUp 002 - Beginners Python Support Sessions

Learning objectives:
    Data types: bool, dict
    Built-in functions: sorted() list() dict() str.format()
    IDE: Virtual environment, requirements.txt

@author D Tim Cummings

# Review
int, float, str, list
variables (naming anything but keywords. Be careful you don't accidentally override built in functions.)
assignment and other operators, = + - / // % * ** += -= /= *= //= %=
Comparison operators return bool == != < <= >=

# Python keywords - https://docs.python.org/3/reference/lexical_analysis.html#keywords

# Python indexing - think of indexes as being between the elements

 a b c d e f g     # characters in string
0 1 2 3 4 5 6 7    # indexes of characters in string

# Virtual environment
PyCharm Win:
    File > Settings > Project > Project Interpreter > Project Interpreter > Show all
    + > Virtualenv Environment > New environment
PyCharm Mac: PyCharm > Preferences > ...
Create a file called requirements.txt in project with contents like
beautifulsoup4
Then Install requirement when asked.

# LISTS

# Create an empty list
my_list = []  # or my_list = list()
# Add to the list
my_list.append("another value")
# Remove from the list
del my_list[4]
# Update value in list
my_list[3] = 4
# Concatenate lists
[1, 2, 2] + [3, 3, 3]  # [1, 2, 2, 3, 3, 3]
[2, 1] * 3  # [2, 1, 2, 1, 2, 1]
# sort a list
sorted(my_list)
sorted(my_list, reverse=True)

# The problem with lists is you have no control over the index values. They are the position in the list
# If you don't need a value for every position you would have to enter dummy values for the other positions.

# DICTS

# Better way: use a dict (short for dictionary)

# Example: store the names of American coins in a dict
coin = {1: 'penny', 5: 'nickel', 10: 'dime', 25: 'quarter'}
coin[100] = 'dollar'
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

"""

# Challenge 1: Print out the names of all numbers up to 99 using the original list and a dict

names_sub_20 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
names_tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
              60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
i = 0
while i < 100:
    if i < len(names_sub_20):
        print(i, names_sub_20[i])
    else:
        units = i % 10
        tens = i - units
        if units == 0:
            print(i, names_tens[tens])
        else:
            print(i, names_tens[tens] + "-" + names_sub_20[units])
    i += 1


# Challenge 2: Store a cent value in a variable (eg change = 73) and then work out what coin names are required to make
# up that value. eg quarter x 2 + dime x 2 + penny x 3
#
# Challenge 4: Repeat challenge 2 with string formats so that all the numbers line up.


coin_us = {1: 'penny', 5: 'nickel', 10: 'dime', 25: 'quarter'}
coin_au = {1: 'cent', 2: 'two cent', 5: 'sixpence', 10: 'shilling', 20: 'florin', 50: 'crown' }
coin = coin_au
coin_values = sorted(coin, reverse=True)

change = 74
for coin_value in coin_values:
    count = change // coin_value
    change = change % coin_value
    # count, change = divmod(change, value)
    if count > 0:
        print("{:<8s} x {:>2d} = {:>4d}".format(coin[coin_value], count, coin_value * count))


# Challenge 3: Create a dict storing times for 5 runners in a race (key = runners name, value = time in seconds).
# Search through the data to find the fastest runner.
# Advanced: If more than one runner has the fastest time show all the runners with the fastest time.
results = {'Annie': 1350, 'Ben': 1425, 'Cameron': 1325, 'Des': 1375, 'Ellen': 1325}
fastest_time = None
for runner, time in results.items():
    if fastest_time is None or fastest_time > time:
        fastest_time = time
        fastest_runner = runner
        fastest_runners = [runner]      # advanced
    elif fastest_time == time:          # advanced
        fastest_runners.append(runner)  # advanced
print('Fastest runner is', fastest_runner, 'with a time of', fastest_time)
print('Fastest runners are', fastest_runners, 'with a time of', fastest_time)  # advanced
