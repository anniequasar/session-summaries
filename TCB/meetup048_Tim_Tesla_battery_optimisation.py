#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wednesday MeetUp 048 - Beginners Python and Machine Learning - 25th Feb 2020 - Optimise Tesla SA Battery

Learning objectives:
    Object oriented program (class)
    pandas DataFrames
    scipy optimize

@author D Tim Cummings

Project to optimise operation of a South Australian style Tesla battery linked to a solar farm

Challenge 1: Read electricity production (MW) from a solar farm for a month and find the average for each hour of the
day plotting the results on a chart
i.e. the value for 9am is the average from 9am to 10am over all days in the month
Emerald solar farm data for January is http://nemlog.com.au/api/unit/EMERASF1/20200101/20200131/csv
Steps:
    Read CSV file into dataframe or url using pandas.read_csv()
    Convert SETTLEMENTDATE to datetime and set as index column
    Add another column to dataframe storing the hour of the day
    Group results by hour and find the average of SCADAVALUE and RRP
    Plot results using provided function plot_by_hour(df)

Data can be retrieved from http://nemlog.com.au. See http://nemlog.com.au/nlog for examples
http://nemlog.com.au/nlog/qld-large-scale-solar-24-hour-and-cumulative-maximum-outputs-for-period-01-april-2017-to-20-august-2019/

SETTLEMENTDATE is the date and time at the end of 5 minutes of production
DUID is the unit ID for the solar farm, in this case EMERASF1
RRP is the current electricity price on the grid for this region $/MWh (regional reference price)
REGIONID is the location of the solar farm in this case QLD1
SCADAVALUE is the electricity production from the solar farm MW

Challenge 2: We want to install a Tesla battery like the one installed in South Australia to smooth the electricity
output from renewable energy sources. Storage capacity 129 MWh, power limit from or to grid is 100 MW.
Assume 90% efficiency (100 MW to battery for one hour increases storage level by 90 MWh. 100 MW from battery for one hour reduces storage level by 100 MWh)
Battery to discharge at power limit when sell price > $ 60 /MWh of stored energy
Battery to charge at power limit when buy price < $ 60 /MWh of stored energy
Steps:
    Create a class Battery to model the behaviour of the battery
        Initialising instance of Battery will require mwh_capacity (129 MWh), mw_limit (100 MW), efficiency(0.9), rrp_break ($60/MWh)
        Battery will need instance variables to track energy stored (mwh_level) and value of buy/sell transactions (aud_profit).
        Battery will need a method which decides how much power to buy or sell for 5 minutes given the current price (mw_decision(rrp))
        Method mw_decision(rrp) will check that battery level does not reduce below 0 or exceed mwh_capacity
        Calling mw_decision(rrp) will update mwh_level and aud_profit and return the power (MW) bought (+ve) or sold (-ve)
    Write a Python script to run model for all data in dataframe
        Create an instance of type Battery
        Loop through dataframe (using idx as loop variable)
            get MW bought or sold by battery
            Store buy price in df.at[idx, 'buy'], sell price in df.at[idx, 'sell'], level in df.at[idx, 'mwh_level']
        Print final profit of battery
        Plot results using provided function plot_battery(df)

Challenge 3: Find the optimum price break point using scipy.optimize.minimize(fun, x0, method, options)
    fun is loss or objective function to be minimised. Loss is negative of profit (which we want to maximise)
    x0 is initial guess array. Can be numpy ndarray or python list
    method is optimization method. Try 'Nelder-Mead'
    options is dict of options eg {'disp': True, 'xatol': 0.1, 'fatol': 10}
        disp: set to True to print convergence messages
        xatol: Absolute error in xopt between iterations that is acceptable for convergence
        fatol: Absolute error in func(xopt) between iterations that is acceptable for convergence.
Method Nelder-Mead uses the Simplex algorithm. This algorithm is robust in many applications. However, if
numerical computation of derivative can be trusted, other algorithms using the first and/or second derivatives
information might be preferred for their better performance in general.

Challenge 4: Modify mw_decision(rrp) so that if rrp is only just higher than rrp only a little bit of electricity is
sold but if rrp is a lot higher then it is sold at maximum rate.
    Optimise how much to sell based on how much above rrp

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import math
import random
import logging


logging.getLogger().setLevel(logging.DEBUG)
challenge = 0  # number between 0 and 4 indicating which challenge to run


def plot_by_hour(df_for_plot, title):
    ax = plt.gca()  # get current axis so that both plots are on same chart
    plt.xlabel('hour of day')
    plt.suptitle('Profile')
    plt.title(title)
    df_for_plot.plot(kind='line', y='SCADAVALUE', ax=ax, color='yellow')
    plt.ylabel('Average MW generation during hour')
    df_for_plot.plot(kind='line', y='RRP', ax=ax, secondary_y=True, color='red')
    ax.set_ylim([0, df_for_plot['SCADAVALUE'].max() * 1.1])
    ax.right_ax.set_ylim([0, df_for_plot['RRP'].max() * 1.1])
    ax.legend(loc='best')
    plt.ylabel('Average $/MWh during hour')
    plt.show()


def plot_battery(df_for_plot):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 10), sharex='all')
    axes[0].set_title("Battery Levels")
    axes[0].set_ylabel('Storage level (MWh)')
    axes[0].set_ylim([0, df_for_plot['mwh_level'].max() * 1.2])
    df_for_plot.plot(kind='line', y='mwh_level', ax=axes[0])
    df_for_plot.plot(kind='line', y='RRP', ax=axes[1])
    df_for_plot.plot(kind='line', y='sell', ax=axes[1], linestyle=' ', marker='o', markersize=0.5, color='red')
    df_for_plot.plot(kind='line', y='buy', ax=axes[1], linestyle=' ', marker='o', markersize=0.5, color='green')
    axes[1].set_xlabel('date')
    axes[1].set_ylabel('RRP')
    axes[1].set_ylim([0, 500])
    axes[1].legend(loc='best')
    plt.show()


def plot_car(df_for_plot):
    ax = plt.gca()  # get current axis so that both plots are on same chart
    plt.xlabel('km travelled')
    plt.ylabel('Litres')
    df_for_plot.plot(kind='line', y='litre level', ax=ax, secondary_y=False)
    ax.set_ylim([0, df_for_plot['litre level'].max() * 1.2])
    ax.legend(loc='best')
    df_for_plot.plot(kind='line', y='price', ax=ax, secondary_y=True)
    ax.right_ax.set_ylim([1, df_for_plot['price'].max() * 1.2])
    plt.ylabel('Price')
    plt.show()


def price_for_day(day):
    """Period is roughly 30 days between 1.75 and 1.25"""
    sign = day // 30 % 2 * 2 - 1
    return 1.50 - 0.25 * sign * math.cos(day * math.pi / 30)


def plot_price_for_day():
    # Test price function by plotting
    lst_x = range(120)
    lst_y = [price_for_day(x) for x in lst_x]
    plt.plot(lst_x, lst_y)
    plt.ylim([0, 2])
    plt.show()


# Demo 1  - see help(pandas.DataFrame.groupby)
# Create a function which takes a row from dataframe and finds the column 'Max km/h' and converts to m/s
# Create a dataframe of birds and their maximum speeds etc
# Create a new column in dataframe by applying previous function
# Group by animal and find the mean of columns 'Max m/s' and 'Colours'
def mps_from_kmph(row):
    """Returns speed in m/s given speed in km/h"""
    logging.info(f"row passed to mps_from_kmph \n{row}")
    logging.info(f"row.name = {row.name}")
    return row['Max km/h'] * 1000 / 3600


if challenge == 0:
    df_demo = pd.DataFrame({'Animal': ['Falcon', 'Falcon', 'Parrot', 'Parrot'],
                            'Max km/h': [380., 370., 24., 26.],
                            'Colours': [3, 4, 20, 30],
                            'Name': ['Fred', 'Finn', 'Percy', 'Peter']})
    print(df_demo)
    df_demo['Max m/s'] = df_demo.apply(mps_from_kmph, axis='columns')
    df_demo_mean = df_demo.groupby(['Animal']).mean()
    df_demo_2col = df_demo_mean[['Max m/s', 'Colours']]
    print(df_demo_2col)

# Challenge 1: Read electricity production (MW) from a solar farm for a month and find the average for each hour of the
# day plotting the results on a chart
# i.e. the value for 9am is the average from 9am to 10am over all days in the month
# Emerald solar farm data for January is http://nemlog.com.au/api/unit/EMERASF1/20200101/20200131/csv
# Steps:
#     Read CSV file into dataframe or url using pandas.read_csv()
#     Convert SETTLEMENTDATE to datetime and set as index column
#     Add another column to dataframe storing the hour of the day (use .hour property of datetime objects)
#     Group results by hour and find the average of SCADAVALUE and RRP
#     Plot results using provided function plot_by_hour(df)
# url = "http://nemlog.com.au/api/unit/EMERASF1/20200101/20200131/csv"
url = "unit_emerasf1_20200101_20200131.csv"
df = pd.read_csv(url, parse_dates=['SETTLEMENTDATE'], index_col='SETTLEMENTDATE')
df['hour'] = df.apply(lambda row: row.name.hour, axis=1)
if challenge == 1:
    df_by_hour = df.groupby('hour')[['SCADAVALUE', 'RRP']].mean()
    plot_by_hour(df_by_hour)


# Demo 2: Use Object oriented programming to model driving a car and deciding when to fill up with fuel
#     Create a class Car to model the behaviour of the car
#         Initialising instance of Car will require litre_capacity (60L), litre_per_100_km (8 L/100km), price_break ($1.4/L)
#         Car will need instance variables to track fuel stored (litre_level) and cost of buying fuel (aud_cost).
#         Car will need a method which decides how much fuel to buy given the current price and how far travelled since last decision (litre_decision(price, km))
#         Method litre_decision(price, km) will check that fuel level does not reduce below 0 otherwise need fuel delivered to car at $50 per 10L
#         Calling litre_decision(price, km) will update litre_level and aud_cost and return the volume (litre) bought
#     Write a Python function to calculate fuel cost given the decision break price
#         Create an instance of type Car
#         Loop through dataframe (using idx as loop variable)
#             get litre bought by car
#             Store fuel bought in df.at[idx, 'litre'], fuel level before purchase in df.at[idx, 'litre level'], level in df.at[idx, 'mwh_level']
#         Print final cost of fuel
#         Plot results using provided function plot_car(df)
class Car:
    def __init__(self, litre_capacity=60, price_break=1.45, litre_per_100_km=7):
        self.litre_capacity = litre_capacity
        self.price_break = price_break
        self.litre_per_100_km = litre_per_100_km
        self.litre_level = litre_capacity  # start with full tank
        self.aud_cost = 0

    def litre_decision(self, price, km):
        self.litre_level -= km * self.litre_per_100_km / 100
        litre_delivered = 0
        while self.litre_level < 0:
            litre_delivered += 10
            self.litre_level += 10
            self.aud_cost += 50  # Cost $50 per 10L if run out and need to have it delivered
        if price <= self.price_break:
            litre_self_serve = self.litre_capacity - self.litre_level
            self.litre_level = self.litre_capacity
            self.aud_cost += litre_self_serve * price
        else:
            litre_self_serve = 0
        return litre_self_serve + litre_delivered


# check price_for_day() function
if challenge == 1:
    plot_price_for_day()
    pass
# Create dataframe
lst_km_to_fuel = [random.randrange(20, 200) for i in range(100)]
df_demo_car = pd.DataFrame({'km to fuel': lst_km_to_fuel})
df_demo_car['km travelled'] = df_demo_car['km to fuel'].cumsum()
# assume we travel 40km per day.
df_demo_car['price'] = df_demo_car.apply(lambda row: price_for_day(row['km travelled'] / 40), axis='columns')
df_demo_car.set_index('km travelled', inplace=True)


def cost_for_car_fuel(price_break):
    car = Car(litre_capacity=60, price_break=price_break, litre_per_100_km=7)
    for idx in df_demo_car.index:
        df_demo_car.at[idx, 'litre'] = car.litre_decision(price=df_demo_car.at[idx, 'price'], km=df_demo_car.at[idx, 'km to fuel'])
        df_demo_car.at[idx, 'litre level'] = car.litre_level - df_demo_car.at[idx, 'litre']  # level before filling
    print(f"Using price break point ${price_break:7.4f} the total cost to fill car is ${car.aud_cost:5,.2f}")
    return car.aud_cost


# Find cost if purchase fuel when 1.40 or cheaper
if challenge == 1:
    cost_for_car_fuel(1.4)
    print(df_demo_car)
    plot_car(df_demo_car)


# Challenge 2: We want to install a Tesla battery like the one installed in South Australia to smooth the electricity
# output from renewable energy sources. Storage capacity 129 MWh, power limit from or to grid is 100 MW.
# Assume 90% efficiency (100 MW to battery for one hour increases storage level by 90 MWh. 100 MW from battery for one hour reduces storage level by 100 MWh)
# Battery to discharge at power limit when sell price > $ 60 /MWh of stored energy
# Battery to charge at power limit when buy price < $ 60 /MWh of stored energy
# Steps:
#     Create a class Battery to model the behaviour of the battery
#         Initialising instance of Battery will require mwh_capacity (129 MWh), mw_limit (100 MW), efficiency(0.9), rrp_break ($60/MWh)
#         Battery will need instance variables to track energy stored (mwh_level) and value of buy/sell transactions (aud_profit).
#         Battery will need a method which decides how much power to buy or sell for 5 minutes given the current price (mw_decision(rrp))
#         Method mw_decision(rrp) will check that battery level does not reduce below 0 or exceed mwh_capacity
#         Calling mw_decision(rrp) will update mwh_level and aud_profit and return the power (MW) bought (+ve) or sold (-ve)
#     Write a Python script to run model for all data in dataframe
#         Create an instance of type Battery
#         Loop through dataframe (using idx as loop variable)
#             get MW bought or sold by battery
#             Store buy price in df.at[idx, 'buy'], sell price in df.at[idx, 'sell'], level in df.at[idx, 'mwh_level']
#         Print final profit of battery
#         Plot results using provided function plot_battery(df)
class Battery:
    def __init__(self, mwh_capacity, mw_limit, efficiency=0.9, rrp_break=62.45, rrp_factor=1000000):
        self.mwh_capacity = mwh_capacity
        self.rrp_break = rrp_break
        self.rrp_factor = rrp_factor  # Challenge 4
        self.mw_limit = mw_limit
        self.mwh_level = 0
        self.aud_profit = 0
        self.efficiency = efficiency

    def mw_decision(self, rrp):
        if rrp < self.rrp_break * self.efficiency:
            # buy
            if challenge < 4:
                mw = min(self.mw_limit, (self.mwh_capacity - self.mwh_level) * 12 / self.efficiency)  # +ve means buy
            else:
                mw = min(self.mw_limit, (self.mwh_capacity - self.mwh_level) * 12 / self.efficiency, -(rrp - self.rrp_break * self.efficiency) / self.rrp_break * self.rrp_factor)  # +ve means buy  # Challenge 4
            self.mwh_level += mw * self.efficiency / 12
        elif rrp > self.rrp_break:
            # sell
            if challenge < 4:
                mw = -min(self.mw_limit, self.mwh_level * 12)  # -ve means sell  # Challenge 2 and 3
            else:
                mw = -min(self.mw_limit, self.mwh_level * 12, (rrp - self.rrp_break) / self.rrp_break * self.rrp_factor)  # -ve means sell  # Challenge 4
            self.mwh_level += mw / 12
        else:
            # don't buy or sell
            mw = 0
        self.aud_profit -= mw * rrp / 12
        return mw


def profit_for_rrp_break(rrp_break, rrp_factor=None):
    # Tesla battery for South Australia. Cost ~ AUD 90 million + maintenance AUD 5 million per year, capacity 129 MWh, throughput 100 MW
    if rrp_factor is None:
        # Challenge 2 and 3
        battery = Battery(mwh_capacity=129, mw_limit=50, rrp_break=rrp_break)
    else:
        # Challenge 4
        battery = Battery(mwh_capacity=129, mw_limit=100, rrp_break=rrp_break, rrp_factor=rrp_factor)
    for idx in df.index:
        mw_buy_or_sell = battery.mw_decision(df.at[idx, 'RRP'])
        if mw_buy_or_sell < 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, df.at[idx, 'RRP']
        elif mw_buy_or_sell > 0:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = df.at[idx, 'RRP'], None
        else:
            df.at[idx, 'buy'], df.at[idx, 'sell'] = None, None
        df.at[idx, 'aud_profit'] = -mw_buy_or_sell * df.at[idx, 'RRP'] / 12
        df.at[idx, 'mwh_level'] = battery.mwh_level
    if rrp_factor is None:
        # Challenge 2 and 3
        print(f"RRP break point ${rrp_break:5,.2f}. Profit ${battery.aud_profit:10,.2f}  ")
    else:
        # Challenge 4
        print(f"RRP break point ${rrp_break:5,.2f}, factor ${rrp_factor:5,.2f}. Profit ${battery.aud_profit:12,.2f}  ")
    # loss is same as negative profit
    return battery.aud_profit + rrp_break * battery.mwh_level


if challenge == 2:
    profit_for_rrp_break(62.45)
    plot_battery(df_for_plot=df)


# Demo 3: Find the optimum price break point using scipy.optimize.minimize(fun, x0, method, options)
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
def loss_for_price_break(x):
    return cost_for_car_fuel(price_break=x[0])


def optimise_car_3():
    result = minimize(loss_for_price_break, x0=np.array([1.4]), method='Nelder-Mead', options={'disp': True, 'xatol': 0.01, 'fatol': 1})
    print(f"Optimisation result for car purchasing fuel {result}")


if challenge == 2:
    optimise_car_3()
    plot_car(df_demo_car)


# Challenge 3: Find the optimum rrp break point using scipy.optimize.minimize(fun, x0, method, options)
def loss_function_for_rrp_break(x):
    return -profit_for_rrp_break(rrp_break=x[0])


def optimise_battery_3():
    result = minimize(loss_function_for_rrp_break, x0=np.array([50]), method='Nelder-Mead', options={'disp': True, 'xatol': 0.1, 'fatol': 10})
    print(f"Optimisation result {result}")


if challenge == 3:
    optimise_battery_3()
    plot_battery(df_for_plot=df)


# Challenge 4: Modify mw_decision(rrp) so that if rrp is only just higher than rrp only a little bit of electricity is
# sold but if rrp is a lot higher then it is sold at maximum rate.
#     Optimise how much to sell based on how much above rrp
def loss_function_for_rrp_break_4(x):
    return -profit_for_rrp_break(rrp_break=x[0], rrp_factor=x[1])


def optimise_battery_4():
    result = minimize(loss_function_for_rrp_break_4, x0=np.array([62, 50]), method='Nelder-Mead', options={'disp': True, 'xatol': 0.1, 'fatol': 10})
    print(f"Optimisation result {result}")


if challenge == 4:
    optimise_battery_4()
    plot_battery(df_for_plot=df)
