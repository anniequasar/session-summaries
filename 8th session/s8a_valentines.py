# -*- coding: utf-8 -*-
"""
Valentine's Day - Beginners Python Session 8 - s8a_valentine.py

@author: Tim Cummings

Challenge: Find the perfect match between the functions
Put all five functions in a list.
Loop through all possible permutations of 2 functions from 5.
Find the best match at points x = 0, x = 1, x = 2 by summing
the squares of the differences of the function values at the
two points.

Challenge: Repeat the exercise at more points x in (0, 0.5, 1, 1.5, 2)

How to use range() in for loops
range(4) = (0, 1, 2, 3)
range(2, 5) = (2, 3, 4)
range(3, 10, 2) = ( 3, 5, 7, 9 )
"""

import math

def quadratic(x):
    return 1 - (x - 1) ** 2

def zero(x):
    return 0

def cubic(x):
    return (x-1) * (x-2) * x

def sine_wave(x):
    return math.sin(x * math.pi / 2)

def line(x):
    return x

list_funcs = [quadratic, zero, cubic, sine_wave, line]

# Minimum sum of squares of the differences = min_ss
min_ss = None
for i in range(len(list_funcs) - 1):
    fa = list_funcs[i]
    for j in range(i + 1, len(list_funcs)):
        fb = list_funcs[j]
        # This sum of squares of the differences = ss
        ss = 0
        for x in (0, 0.5, 1, 1.5, 2):
            ss += (fa(x) - fb(x)) ** 2
        print(i, fa.__name__, j, fb.__name__, ss)
        if min_ss is None or min_ss > ss:
            # found a new minimum sum of squares so save fa fb and ss
            min_ss, min_fa, min_fb = ss, fa, fb
print("Sum of squares between {} and {} is {}".format(min_fa.__name__, min_fb.__name__, min_ss))
