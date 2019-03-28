"""
MeetUp 004 - Beginners Python Support Sessions 27-Mar-2019

Learning objectives:
    User defined functions
    Importing module datetime
    Testing with assert

@author D Tim Cummings

Challenge 1: Write a function which shows how much time is left in this session
Hint: datetime.datetime.combine(dt1, dt2) combines date from dt1 with time from dt2
Hint: Time 8pm  datetime.time(hour=20)
Advanced: Show time left until next session starts (next Wednesday night 5:30pm)
Hint: dt.weekday() gives day of week between 0 and 6 (0 = Monday) where dt is object of type datetime.datetime

Challenge 2: Write a function which returns the time to go before the next session starts

Challenge 3: Write a function which returns a datetime object for the same time as now but tomorrow
Hint: timedelta(days=1)

Challenge 4: Convert (0°C, 100°C, -40°C, 12.34°C) to °F by calling function. Show results using string formatting
assert flt_f_from_c(0) == 32
assert flt_f_from_c(100) == 212
assert flt_f_from_c(-40) == -40

Challenge 5: Write a function which returns a dict of coins to make up change amount
Advanced: Accept a country code (which defaults to 'au') to select between 'au' or 'us' coins
assert dct_coins(37) == {20: {'quantity': 1, 'name': 'florin'},
                         10: {'quantity': 1, 'name': 'shilling'},
                         5: {'quantity': 1, 'name': 'sixpence'},
                         2: {'quantity': 1, 'name': 'two cent'}}
assert dct_coins(37, country='us') == {25: {'quantity': 1, 'name': 'quarter'},
                                       10: {'quantity': 1, 'name': 'dime'},
                                       1: {'quantity': 2, 'name': 'penny'}}

Challenge 6: Write a function which accepts an int between 0 and 99 and returns it's name
Advanced: Accept int up to 999999
assert str_number_name(37) == "thirty-seven"
assert str_number_name(50) == "fifty"
assert str_number_name(323123) == "three hundred and twenty-three thousand one hundred and twenty-three"

"""
import datetime  # makes everything in datetime module available to this script


# A function is defined using def
def show_now():
    time_now = datetime.datetime.now().time()  # module datetime, class datetime, function now() in module
    print("The time is now", time_now)


# To call a function use the function's name followed by parentheses
show_now()
show_now()

# Choose a consistent naming scheme
# By convention, function names should be lower case with words separated by underscores
# Example naming scheme, if a function performs an action, start the function name with that action


# Challenge1: Write a function which shows how much time is left in this session
# Hint: datetime.datetime.combine(dt1, dt2) combines date from dt1 with time from dt2
# Hint: Time 8pm  datetime.time(hour=20)
# Advanced: Show time left until next session starts (next Wednesday night 5:30pm)
# Hint: dt.weekday() gives day of week between 0 and 6 (0 = Monday) where dt is object of type datetime.datetime
def show_time_left():
    # datetime now
    dt_now = datetime.datetime.now()
    # time 8pm
    time_finish = datetime.time(hour=20)
    # datetime today at 8pm
    dt_finish = datetime.datetime.combine(dt_now, time_finish)
    print("Time left in today's session is", dt_finish - dt_now)
    # time 5:30pm
    time_start = datetime.time(hour=17, minute=30)
    # Wednesday
    weekday_start = 2
    # Days until next Wednesday (mod 7 so between 0 and 6)
    days_to_start = (weekday_start - dt_now.weekday()) % 7
    # If today is Wednesday check if session already started. If so use next week
    if days_to_start == 0 and dt_now.time() > time_start:
        days_to_start += 7
    # Start date of next session
    date_start = dt_now.date() + datetime.timedelta(days=days_to_start)
    # Start date and time of next session
    dt_start = datetime.datetime.combine(date_start, time_start)
    # Time left until start of session next week
    time_delta = dt_start - dt_now
    print("Time before next session starts is", time_delta)


show_time_left()


# A function can return a value to where it is called using the return statement
# A function can have several return lines. Nothing after the first return reached will be executed
# If a function returns a value I like to include the return type in the function name
# Challenge 2: Write a function which returns the time before the next session starts
def td_time_before_next_session():
    """Calculate time from now until the next session starts (Wed 5:30pm) and return it as a datetime.timedelta"""
    # datetime now
    dt_now = datetime.datetime.now()
    time_start = datetime.time(hour=17, minute=30)
    weekday_start = 2
    days_to_start = (weekday_start - dt_now.weekday()) % 7
    if days_to_start == 0 and dt_now.time() > time_start:
        days_to_start += 7
    date_start = dt_now.date() + datetime.timedelta(days=days_to_start)
    dt_start = datetime.datetime.combine(date_start, time_start)
    time_delta = dt_start - dt_now
    return time_delta


# Using a function with parentheses calls the function and stores the return value
td_value = td_time_before_next_session()
print("Time before next session starts is {}".format(td_value))

# A function's name has same rules as variable names because it is a variable name
# To assign to a new variable use function name without parentheses
td_function = td_time_before_next_session
print("Time left to start of next session is {}".format(td_function()))


# Challenge 3: Write a function which returns a datetime object for the same time as now but tomorrow
# Hint: datetime.timedelta(days=1)
def dt_same_time_tomorrow():
    """Returns the date and time one day after this function is called

    The return result is a datetime.datetime object"""
    return datetime.datetime.now() + datetime.timedelta(days=1)


print("Same time tomorrow is", dt_same_time_tomorrow())
help(dt_same_time_tomorrow)  # displays docstring


# A function can take one or more arguments (also known as parameters)
def flt_f_from_c(c):
    """Returns the temperature in Fahrenheit given the temperature in Celsius"""
    return c * 1.8 + 32


# Challenge 4: Convert (0°C, 100°C, -40°C, 12.34°C) to °F by calling function.
# Show results using string formatting
for c in (0, 100, -40, 12.34):
    print("Temperature {0:>7.2f}°C is {1:>7.2f}°F".format(c, flt_f_from_c(c)))
# ° = opt-shift-8 on Mac = alt0176 on Windows


# asserts can be used to test your program in case someone makes a change later which breaks it
assert flt_f_from_c(0) == 32
assert flt_f_from_c(100) == 212
assert flt_f_from_c(-40) == -40


# Challenge 5: Write a function which returns a dict of coins to make up change amount
# Advanced: Accept a country code (which defaults to 'au') to select between 'au' or 'us' coins
def dct_coins(change, country='au'):
    coin_us = {1: 'penny', 5: 'nickel', 10: 'dime', 25: 'quarter'}
    coin_au = {1: 'cent', 2: 'two cent', 5: 'sixpence', 10: 'shilling', 20: 'florin', 50: 'crown' }
    if country == 'au':
        coin = coin_au
    else:
        coin = coin_us
    coin_values = sorted(coin, reverse=True)
    coins = {}
    for coin_value in coin_values:
        count, change = divmod(change, coin_value)
        if count > 0:
            # add into coins coin_value and quantity
            coins[coin_value] = {'quantity': count, 'name': coin[coin_value]}
    return coins


assert dct_coins(37) == {20: {'quantity': 1, 'name': 'florin'},
                         10: {'quantity': 1, 'name': 'shilling'},
                         5: {'quantity': 1, 'name': 'sixpence'},
                         2: {'quantity': 1, 'name': 'two cent'}}
assert dct_coins(37, country='us') == {25: {'quantity': 1, 'name': 'quarter'},
                                       10: {'quantity': 1, 'name': 'dime'},
                                       1: {'quantity': 2, 'name': 'penny'}}


print(37, dct_coins(37))
print(37, dct_coins(37, 'us'))


# Challenge 6: Write a function which accepts an int between 0 and 99 and returns it's name
# Advanced: Accept int up to 999999
def str_number_name(num):
    """Returns a number's name in text as a str (0 - 999,999,999)"""
    names_sub_20 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                    "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
    names_tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
                  60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
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
        hundreds = num // 100
        sub100 = num % 100
        if sub100 == 0:
            return names_sub_20[hundreds] + " hundred"
        else:
            return names_sub_20[hundreds] + " hundred and " + str_number_name(sub100)
    elif num < 1000000:
        thousands = num // 1000
        sub1000 = num % 1000
        if sub1000 == 0:
            return str_number_name(thousands) + " thousand"
        elif sub1000 < 100:
            return str_number_name(thousands) + " thousand and " + str_number_name(sub1000)
        else:
            return str_number_name(thousands) + " thousand " + str_number_name(sub1000)
    elif num < 1000000000:
        name = str_number_name(num // 1000000) + " million"
        if num % 1000000 == 0:
            return name
        elif num % 1000000 < 100:
            return name + " and " + str_number_name(num % 1000000)
        else:
            return name + " " + str_number_name(num % 1000000)
    else:
        return "Too big"


assert str_number_name(37) == "thirty-seven"
assert str_number_name(50) == "fifty"
assert str_number_name(323123) == "three hundred and twenty-three thousand one hundred and twenty-three"
for n in (323, 323123, 323023, 323023001, 20503015012, 1000000000000000):
    print("str_number_name({:,}) is {}".format(n, str_number_name(n)))


def str_number_name2(num):
    """Returns a number's name in text as a str (0 - 999,999,999,999,999,999). Easily extendable to larger numbers"""
    names_sub_20 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                    "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
    names_tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
                  60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
    names_powers = {100: 'hundred', 1000: 'thousand', 1000000: 'million', 1000000000: 'billion', 1000000000000: 'trillion', 1000000000000000: 'quadrillion', 1000000000000000000: 'Too big'}
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
                name = str_number_name2(num // power) + " " + names_powers[power]
                if num % power == 0:
                    return name
                elif num % power < 100:
                    return name + " and " + str_number_name2(num % power)
                else:
                    return name + " " + str_number_name2(num % power)
            idx += 1
    return "Too big"


assert str_number_name2(37) == "thirty-seven"
assert str_number_name2(50) == "fifty"
assert str_number_name2(323123) == "three hundred and twenty-three thousand one hundred and twenty-three"
for n in (323, 12323123323023, 323023001, 20503015012, 1000000000000000):
    pass
    print("str_number_name2({:,}) is {}".format(n, str_number_name2(n)))
