"""
MeetUp 022 - Beginners Python Support Sessions - Wed 07 Aug 2019 - Functions

Learning objectives:
    Functions:
    Data types: dict

@author D Tim Cummings

Challenge 1: How to create a function quadratic(x) = 1 - (x-1)²

Challenge 2: Create a function cubic(x) = x(x-1)(x-2).

Challenge 3: Print a table of v, quadratic(v) and cubic(v) with value v going from 0 to 2 in 0.1 steps

Challenge 4: Create functions:
    zero(x) which always returns zero regardless of the value of x
    line(x) which is the equation of a straight line with slope of 1 going through (0, 0)
    sine_wave(x) which is a sine wave with amplitude 1 and period 4

Challenge 5: Plot this data using matplotlib
    import matplotlib.pyplot as plt
    plt.plot(x, y, label=f.__name__, marker='x')
    plt.legend()
    plt.show()

Challenge 6: Create a function str_number_name_29(i) which takes an int from 0 to 29 and returns it's name as a str
    eg str_number_name_29(15) returns "fifteen"
hint: use list of number names up to 20
names_sub_20 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]

Challenge 7: Create a function str_number_name_99(i) which takes an int from 0 to 99 and returns it's name as a str
    eg str_number_name_99(33) returns "thirty-three"
hint: use dict of names of tens
names_tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
              60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}

Challenge 8: Write a function which accepts an int between 0 and 999 and returns it's name

Challenge 9: Write a function which accepts an int between 0 and 1 quadrillion and returns it's name
hint: use dict of names of powers
names_powers = {100: 'hundred', 1000: 'thousand', 1000000: 'million', 1000000000: 'billion', 1000000000000: 'trillion',
                1000000000000000: 'quadrillion', 1000000000000000000: 'Too big'}

"""
import matplotlib.pyplot as plt
import math


# Challenge 1: How to create a function quadratic(x) = 1 - (x-1)²
def quadratic(x):
    return 1 - (x - 1) ** 2


# Challenge 2: Create a function cubic(x) = x(x-1)(x-2).
def cubic(x):
    return (x-1) * (x-2) * x


# Challenge 3: Print a table of v, quadratic(v) and cubic(v) with value v going from 0 to 2 in 0.1 steps
for i in range(21):
    v = i / 10
    print("{:3.1f}  {:6.3f}  {:6.3f}".format(v, quadratic(v), cubic(v)))


# Challenge 4: Create functions zero(x), line(x), sine_wave(x):
def zero(x):
    return 0


def line(x):
    return x


def sine_wave(x):
    return math.sin(x * math.pi / 2)


# Challenge 5: Plot this data using matplotlib
lst_x = [i/10 for i in range(21)]
for f in [quadratic, zero, cubic, sine_wave, line]:
    lst_y = [f(x) for x in lst_x]
    plt.plot(lst_x, lst_y, label=f.__name__, marker='x')
plt.legend()
plt.show()


# Challenge 6: Create a function str_number_name_29(i) which takes an int from 0 to 29 and returns it's name as a str
names_sub_20 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def str_number_name_29(num):
    if num < len(names_sub_20):
        return names_sub_20[num]
    elif num < 30:
        return names_sub_20[20] + "-" + names_sub_20[num - 20]
    else:
        return "Too big"


names_tens = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
              60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}


# Challenge 7: Create a function str_number_name_99(i) which takes an int from 0 to 99 and returns it's name as a str
def str_number_name_99(num):
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
        return "Too big"


# Challenge 8: Write a function which accepts an int between 0 and 999 and returns it's name
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
    elif num < 1000000000:
        name = str_number_name_999(num // 1000000) + " million"
        if num % 1000000 == 0:
            return name
        elif num % 1000000 < 100:
            return name + " and " + str_number_name_999(num % 1000000)
        else:
            return name + " " + str_number_name_999(num % 1000000)
    else:
        return "Too big"


assert str_number_name_999(37) == "thirty-seven"
assert str_number_name_999(50) == "fifty"
assert str_number_name_999(323123) == "three hundred and twenty-three thousand one hundred and twenty-three"
for n in (323, 323123, 323023, 323023001, 20503015012, 1000000000000000):
    print("str_number_name_999({:,}) is {}".format(n, str_number_name_999(n)))


names_powers = {100: 'hundred', 1000: 'thousand', 1000000: 'million', 1000000000: 'billion', 1000000000000: 'trillion',
                1000000000000000: 'quadrillion', 1000000000000000000: 'Too big'}


# Challenge 9: Write a function which accepts an int between 0 and 1 quadrillion and returns it's name
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
    print("str_number_name({:,}) is {}".format(n, str_number_name(n)))
