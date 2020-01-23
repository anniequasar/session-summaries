#!/usr/bin/env python3
# coding=utf-8
"""
MeetUp 043 - Beginners Python Support Sessions - Thu 23 Jan 2020 - Functions

Learning objectives:
    Functions: plotting, first class objects, recursive, logging, testing

@author D Tim Cummings

Challenge 1: Define the following functions and plot using matplotlib from x = 0 to 2 in 20 steps
    quadratic(x) = 1 - (x-1)²
    cubic(x) = x(x-1)(x-2).
    zero(x) which always returns zero regardless of the value of x
    line(x) which is the equation of a straight line with slope of 1 going through (0, 0)
    sine_wave(x) which is a sine wave with amplitude 1 (maximum value) and period 4 (completes one cycle when x=4)

Hint to plot this data using matplotlib
    import matplotlib.pyplot as plt
    plt.plot(x, y, label=f.__name__, marker='x')
    plt.legend()
    plt.show()

Challenge 2: Challenge: Find the perfect match between the functions
    Put all five functions in a list.
    Loop through all possible permutations of 2 functions from 5.
    Find the best match at points x = 0, x = 1, x = 2 by summing
    the squares of the differences of the function values at the
    two points.
    Repeat the exercise at 21 points of x between 0 and 2.0

Challenge 3: Write a function which takes the unit price, and the quantity and returns the extended price
    assert extended_price(unit_price=3.00, quantity=5) == 15.00
    assert extended_price(unit_price=2.50, quantity=-2) == -5.00
    assert extended_price(unit_price=1.10, quantity=3) == 3.30
    Use debug logging to determine what problem might be

Challenge 4: Write a recursive function to print the name of any number up to one quadrillion
names_sub_20 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
names_tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
              60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
assert str_number_name(323123) == "three hundred and twenty-three thousand one hundred and twenty-three"

Challenge 5: Write a function which accepts an int between 0 and 1 quadrillion and returns it's name using dict of powers
names_powers = {100: 'hundred', 1000: 'thousand', 1000000: 'million', 1000000000: 'billion', 1000000000000: 'trillion',
                1000000000000000: 'quadrillion', 1000000000000000000: 'Too big'}

"""
import matplotlib.pyplot as plt
import math
import logging
from datetime import datetime, time, timedelta

# Logging level can be critical, error, warning, info, debug,
logging.getLogger().setLevel(logging.INFO)
# logging.basicConfig(filename='meetup043.log', format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)


# Challenge 1: Define the following functions and plot using matplotlib from x = 0 to 2 in 20 steps
#     quadratic(x) = 1 - (x-1)²
#     cubic(x) = x(x-1)(x-2).
#     zero(x) which always returns zero regardless of the value of x
#     line(x) which is the equation of a straight line with slope of 1 going through (0, 0)
#     sine_wave(x) which is a sine wave with amplitude 1 (maximum value) and period 4 (completes one cycle when x=4)
#
# Hint to plot this data using matplotlib
#     import matplotlib.pyplot as plt
#     plt.plot(x, y, label=f.__name__, marker='x')
#     plt.legend()
#     plt.show()
def quadratic(x):
    return 1 - (x - 1) ** 2


def cubic(x):
    return (x-1) * (x-2) * x


def zero(x):
    return 0


def line(x):
    return x


def sine_wave(x):
    return math.sin(x * math.pi / 2)


# lst_x = [0, 1, 2]
lst_x = [i / 10 for i in range(21)]
tpl_functions = (quadratic, zero, cubic, sine_wave, line)
for f in tpl_functions:
    lst_y = [f(x) for x in lst_x]
    plt.plot(lst_x, lst_y, label=f.__name__, marker='x')
plt.legend()
plt.show()


# Challenge 2: Challenge: Find the "perfect match" between the functions
#     Put all five functions in a list.
#     Loop through all possible permutations of 2 functions from 5.
#     Find the best match at points x = 0, x = 1, x = 2 by summing
#     the squares of the differences of the function values at the
#     two points.
#     Repeat the exercise at 21 points of x between 0 and 2.0
lst_pairs = []
min_ss = None
for a in range(len(tpl_functions) - 1):
    fa = tpl_functions[a]
    for b in range(a + 1, len(tpl_functions)):
        fb = tpl_functions[b]
        ss = sum((fa(x) - fb(x)) ** 2 for x in lst_x)
        print(f"Challenge 2: Pair {fa.__name__}, {fb.__name__} had a sum of squares of {ss}")
        if min_ss is None or min_ss > ss:
            lst_pairs = [(fa, fb)]
            min_ss = ss
        elif min_ss == ss:
            lst_pairs.append((fa, fb))
for pair in lst_pairs:
    print(f"Challenge 2: Closest match pair {pair[0].__name__}, {pair[1].__name__} had a sum of squares of {min_ss}")


# Challenge 3: Write a function which takes the unit price, and the quantity and returns the extended price
# assert extended_price(unit_price=3.00, quantity=5) == 15.00
# assert extended_price(unit_price=2.50, quantity=-2) == -5.00
# assert extended_price(unit_price=1.10, quantity=3) == 3.30
def extended_price(unit_price, quantity=1):
    """Calculates extended price given unit price and quantity. Quantity defaults to 1"""
    # return unit_price * quantity  # doesn't work because of binary representation of floating point numbers
    # could use decimal library, or return extended price in cents (unit price could be fraction of a cent)
    # return (decimal.Decimal(unit_price) * quantity).quantize(decimal.Decimal("0.01"), decimal.ROUND_HALF_UP)
    # ep = unit_price * quantity
    ep = round(unit_price * quantity, 2)
    logging.debug(f"extended_price(): unit_price {unit_price} quantity {quantity} extended_price {ep}")
    return ep


assert extended_price(unit_price=3.00, quantity=5) == 15.00
assert extended_price(unit_price=2.50, quantity=-2) == -5.00
assert extended_price(unit_price=1.10, quantity=3) == 3.30


# When calling a function you can supply parameters by expanding a list of the parameters
my_list = [12.345, 3.5]
assert extended_price(*my_list) == 43.21
# When calling a function you can supply parameters by expanding a tuple of the parameters
my_tuple = (32.42, 7)
assert extended_price(*my_tuple) == 226.94
# When calling a function you can supply parameters by expanding a dict of the named parameters
my_dict = {'quantity': 1/3, 'unit_price': 6.0}
assert extended_price(**my_dict) == 2.00


# When defining a function you can capture arguments into a list
def read_arguments_as_list(*args):
    for i in range(len(args)):
        print(f"Argument {i} is {args[i]}")


# When defining a function you can capture keyword arguments into a dictionary
def read_keyword_arguments(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}={v}")


# Challenge 4: Write a recursive function to print the name of any number up to one million
names_sub_20 = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty")
names_tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
              60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}


def str_number_name_999(num):
    if num < len(names_sub_20):
        return names_sub_20[num]
    elif num < 100:
        units = num % 10
        tens = num - units
        if units == 0:
            return names_tens[tens]
        else:
            return names_tens[tens] + "-" + names_sub_20[units]
    elif num < 1000:
        name = str_number_name_999(num // 100) + " hundred"
        if num % 100 == 0:
            return name
        else:
            return name + " and " + str_number_name_999(num % 100)
    elif num < 1000000:
        name = str_number_name_999(num // 1000) + " thousand"
        if num % 1000 == 0:
            return name
        elif num % 1000 < 100:
            return name + " and " + str_number_name_999(num % 1000)
        else:
            return name + " " + str_number_name_999(num % 1000)
    else:
        return "Too big"


assert str_number_name_999(37) == "thirty-seven"
assert str_number_name_999(50) == "fifty"
assert str_number_name_999(323123) == "three hundred and twenty-three thousand one hundred and twenty-three"
for n in (323, 323123, 323023, 323023001, 20503015012, 1000000000000000):
    print("str_number_name_999({:,}) is {}".format(n, str_number_name_999(n)))

# Challenge 5: Write a function which accepts an int between 0 and 1 quadrillion and returns it's name
names_powers = {100: 'hundred', 1000: 'thousand', 1000000: 'million', 1000000000: 'billion', 1000000000000: 'trillion',
                1000000000000000: 'quadrillion', 1000000000000000000: 'Too big'}


def str_number_name(num):
    lst_powers = sorted(names_powers.keys())
    if num < len(names_sub_20):
        return names_sub_20[num]
    elif num < 100:
        units = num % 10
        tens = num - units
        if units == 0:
            return names_tens[tens]
        else:
            return names_tens[tens] + "-" + names_sub_20[units]
    else:
        idx = 0
        while idx < len(lst_powers) - 1:
            if num < lst_powers[idx + 1]:
                power = lst_powers[idx]
                name = str_number_name(num // power) + " " + names_powers[power]
                if num % power == 0:
                    return name
                elif num % power < 100:
                    return name + " and " + str_number_name(num % power)
                else:
                    return name + " " + str_number_name(num % power)
            idx += 1
    return "Too big"


assert str_number_name(37) == "thirty-seven"
assert str_number_name(50) == "fifty"
assert str_number_name(323123) == "three hundred and twenty-three thousand one hundred and twenty-three"
for n in (323, 12323123323023, 323023001, 20503015012, 1000000000000000):
    print(f"str_number_name({n:,}) is {str_number_name(n)}")
