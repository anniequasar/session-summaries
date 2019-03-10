# -*- coding: utf-8 -*-
"""
Functions - Beginners Python Session 9

@author: Tim Cummings

Demonstrates: matplotlib, list comprehension, functions in variables
"""

import matplotlib.pyplot as plt
import math
import numpy as np


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


x = [0, .2, .4, .6]
# Challenge: Increase x range to 2.0
# Solution 1: three lines of code with a loop
x = list()
for i in range(0, 11):
    x.append(i/5)
# Solution 2: one line of code using list comprehension
x = [i/5 for i in range(11)]
# Solution 3: using numpy
x = np.arange(0, 2.1, 0.2)

# Challenge: Plot all the functions in matplotlib
list_funcs = [quadratic, zero, cubic, sine_wave, line]
for f in list_funcs:
    y = [f(xi) for xi in x]
    plt.plot(x, y, label=f.__name__, marker='x')
plt.legend()
plt.show()
