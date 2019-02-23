"""
Functions - Beginners Python Session 7

@author: Tim Cummings

Functions can be a way of storing commonly used actions or returning results of common calculations.

In programming there is a principal DRY = Don't Repeat Yourself

If you are doing the same code more than once, put it in a function (or loop)
"""

#import datetime
from datetime import datetime, time, timedelta

# A function is defined using def
def show_now():
    time_now = datetime.now().time() # module datetime, function now() in module
    print("The time is now", time_now)


# To call a function use the function's name followed by parentheses
show_now()
show_now()

# Choose a consistent naming scheme
# By convention, function names should be lower case with words separated by underscores
# Example naming scheme, if a function performs an action, start the function name with that action

# Challenge: Write a function which shows how much time is left in this session
# Hint: datetime.combine(dt1, dt2) combines date from dt1 with time from dt2
# Hint: Time 8pm  time(hour=20)


def show_time_left():
    time_finish = datetime.combine(datetime.today(), time(hour=20))
    time_now = datetime.now()
    print("Time left in the session is ", time_finish - time_now)


show_time_left()

# A function can return a value to where it is called using the return statement
# A function can have several return lines. Nothing after the first return reached will be executed
# If a function returns a value I like to include the return type in the function name (useful in


def td_time_left():
    """Calculate time from now until 8pm tonight and return it as a datetime.timedelta"""
    time_finish = datetime.combine(datetime.today(), time(hour=20))
    time_now = datetime.now()
    time_delta = time_finish - time_now
    # print("Time left in session is {} (hh:mm:ss.ssssss)".format(time_delta))
    return time_delta

t = td_time_left()
print("Time left in session is {} (hh:mm:ss.ssssss)".format(t))

# A function's name has same rules as variable names because it is a variable name
# To assign to a new variable use function name without parentheses
time_left = td_time_left
print("Time left in session is {} (hh:mm:ss.ssssss)".format(time_left()))

# Challenge: Write a function which returns a datetime object for the same time as now but tomorrow
# Hint: timedelta(days=1)


def dt_same_time_tomorrow():
    """Returns the date and time one day after this function is called

    The return result is a datetime.datetime object"""
    time_today = datetime.now()
    one_day = timedelta(days=1)
    time_tomorrow = time_today + one_day
    return time_tomorrow


print("Same time tomorrow is", dt_same_time_tomorrow())
help(dt_same_time_tomorrow)


# A function can take one or more arguments also known as parameters
def flt_f_from_c(c):
    """Returns the temperature in Fahrenheit given the temperature in Celsius"""
    return c * 1.8 + 32


print("Temperature {:.2f}°C is equivalent to {:.2f}°F".format(0, flt_f_from_c(0)))
print("Temperature {:.2f}°C is equivalent to {:.2f}°F".format(100, flt_f_from_c(100)))
print("Temperature {:.2f}°C is equivalent to {:.2f}°F".format(-40, flt_f_from_c(-40)))
# ° = opt-shift-8 on Mac = alt0176 on Windows

# Challenge: Write a function which returns the time in seconds as a str in minutes and seconds
# Example str_min_sec(80) -> "1:20"
# Example str_min_sec(40) -> "0:40"
# Example str_min_sec(3601) -> "60:01"
# Example str_min_sec(-80) -> "-1:20"
# Example str_min_sec(-40) -> "-0:40"


def str_min_sec(seconds):
    """Converts seconds into minutes and seconds and returns result as a str
    Example: str_min_sec(-40) returns '-0:40'"""
    sign = ''
    if seconds < 0:
        sign = '-'
        seconds = -seconds
    return "{}{}:{:0>2}".format(sign, seconds // 60, seconds % 60)
print(40, str_min_sec(40))
print(80, str_min_sec(80))
print(3601, str_min_sec(3601))
print(-80, str_min_sec(-80))
print(-40, str_min_sec(-40))
# Functions can return more than one value by separating with commas
# Equivalent to returning a tuple with the values in it
# Challenge: Write a function which returns a sign, minutes and seconds given the seconds
def tpl_min_sec(seconds):
    sign = 1
    if seconds < 0:
        sign = -1
        seconds = -seconds
    return sign, seconds // 60, seconds % 60


sgn, mins, secs = tpl_min_sec(-40)
print("{} seconds is equivalent to sign={}, minutes={}, seconds={} ".format(-40, sgn, mins, secs))
print("repr(tpl_min_sec(375))", repr(tpl_min_sec(375)), type(tpl_min_sec(375)))
m = "my string"
print(m, repr(m), type(m))

# How to write tests to check your function
assert tpl_min_sec(40) == (1, 0, 40)
assert tpl_min_sec(80) == (1, 1, 20)
assert tpl_min_sec(3601) == (1, 60, 1)
assert tpl_min_sec(-80) == (-1, 1, 20)
assert tpl_min_sec(-40) == (-1, 0, 40)

import decimal
D = decimal.Decimal
D(10)
D("10")
D(2.2)


# Challenge: Write a function which returns price including GST given price excluding GST and GST rate
# Return the result as a decimal.Decimal with two decimal places
# Hint: Decimal method quantize(D("0.01")) rounds to two decimal places

def price_incl_gst(price_excl_gst, gst_rate=0.1):
    return round(D(price_excl_gst) * D(1 + gst_rate), 2)


print(price_incl_gst(D("1.1"), D("0.15")))
assert price_incl_gst(10, 0.1) == D("11")
assert price_incl_gst(2.2, 0.1) == D("2.42")
assert price_incl_gst(10) == D("11")
assert price_incl_gst(0) == 0
assert price_incl_gst(-2.2, 0.1) == D("-2.42")
assert price_incl_gst(D("1.1")) == D("1.21")
assert price_incl_gst(D("1.10")) == D("1.21")
assert price_incl_gst(D("1.1"), D("0.15")) == D("1.26")
# When calling a function you can supply parameters in a different order by using their names
assert price_incl_gst(gst_rate=D("0.15"), price_excl_gst=D("1.1")) == D("1.26")
# When calling a function you can supply parameters by expanding a list of the parameters
my_list = [12.345, 0.125]
assert price_incl_gst(*my_list) == D("13.89")
# When calling a function you can supply parameters by expanding a dict of the named parameters
my_dict = {'gst_rate': 1/3, 'price_excl_gst': 6.0}
assert price_incl_gst(**my_dict) == D("8.00")
