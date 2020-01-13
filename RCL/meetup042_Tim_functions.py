#!/usr/bin/env python3
# coding=utf-8
"""
MeetUp 042 - Beginners Python Support Sessions - Wed 15 Jan 2020 - Functions

Learning objectives:
    Functions:

@author D Tim Cummings

Challenge 1: Write a function which shows how much time is left in this session
Hint: datetime.combine(dt1, dt2) combines date from dt1 with time from dt2
Hint: Time 8pm  time(hour=20)

Challenge 2: Write a function which returns a datetime object for the same time as now but tomorrow
Hint: timedelta(days=1)

Challenge 3: Write a function which returns the time in seconds as a str in minutes and seconds
Example str_min_sec(80) -> "1:20"
Example str_min_sec(40) -> "0:40"
Example str_min_sec(4201) -> "70:01"
Example str_min_sec(-80) -> "-1:20"
Example str_min_sec(-40) -> "-0:40"

Challenge 4: Write a function which returns a sign (±1), minutes and seconds given the seconds

Challenge 5: Write a function which takes the unit price, and the quantity and returns the extended price
assert extended_price(unit_price=3.00, quantity=5) == 15.00
assert extended_price(unit_price=2.50, quantity=-2) == -5.00
assert extended_price(unit_price=1.10, quantity=3) == 3.30

Challenge 6: Create a function quadratic(x) = 1 - (x-1)²

Challenge 7: Create a function cubic(x) = x(x-1)(x-2).

Challenge 8: Print a table of v, quadratic(v) and cubic(v) with value v going from 0 to 2 in 0.1 steps

Challenge 9: Create functions:
    zero(x) which always returns zero regardless of the value of x
    line(x) which is the equation of a straight line with slope of 1 going through (0, 0)
    sine_wave(x) which is a sine wave with amplitude 1 (maximum value) and period 4 (completes one cycle when x=4)

Challenge 10: Plot this data using matplotlib
    import matplotlib.pyplot as plt
    plt.plot(x, y, label=f.__name__, marker='x')
    plt.legend()
    plt.show()

"""
import matplotlib.pyplot as plt
import math

from datetime import datetime, time, timedelta


# functions are used so you don't have to repeat yourself when programming. DRY = don't repeat yourself
# A function is defined using def <function_name>():
def show_now():
    time_now = datetime.now().time()  # module datetime, function now() in module
    print(f"The time is now {time_now}")


# To call a function use the function's name followed by parentheses
show_now()
show_now()

# By convention, function names, like variable names should be lower case with words separated by underscores
# By convention, class names are CapWord, constants are UPPER_CASE
# Choose a consistent naming scheme
# Example naming scheme, if a function performs an action, start the function name with that action


# Challenge 1: Write a function which shows how much time is left in this session
# Hint: datetime.combine(dt1, dt2) combines date from dt1 with time from dt2
# Hint: Time 8pm  time(hour=20)
def show_time_left():
    time_finish = datetime.combine(datetime.today(), time(hour=20))
    time_now = datetime.now()
    print(f"Challenge 1: Time left in the session is {time_finish - time_now} (hh:mm:ss.ssssss)")


show_time_left()

# A function can return a value to where it is called using the return statement
# A function can have several return lines. Nothing after the first return reached will be executed
# If a function returns a value I like to include the return type in the function name (useful in group projects)


def td_time_left():
    """Calculate time from now until 8pm tonight and return it as a datetime.timedelta"""
    time_finish = datetime.combine(datetime.today(), time(hour=20))
    time_now = datetime.now()
    time_delta = time_finish - time_now
    return time_delta


t = td_time_left()
print(f"Time left in session is {t} (hh:mm:ss.ssssss)")

# A function's name is a variable name
# To assign to a new variable use function name without parentheses
time_left = td_time_left
print(f"Time left in session is {time_left()} (hh:mm:ss.ssssss)")
# You can find the name a function was originally defined as using .__name__
print(f"Function time_left was originally defined using name {time_left.__name__}")


# Challenge 2: Write a function which returns a datetime object for the same time as now but tomorrow
# Hint: timedelta(days=1)
def dt_same_time_tomorrow():
    """Returns the date and time one day after this function is called

    The return result is a datetime.datetime object"""
    time_today = datetime.now()
    one_day = timedelta(days=1)
    time_tomorrow = time_today + one_day
    return time_tomorrow


print(f"Challenge 2: Same time tomorrow is {dt_same_time_tomorrow()}")
help(dt_same_time_tomorrow)


# A function can take one or more arguments also known as parameters
def flt_f_from_c(c):
    """Returns the temperature in Fahrenheit given the temperature in Celsius"""
    return c * 1.8 + 32


print("Temperature {:7.2f}°C is equivalent to {:7.2f}°F".format(0, flt_f_from_c(0)))
print("Temperature {:7.2f}°C is equivalent to {:7.2f}°F".format(100, flt_f_from_c(100)))
print("Temperature {:7.2f}°C is equivalent to {:7.2f}°F".format(-40, flt_f_from_c(-40)))
# ° = opt-shift-8 on Mac = alt0176 on Windows


# Challenge 3: Write a function which returns the time in seconds as a str in minutes and seconds
# Example str_min_sec(80) -> "1:20"
# Example str_min_sec(40) -> "0:40"
# Example str_min_sec(4201) -> "70:01"
# Example str_min_sec(-80) -> "-1:20"
# Example str_min_sec(-40) -> "-0:40"
def str_min_sec(time_in_seconds):
    """Converts seconds into minutes and seconds and returns result as a str

    Example: str_min_sec(-40) returns '-0:40'"""
    sgn = ''
    if time_in_seconds < 0:
        sgn = '-'
        time_in_seconds = -time_in_seconds
    return f"{sgn}{time_in_seconds//60}:{time_in_seconds%60:0>2}"


for t in (40, 80, 4201, -80, -40):
    print(f"Challenge 3: Time {t:>5d} seconds is equivalent to min:sec {str_min_sec(t):>6s}")


# Functions can return more than one value by separating with commas
# Equivalent to returning a tuple with the values in it
# Challenge 4: Write a function which returns a sign (±1), minutes and seconds given the seconds
def tpl_min_sec(time_in_seconds):
    """Converts seconds into minutes and seconds and returns result as a tuple

    Example: tpl_min_sec(-140) returns (-1, 2, 20)"""
    sgn = 1
    if time_in_seconds < 0:
        sgn = -1
        time_in_seconds = -time_in_seconds
    return sgn, time_in_seconds // 60, time_in_seconds % 60


sign, minutes, seconds = tpl_min_sec(-40)
print(f"Challenge 4: -40 seconds is equivalent to sign={sign}, minutes={minutes}, seconds={seconds}")
t = tpl_min_sec(375)
print(f"tpl_min_sec(375): repr={repr(t)}, type={type(t)}")
t = "my string"
print(f"'my string': repr={repr(t)}, type={type(t)}")

# How to write tests to check your function
assert tpl_min_sec(40) == (1, 0, 40)
assert tpl_min_sec(80) == (1, 1, 20)
assert tpl_min_sec(3601) == (1, 60, 1)
assert tpl_min_sec(-80) == (-1, 1, 20)
assert tpl_min_sec(-40) == (-1, 0, 40)


# Challenge 5: Write a function which takes the unit price, and the quantity and returns the extended price
# assert extended_price(unit_price=3.00, quantity=5) == 15.00
# assert extended_price(unit_price=2.50, quantity=-2) == -5.00
# assert extended_price(unit_price=1.10, quantity=3) == 3.30
def extended_price(unit_price, quantity=1):
    """Calculates extended price given unit price and quantity. Quantity defaults to 1"""
    # return unit_price * quantity  # doesn't work because of binary representation of floating point numbers
    # could use decimal library, or return extended price in cents (unit price could be fraction of a cent)
    # return (decimal.Decimal(unit_price) * quantity).quantize(decimal.Decimal("0.01"), decimal.ROUND_HALF_UP)
    return round(unit_price * quantity, 2)


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


# Challenge 6: Create a function quadratic(x) = 1 - (x-1)²
def quadratic(x):
    return 1 - (x - 1) ** 2


# Challenge 7: Create a function cubic(x) = x(x-1)(x-2).
def cubic(x):
    return (x-1) * (x-2) * x


# Challenge 8: Print a table of v, quadratic(v) and cubic(v) with value v going from 0 to 2 in 0.1 steps
print(f"Challenge 8:     v  quadratic   cubic")
for i in range(21):
    v = i / 10
    print(f"Challenge 8:   {v:>3.1f}  {quadratic(v):9.3f}  {cubic(v):6.3f}")


# Challenge 9: Create functions zero(x), line(x), sine_wave(x):
def zero(x):
    return 0


def line(x):
    return x


def sine_wave(x):
    return math.sin(x * math.pi / 2)


# Challenge 10: Plot this data using matplotlib
lst_x = [i/10 for i in range(21)]
for f in [quadratic, zero, cubic, sine_wave, line]:
    lst_y = [f(x) for x in lst_x]
    plt.plot(lst_x, lst_y, label=f.__name__, marker='x')
plt.legend()
plt.show()
