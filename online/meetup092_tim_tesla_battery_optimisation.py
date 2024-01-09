#!/usr/bin/env python3
"""MeetUp 092 - Beginners Python and Machine Learning - 19th Jan 2021 - Optimise Tesla SA Battery

Continuation from MeetUp 091 on 12th Jan 2021

Youtube: https://youtu.be/yn9FcpRLHgU
Colab:   https://colab.research.google.com/drive/1v-QMawPtWPtUAa0LNEmbZUElFVdYziUx
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/275785495

Learning objectives:
- scipy optimize

@author D Tim Cummings

Optimise operation of a South Australian style Tesla battery linked to a solar farm by choosing parameters to decide
when to buy or sell electricity from the grid

References:
- https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
- https://docs.sympy.org
- https://scipy-lectures.org/advanced/mathematical_optimization/

To install third party libraries, add the following to file requirements.txt

pandas
numpy
matplotlib
scipy
sympy

and run

pip install --requirement requirements.txt
"""

# Standard libraries
import datetime
import logging
import pytest
import warnings
# Third party libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import sympy

logger = logging.getLogger(__name__)


# We have a function which we want to find the minimum value
def parabola(a):
    return a * a - 6.2 * a + 10


# Plot the function to see what it looks like
lx, ly = [], []  # Set up two empty lists for x and y values
for i in range(63):
    x = i/10
    y = parabola(x)
    lx.append(x)
    ly.append(y)
plt.plot(lx, ly)
plt.show()

print("To find the minimum we could try lots of values of x and see which produces the lowest value of y")
x_min = -1
y_min = parabola(x_min)
for x in range(6):
    y = parabola(x)
    if y < y_min:
        x_min, y_min = x, y
    print(f"x={x:6.3f} y={y:6.3f} x_min={x_min:6.3f} y_min={y_min:6.3f} ")
print()

# scipy.optimize provides the minimize_scalar function which does this for us
# we pass in the function name (which is callable)
# minimize_scalar is good for functions which take a single argument
# notice the success attribute to determine if it was successful
print("\nFinding the minimum using scipy.optimize.minimize_scalar")
print(opt.minimize_scalar(parabola))
print()

# Get help on minimize_scalar in IPython.
# opt.minimize_scalar?
# For Python use - uncomment following line to see
# help(opt.minimize_scalar)

# Find additional options possible - uncomment following line to see
# opt.show_options(solver='minimize_scalar')

print("\nWatch as minimize_scalar converges on a solution")
opt.minimize_scalar(parabola, method='bounded', bounds=(-10, 10), options={'disp': 3})


# Python has a built-in function to determine if something is callable.
# Note that functions are callable and variables are not
print(f"\n {callable(parabola)=}, {callable(y_min)=}")

print("\nscipy.optimize also provides the minimize function which is useful if function takes multiple arguments")
# we need to also provide an initial guess as a sequence (list or tuple or np.array) of initial values of all arguments
print(f"{opt.minimize(parabola, x0=np.array([200]))=}")  # for a single value could also pass in x0=200


# Challenge 1: Plot the following curve and find where the minimum value occurs
# Try starting values of 10, -10, 3, 4
def quartic(a):
    return (a - 0.5) * (a - 3) * (a - 4) * (a - 5.5)


print("\nSolution 1:")
x = [i/10 for i in range(63)]
y = [quartic(x[i]) for i in range(63)]
plt.plot(x, y)
plt.show()

# Try different methods. Just lucky whether it finds global minimum or local minimum
result = opt.minimize_scalar(quartic)
print(f"Minimize.scalar quartic                      x_min={result.x:10.7f} y_min={result.fun:12.7f} success={result.success}")
for guess in [10, -10, 3, 4]:
    result = opt.minimize(quartic, x0=np.array([guess]))
    print(f"Minimize quartic from initial guess={guess:8.3f} x_min={result.x[0]:10.7f} y_min={result.fun:12.7f} success={result.success}")

# Challenge 2: Repeat loop of Solution 1 but keep a list of all local minima
# Note that the following code produces the wrong answer because there are only two minima
minima = set()
for guess in [10, -10, 3, 4]:
    result = opt.minimize(quartic, x0=np.array([guess]))
    print(f"Minimize quartic from guess={guess:8.3f} x_min={result.x[0]:10.7f} y_min={result.fun:12.7f} ")
    minima.add(result.x[0])
print(f"All local minima: {minima}  :( DUPLICATIONS")

# Solution 2: Calculating absolute tolerance manually - Have to know magnitude of answers to get this right
# Uses extra variable
print(f"\nSolution 2 - using manual tolerance calculation")
minima = set()
for guess in [10, -10, 3, 4]:
    result = opt.minimize(quartic, x0=np.array([guess]))
    print(f"Minimize quartic from guess={guess:8.3f} x_min={result.x[0]:10.7f} y_min={result.fun:12.7f} ")
    tf_found = False
    for prev_solution in minima:
        if abs(prev_solution - result.x[0]) < 1e-5:
            tf_found = True
    if not tf_found:
        minima.add(result.x[0])
print(f"All local minima: {minima}")

# Solution 2: Using approx from pytest library which checks relative and absolute tolerance
print(f"\nSolution 2 - using pytest approx")
minima = set()
for guess in [10, -10, 3, 4]:
    result = opt.minimize(quartic, x0=np.array([guess]))
    print(f"Minimize quartic from guess={guess:8.3f} x_min={result.x[0]:10.7f} y_min={result.fun:12.7f} ")
    # Keep a list of all unique solutions
    # pytest.approx: Comparing floating point numbers. Checks for relative tolerance of 1e-6 or absolute tolerance of 1e-12
    # break: breaks out of innermost for or while loop
    # else:  after for or while loop only runs if no breaks occur
    for minimum in minima:
        if pytest.approx(minimum) == result.x[0]:
            break
    else:
        minima.add(result.x[0])
print(f"All local minima: {minima}")

print("\nBrute force solution evaluates function at various steps across range")
print(opt.brute(quartic, ranges=[(-100, 100)], Ns=1000))

print("\nEven brute force doesn't work if we don't have enough steps. Example with 20 steps instead of 1000")
print(opt.brute(quartic, ranges=[(-100, 100)], Ns=20))

print("\nbasinhopping finds global minimum from an initial guess. Number of iterations = 100 is not enough in this example")
print(opt.basinhopping(quartic, x0=10, niter=1000))

print("\nshgo is another scipy optimizer to find global minimum")
print(opt.shgo(quartic, bounds=[(-1000, 1000)]))

print("\ndifferential_evolution is another scipy optimizer to find global minimum")
print(opt.differential_evolution(quartic, bounds=[(-1000, 1000)]))

print("\ndual_annealing is another scipy optimizer to find global minimum")
print(opt.dual_annealing(quartic, bounds=[(-1000, 1000)]))

print("\nshgo can find all local minima with sampling_method='sobol'")
print(opt.shgo(quartic, bounds=[(-1000, 1000)], n=40, iters=50, sampling_method='sobol'))

# print("\nWithin an algorithm for finding global minimum you can specify minimizer for finding local minimum")
# help(opt.shgo)

# There are several methods that can be used to minimize. Some require additional arguments. Nelder-Mead does not.
# Default method is "BFGS" when no constraints or bounds
opt.minimize(quartic, x0=np.array(4), method="Nelder-Mead")

print("\nDifferent methods that can be used in minimize")
methods = [None, "Nelder-Mead", "CG", "BFGS", "Newton-CG", "dogleg", "trust-ncg", "trust-krylov", "trust-exact", "L-BFGS-B", "Powell", "TNC", "COBYLA", "SLSQP", "trust-constr"]
for method in methods:
    try:
        result = opt.minimize(quartic, x0=np.array(4), method=method)
        print(f"{str(method):15} {str(result.success):5} {result.x[0]}")
    except ValueError as ve:
        print(f"{method:15} ValueError: {ve}")
    except IndexError as ie:
        print(f"{method:15} IndexError: {ie}")

# Some methods require first and second derivatives.
print("Using sympy to calculate first and second derivatives because we know the algebraic formula")
x = sympy.symbols('a')
q = (x - 0.5) * (x - 3) * (x - 4) * (x - 5.5)
print(q)
print(q.expand())  # opposite of factorize
print(q.expand().diff(x))  # differentiate
print(q.expand().diff(x).diff(x))  # differentiate twice
print(sympy.latex(q.expand()))  # just for fun, produce latex of equation

# To display LaTeX in colab markdown cells (not code cells), surround with dollar signs
#
# $a^{4} - 13.0 a^{3} + 56.75 a^{2} - 91.25 a + 33.0$


def quartic_derivative_1(a: np.ndarray) -> np.ndarray:
    """First derivative of quartic - jacobian"""
    return 4 * a**3 - 39 * a**2 + 113.5 * a - 91.25


def quartic_derivative_2(a: np.ndarray) -> np.ndarray:
    """Second derivative of quartic - hessian"""
    return 12 * a**2 - 78 * a + 113.5


print("\nUsing different methods with minimize, suppressing warnings, providing jacobian and hessian")
methods = [None, "Nelder-Mead", "CG", "BFGS", "Newton-CG", "dogleg", "trust-ncg", "trust-krylov", "trust-exact", "L-BFGS-B", "Powell", "TNC", "COBYLA", "SLSQP", "trust-constr"]
for method in methods:
    try:
        with warnings.catch_warnings():
            # turn off warnings about providing arguments that are not used
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            result = opt.minimize(quartic, x0=np.array([4]), jac=quartic_derivative_1, hess=quartic_derivative_2, method=method)
        print(f"{str(method):15} {str(result.success):5} {result.x[0]}")
    except ValueError as ve:
        print(f"{method:15} ValueError: {ve}")
    except IndexError as ie:
        print(f"{method:15} IndexError: {ie}")


# Function defined in meetup091 for plotting results
def plot_battery(df_for_plot):
    """Plot two subplots, one above the other, based on same x axis (datetime) but their own y axes.
    
    Code to set lines or dots, colours, legends, y axis ranges, axis titles"""
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 10), sharex='all')
    axes[0].set_title("Battery Levels")
    df_for_plot.plot(kind='line', y='mwh_level', ax=axes[0])
    axes[0].set_ylabel('Storage level (MWh)')
    axes[0].set_ylim([0, df_for_plot['mwh_level'].max() * 1.2])
    axes[0].legend(loc='upper left')
    df_for_plot.plot(kind='line', y='RRP', ax=axes[1], color='orange')
    df_for_plot.plot(kind='line', y='sell', ax=axes[1], linestyle=' ', marker='o', markersize=0.5, color='red')
    df_for_plot.plot(kind='line', y='buy', ax=axes[1], linestyle=' ', marker='o', markersize=0.5, color='green')
    axes[1].set_xlabel('date')
    axes[1].set_ylabel('RRP')
    axes[1].set_ylim([0, 500])
    axes[1].legend(loc='upper left')
    plt.show()


# Code from meetup091 notebook
# Locations for data on Internet and in file system
date_start = datetime.datetime(year=2020, month=11, day=1)
date_finish = datetime.datetime(year=date_start.year + date_start.month // 12, month=date_start.month % 12 + 1, day=1)
date_finish_yesterday = date_finish - datetime.timedelta(days=1)
str_start = date_start.strftime('%Y%m%d')
str_finish = date_finish_yesterday.strftime('%Y%m%d')
url = f"http://nemlog.com.au/api/unit/EMERASF1/{str_start}/{str_finish}/csv"
filename = f"unit_emerasf1_{str_start}_{str_finish}.csv"
print("\nGetting electricity data for modelling")
print(f"{url=}")
print(f"{filename=}")
# Read URL and save result into a file for future use
try:
    df = pd.read_csv(filename, parse_dates=['SETTLEMENTDATE'], index_col='SETTLEMENTDATE')
except FileNotFoundError:
    logging.info(f"File {filename} not found so retrieving from Internet")
    df = pd.read_csv(url, parse_dates=['SETTLEMENTDATE'], index_col='SETTLEMENTDATE')
    df.to_csv(filename)


class Battery:
    """
    A Battery object represents a battery/operator combination. For the battery it
    knows the size of battery storage in MWh, the efficiency of storing energy, 
    the maximum charge/discharge rate in MW, and how much energy is currently in 
    the battery.
    For the operator it knows how the operator makes decisions on when to charge
    the battery (buy electricity), when to discharge (sell electricity), and how 
    much profit the operator has made from buying and selling.
    """

    def __init__(self, mwh_capacity, mw_limit, efficiency=0.9):
        """
        Constructor of Battery objects

        :param mwh_capacity: Full number of MWh battery can store after all charging and discharging losses
        :param mw_limit: Maximum rate MW battery can send power to/from the grid
        :param efficiency: Round trip efficiency of charging and discharging battery. 0.9 = 90%
        """
        self.mwh_capacity = mwh_capacity
        self.mw_limit = mw_limit
        self.efficiency = efficiency
        self.mwh_level = 0
        self.aud_profit = 0
    
    def mwh_charge(self, duration_minutes, pc_rate=1):
        """Instruction for battery to charge for the specified number of minutes at a percentage (pc_rate) of its maximum rate"""
        # capacity left for charging. mwh is a local variable not an instance variable
        mwh = self.mwh_capacity - self.mwh_level
        # MWh if charging at maximum rate. mw_limit is at grid
        pc_rate = min(max(pc_rate, 0), 1)
        mwh_max = self.mw_limit * pc_rate * self.efficiency * duration_minutes / 60
        # clip the return value to [0, mwh_max]. Could also use numpy.clip
        mwh = min(max(mwh, 0), mwh_max)
        # adjust the battery level by the MWh to be stored in battery
        self.mwh_level += mwh
        mw = mwh / self.efficiency / duration_minutes * 60
        logging.debug(f"After charging at {mw:6.2f}MW for {duration_minutes}minutes, the battery level is {self.mwh_level:6.2f}MWh")
        # return the MWh purchased from the grid
        return mwh / self.efficiency

    def mwh_discharge(self, duration_minutes, pc_rate=1):
        """Instruction for battery to discharge for the specified number of minutes at a percentage (pc_rate) of its maximum rate"""
        # capacity left for discharging
        mwh = self.mwh_level
        # MWh if discharging at maximum rate
        pc_rate = min(max(pc_rate, 0), 1)
        # if not (0 <= pc_rate <= 1):
        #     raise ValueError("mwh_discharge: pc_rate must be between 0 and 1 inclusive")
        mwh_max = self.mw_limit * pc_rate * duration_minutes / 60
        # clip the return value to [0, mwh_max]. Could also use numpy.clip
        mwh = min(max(mwh, 0), mwh_max)
        # adjust the battery level
        self.mwh_level -= mwh
        # return the charge amount in MWh
        mw = mwh / duration_minutes * 60
        logging.debug(f"After discharging at {mw:6.2f}MW for {duration_minutes}minutes, the battery level is {self.mwh_level:6.2f}MWh")
        return mwh

    def mwh_decide(self, rrp, rrp_break, duration_minutes):
        """Instruction for battery to look at current price and charge or discharge"""
        if rrp > rrp_break:
            mwh = self.mwh_discharge(duration_minutes)
        elif rrp < rrp_break * self.efficiency:
            mwh = -self.mwh_charge(duration_minutes)
        else:
            mwh = 0
        self.aud_profit += mwh * rrp
        # logging.INFO = 20, logging.DEBUG = 10. Can add logging levels 
        logging.log(15, f"After Grid change of {mwh:6.2f}MWh at RRP ${rrp:8,.2f}/MWh, profit is ${self.aud_profit:10,.2f}, level is {self.mwh_level:6.2f}MW")
        return mwh


# test the class by creating an instance
b = Battery(mwh_capacity=129, mw_limit=100, efficiency=0.9)

# Check current storage level and operating profit
logger.info(f"After creating Battery {b.mwh_level=}, {b.aud_profit=}")

price_break = 70  # Buy below $70/MWh Sell above $70/MWh
duration = 5  # Minutes for current instruction
price = 50
print(f"RRP ${price:5.2f} Decision {b.mwh_decide(price, price_break, duration):7.1f} MWh, level {b.mwh_level:7.1f} MWh, profit ${b.aud_profit:10,.2f}")
print(f"RRP ${price:5.2f} Decision {b.mwh_decide(price, price_break, duration):7.1f} MWh, level {b.mwh_level:7.1f} MWh, profit ${b.aud_profit:10,.2f}")
print(f"RRP ${price:5.2f} Decision {b.mwh_decide(price, price_break, duration):7.1f} MWh, level {b.mwh_level:7.1f} MWh, profit ${b.aud_profit:10,.2f}")
price = 90
print(f"RRP ${price:5.2f} Decision {b.mwh_decide(price, price_break, duration):7.1f} MWh, level {b.mwh_level:7.1f} MWh, profit ${b.aud_profit:10,.2f}")


# Test battery for month using a price break of $65/MWh
def plot_battery_for_price_break(rrp_break=65):
    battery = Battery(mwh_capacity=129, mw_limit=100)
    for idx in df.index:
        mwh_buy_or_sell = battery.mwh_decide(df.at[idx, 'RRP'], rrp_break, duration)
        if mwh_buy_or_sell > 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, df.at[idx, 'RRP']
        elif mwh_buy_or_sell < 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = df.at[idx, 'RRP'], None
        else:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, None
        df.at[idx, 'aud_profit'] = mwh_buy_or_sell * df.at[idx, 'RRP']
        df.at[idx, 'mwh_level'] = battery.mwh_level
    print(f"RRP break point ${rrp_break:5,.2f}. Profit ${battery.aud_profit:10,.2f}  ")
    pd.set_option('display.max_columns', 20)
    print(df.head())
    plot_battery(df)


plot_battery_for_price_break(65)

# Find the optimum price break point using scipy.optimize.minimize(fun, x0, method, options)
#     fun is loss or objective function to be minimised. Loss is negative of profit (which we want to maximise)
#     x0 is initial guess array. Can be numpy ndarray or python list
#     method is optimization method. Try 'Nelder-Mead'
#     options is dict of options eg {'disp': True, 'xatol': 0.1, 'fatol': 10}
#         disp: set to True to print convergence messages
#         xatol: Absolute error in xopt between iterations that is acceptable for convergence
#         fatol: Absolute error in func(xopt) between iterations that is acceptable for convergence.
# Method Nelder-Mead uses the Simplex algorithm. This algorithm is robust in many applications. However, if
# numerical computation of derivative can be trusted, other algorithms using the first and/or second derivatives
# information might be preferred for their better performance in general.

# Challenge 3: Find the optimum rrp break point using scipy.optimize.minimize(fun, x0, method, options)


def loss_function_for_rrp_break(array_x):
    rrp_break = array_x[0]
    duration_minutes = 5
    battery_local = Battery(mwh_capacity=129, mw_limit=100)
    for idx in df.index:
        mwh_buy_or_sell = battery_local.mwh_decide(df.at[idx, 'RRP'], rrp_break, duration_minutes)
        if mwh_buy_or_sell > 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, df.at[idx, 'RRP']
        elif mwh_buy_or_sell < 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = df.at[idx, 'RRP'], None
        else:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, None
        df.at[idx, 'aud_profit'] = -mwh_buy_or_sell * df.at[idx, 'RRP']
        df.at[idx, 'mwh_level'] = battery_local.mwh_level
    aud_profit_excl_storage = battery_local.aud_profit
    aud_profit_incl_storage = aud_profit_excl_storage + battery_local.mwh_level * rrp_break
    print(f"RRP break point ${rrp_break:6,.2f}. Profit incl storage ${aud_profit_incl_storage:11,.2f}")
    return -aud_profit_incl_storage


print(f"Optimising result using minimize")
result = opt.minimize(loss_function_for_rrp_break, x0=np.array([50]), method='Nelder-Mead', options={'disp': True, 'xatol': 0.1, 'fatol': 10})
print(f"Optimisation result using minimize {result}")
plot_battery(df_for_plot=df)

print(f"Optimising result using shgo")
result = opt.shgo(loss_function_for_rrp_break, bounds=[(30, 150)], minimizer_kwargs={'method': 'Nelder-Mead', 'options': {'disp': True, 'xatol':0.1, 'fatol': 10}})
print(f"Optimisation result using shgo {result}")
plot_battery(df_for_plot=df)

# Challenge 4: Modify mwh_decide(self, rrp, rrp_break, duration_minutes) so that it takes
# an additional parameter rrp_gap being the additional difference between minimum sell and maximum buy
# Optimise


# Solution 4
def mwh_decide(self, rrp, rrp_break, duration_minutes, rrp_gap=0):
    """Instruction for battery to look at current price and charge or discharge"""
    if rrp > rrp_break + rrp_gap:
        mwh = self.mwh_discharge(duration_minutes)
    elif rrp < rrp_break * self.efficiency:
        mwh = -self.mwh_charge(duration_minutes)
    else:
        mwh = 0
    self.aud_profit += mwh * rrp
    # logging.INFO = 20, logging.DEBUG = 10
    logging.log(15, f"After Grid change of {mwh:6.2f}MWh at RRP ${rrp:8,.2f}/MWh, break ${rrp_break:6,.2f}/MWh, gap ${rrp_gap:6,.2f}/MWh, profit is ${self.aud_profit:10,.2f}, level is {self.mwh_level:6.2f}MW")
    return mwh


Battery.mwh_decide = mwh_decide


def loss_function_for_rrp_break_and_gap(lst_x):
    rrp_break = lst_x[0]
    # Challenge 4
    rrp_gap = lst_x[1]
    # Tesla battery for South Australia. Cost ~ AUD 90 million + maintenance AUD 5 million per year, capacity 129 MWh, throughput 100 MW
    # Challenge 4
    battery = Battery(mwh_capacity=129, mw_limit=100)
    for idx in df.index:
        mw_buy_or_sell = battery.mwh_decide(df.at[idx, 'RRP'], rrp_break=rrp_break, duration_minutes=5, rrp_gap=rrp_gap)
        if mw_buy_or_sell > 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, df.at[idx, 'RRP']
        elif mw_buy_or_sell < 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = df.at[idx, 'RRP'], None
        else:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, None
        df.at[idx, 'aud_profit'] = -mw_buy_or_sell * df.at[idx, 'RRP'] / 12
        df.at[idx, 'mwh_level'] = battery.mwh_level
    aud_profit_incl_storage = battery.aud_profit + battery.mwh_level * rrp_break
    print(f"RRP break point ${rrp_break:7,.2f}/MWh, gap ${rrp_gap:7,.2f}/MW. Profit incl storage ${aud_profit_incl_storage:10,.2f}")
    return -aud_profit_incl_storage


print(f"Optimising result using minimize and two parameters")
result = opt.minimize(loss_function_for_rrp_break_and_gap, x0=np.array([60, 30]), method='Nelder-Mead', options={'disp': True, 'xatol': 0.1, 'fatol': 10})
print(f"Optimisation result {result}")
plot_battery(df_for_plot=df)

# Use a global searching method to ensure we haven't found a local minimum
print(f"Optimising result using differential_evolution and two parameters")
result = opt.differential_evolution(loss_function_for_rrp_break_and_gap, bounds=[(20, 100), (-20, 80)])
print(f"Optimisation result {result}")
plot_battery(df_for_plot=df)
