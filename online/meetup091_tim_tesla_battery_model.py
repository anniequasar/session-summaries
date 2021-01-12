#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MeetUp 091 - Beginners' Python and Machine Learning - 12 Jan 2021 - Model Tesla South Australian battery

Youtube: https://youtu.be/yn0k-nLjvR8
Colab:   https://colab.research.google.com/drive/1DZzbdOuG7WZE3xfE8j08mjMcr6dTUIhn
Github:  https://github.com/anniequasar/session-summaries/tree/master/online
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/275600676/

Learning objectives:
- Object oriented program (class)
- pandas DataFrames

@author D Tim Cummings

Model to optimise operation of a South Australian style Tesla battery linked to a solar farm by buy and selling power to the grid

"""
# standard libraries
import logging

# third party libraries (included with Anaconda) - install with pip if you don't have Anaconda
import matplotlib.pyplot as plt  # pip install matplotlib
import pandas as pd  # pip install pandas

# Commented out IPython magic to ensure Python compatibility.
# Jupyter Notebooks used to need the following to show plots as part of the notebook
# %matplotlib inline

# Set logging level - levels are CRITICAL, ERROR, WARNING, INFO, DEBUG
logging.basicConfig(level=logging.INFO)
# logging.getLogger().setLevel(logging.INFO)

"""### Demo 1: Read electricity production (MW) from a solar farm for a month and summarise data for each hour of the day plotting the results on a chart
i.e. the value for 9am will be the average from 9am to 10am over all days in the month

Emerald solar farm data for December 2021 is http://nemlog.com.au/api/unit/EMERASF1/20201201/20201231/csv

Data can be retrieved from http://nemlog.com.au. See http://nemlog.com.au/nlog for examples
http://nemlog.com.au/nlog/qld-large-scale-solar-24-hour-and-cumulative-maximum-outputs-for-period-01-april-2017-to-20-august-2019/

- SETTLEMENTDATE is the date and time at the end of 5 minutes of production
- DUID is the unit ID for the solar farm, in this case EMERASF1
- RRP is the current electricity price on the grid for this region $/MWh (regional reference price)
- REGIONID is the location of the solar farm in this case QLD1
- SCADAVALUE is the electricity production from the solar farm MW

"""

# Locations for data on Internet and in file system
url = "http://nemlog.com.au/api/unit/EMERASF1/20201201/20201231/csv"
filename = "unit_emerasf1_20201201_20201231.csv"

# See what happens if file does not exist by uncommenting following line
# df = pd.read_csv(filename)

# Read URL and save result into a file for future use
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    logging.info(f"Demo 1: File {filename} not found so retrieving from Internet")
    df = pd.read_csv(url)
# Note that SETTLEMENTDATE is stored as a string object not a datetime64
logging.info("Demo 1: DataFrame after read_csv(url) or read_csv(filename)")
logging.info(f"Demo 1: df.info()={df.info()} (see console for actual output)")
logging.info(f"Demo 1: df.head()=\n{df.head()}")

# How to convert to datetime64. Could also specify a format="%Y-%m-%d %H:%M:%S" using strptime codes
df['SETTLEMENTDATE'] = pd.to_datetime(df['SETTLEMENTDATE'], format="%Y-%m-%d %H:%M:%S")
logging.info("Demo 1: DataFrame after pd.to_datetime")
df.info()

# Specify which column is going to be the index. (Also possible to set inplace=True to modify df in place)
df = df.set_index(['SETTLEMENTDATE'])
logging.info(f"Demo 1: DataFrame after df.set_index df.head()=\n{df.head()}")

# Can now save df as a csv file to cache results for next time
df.to_csv(filename)

# Another form of read_csv can parse dates and set the index at the same time
df = pd.read_csv(filename, parse_dates=['SETTLEMENTDATE'], index_col='SETTLEMENTDATE')
logging.info(f"Demo 1: After pd.read_csv(filename, parse_dates=['SETTLEMENTDATE'], index_col='SETTLEMENTDATE') df.head()=\n{df.head()}")
df.info()

# First values of month when solar panels are producing
logging.info(f"Demo 1: First values of month when solar panels are producing\ndf[df['SCADAVALUE'] > 0].head()=\n{df[df['SCADAVALUE'] > 0].head()}")

# Create a new column for hour of the day 
df['hour'] = df.index.hour  # alternatively = df.apply(lambda row: row.name.hour, axis=1)

# Filtering to find data at minutes=30 for every hour of first day
logging.info(f"Demo 1: First values of month when time is 30 minutes past hour\ndf[df.index.minute == 30].head(24)=\n{df[df.index.minute == 30].head(24)}")

# Find mean, min and max of solar production for each hour
df_by_hour_mw = df.groupby('hour')[['SCADAVALUE']].mean()
df_by_hour_mw.rename(columns={'SCADAVALUE': 'MW Mean'}, inplace=True)
df_by_hour_mw['MW Max'] = df.groupby('hour')[['SCADAVALUE']].max()
df_by_hour_mw['MW Min'] = df.groupby('hour')[['SCADAVALUE']].min()
df_by_hour_mw.plot()  # add semicolon to end to prevent display of superfluous output in Jupyter Notebooks
plt.show()

# Find mean, min and max of pricing $/MWh for each hour
df_by_hour_rrp = df.groupby('hour')[['RRP']].mean()
df_by_hour_rrp.rename(columns={'RRP': 'RRP Mean'}, inplace=True)
df_by_hour_rrp['RRP Max'] = df.groupby('hour')[['RRP']].max()
df_by_hour_rrp['RRP Min'] = df.groupby('hour')[['RRP']].min()
df_by_hour_rrp.plot()
plt.show()

# Find the mean of production and pricing through the month during each hour of the day
df_by_hour = df.groupby('hour')[['SCADAVALUE', 'RRP']].mean()
logging.info(f"Demo 1: Hourly averages are\ndf_by_hour=\n{df_by_hour}")
# Plotting on the same scale and single y axis
df_by_hour.plot()
plt.show()


def plot_by_hour(df_for_plot, title):
    """Demo of what can be achieved with matplotlib. Plots for each hour 0 - 23, SCADAVALUE and RRP"""
    ax = plt.gca()  # get current axis so that both plots are on same chart
    plt.xlabel('hour of day')
    plt.suptitle('Profile')
    plt.title(title)
    df_for_plot.plot(kind='line', y='SCADAVALUE', ax=ax, color='yellow')
    plt.ylabel('Average MW generation during hour')
    df_for_plot.plot(kind='line', y='RRP', ax=ax, secondary_y=True, color='red')
    ax.set_ylim([0, df_for_plot['SCADAVALUE'].max() * 1.1])
    ax.right_ax.set_ylim([0, df_for_plot['RRP'].max() * 1.1])
    ax.legend(loc='upper left')
    ax.right_ax.legend(loc='upper right')
    plt.ylabel('Average $/MWh during hour')
    plt.show()


# Use the provided function to plot
plot_by_hour(df_by_hour, "Emerald Solar Farm Average Production")

"""### Challenge 1: Read electricity production (MW) from a solar farm for a month and find the average for each hour of the day plotting the results on a chart

Use code already developed above. Delete and edit to achieve the following functionality.

Steps:
- Read CSV file or URL into dataframe using pandas.read_csv()
- Convert SETTLEMENTDATE to datetime and set as index column
- Add another column to dataframe storing the hour of the day
- Group results by hour and find the average of SCADAVALUE and RRP
- Plot results using provided function plot_by_hour(df, title)

"""
# Solution 1 
# Locations for data on Internet and in file system
url = "http://nemlog.com.au/api/unit/EMERASF1/20201201/20201231/csv"
filename = "unit_emerasf1_20201201_20201231.csv"
# Read URL and save result into a file for future use
try:
    df = pd.read_csv(filename, parse_dates=['SETTLEMENTDATE'], index_col='SETTLEMENTDATE')
except FileNotFoundError:
    logging.info(f"Solution 1: File {filename} not found so retrieving from Internet")
    df = pd.read_csv(filename, parse_dates=['SETTLEMENTDATE'], index_col='SETTLEMENTDATE')
    df.to_csv(filename)
# Create a new column for hour of the day 
df['hour'] = df.index.hour  # alternatively = df.apply(lambda row: row.name.hour, axis=1)
# Find the mean of production and pricing through the month during each hour of the day
df_by_hour = df.groupby('hour')[['SCADAVALUE', 'RRP']].mean()
logging.debug(f"Solution 1: Hourly averages are\ndf_by_hour=\n{df_by_hour}")
# Use the provided function to plot
plot_by_hour(df_by_hour, "Emerald Solar Farm Average Production")

# We want to install a Tesla battery like the one installed in South Australia to smooth the electricity
# output from renewable energy sources. Storage capacity 129 MWh, power limit from or to grid is 100 MW.
# Assume 90% efficiency (100 MW to battery for one hour increases storage level by 90 MWh. 100 MW from battery for one hour reduces storage level by 100 MWh)
# Battery to discharge at power limit when sell price > $ 60 /MWh of stored energy
# Battery to charge at power limit when buy price < $ 60 /MWh of stored energy
# Steps:
#     Create a class Battery to model the behaviour of the battery
#         Initialising instance of Battery will require mwh_capacity (129 MWh), mw_limit (100 MW), efficiency(0.9)
#         Battery will need instance variables to track energy stored (mwh_level) and value of buy/sell transactions (aud_profit).
#         Battery will need a method which decides how much power to buy or sell for 5 minutes given the current price (mw_decision(rrp))
#         Method mw_decision(rrp) will check that battery level does not reduce below 0 or exceed mwh_capacity
#         Calling mw_decision(rrp) will update mwh_level and aud_profit and return the power (MW) bought (+ve) or sold (-ve)
#     Write a Python script to run model for all data in dataframe
#         Create an instance of type Battery
#         Print final profit of battery


# Object oriented programming: We create a new data type which is a metaphor for a real object (in this case a battery)
# Variables with this data type are called instances of the class.
# An object has attributes (eg current storage level, capacity, charging limit, efficiency). These are stored in instance variables
# An object can do things (eg charge, discharge). These are defined in methods (functions)
class Battery:

    def __init__(self, mwh_capacity, mw_limit, efficiency=0.9):
        """
        __init__ is a specially named method which is called when creating a new instance of object
        self is the first parameter of any method. Examples of using self below to create instance attributes 
        other parameters are just like in normal functions
        """
        self.mwh_capacity = mwh_capacity
        self.mw_limit = mw_limit
        self.efficiency = efficiency
        self.mwh_level = 0
        self.aud_profit = 0
    
    def mwh_charge(self, duration_minutes):
        """other methods can have any function name. First parameter is still self"""
        # capacity left for charging. mwh is a local variable not an instance variable
        mwh = self.mwh_capacity - self.mwh_level
        # MWh if charging at maximum rate. mw_limit is at grid
        mwh_max = self.mw_limit * self.efficiency * duration_minutes / 60
        # clip the return value to [0, mwh_max]. Could also use numpy.clip
        mwh = min(max(mwh, 0), mwh_max)
        # adjust the battery level by the MWh to be stored in battery
        self.mwh_level += mwh
        mw = mwh / self.efficiency / duration_minutes * 60
        logging.debug(f"After charging at {mw:6.2f}MW for {duration_minutes}minutes, the battery level is {self.mwh_level:6.2f}MWh")
        # return the MWh purchased from the grid
        return mwh / self.efficiency

    # Challenge 2: Create a method on Battery class for discharging. All the efficiency losses are to be modelled to occur at charging
    # Solution 2:
    def mwh_discharge(self, duration_minutes):
        # capacity left for discharging
        mwh = self.mwh_level
        # MWh if discharging at maximum rate
        mwh_max = self.mw_limit * duration_minutes / 60
        # clip the return value to [0, mwh_max]. Could also use numpy.clip
        mwh = min(max(mwh, 0), mwh_max)
        # adjust the battery level
        self.mwh_level -= mwh
        # return the charge amount in MWh
        mw = mwh / duration_minutes * 60
        logging.debug(f"After discharging at {mw:6.2f}MW for {duration_minutes}minutes, the battery level is {self.mwh_level:6.2f}MWh")
        return mwh

    # Challenge 3: To class Battery add a method mwh_decide which takes parameters
    #   rrp = Regional Reference Price of grid from AEMO
    #   rrp_break = Effective decision price per MWh in storage.
    #   duration_minutes = length of time at that price
    # Above rrp_break battery will discharge. Below rrp_break battery will charge.
    # Because of efficiency losses there will be a range of grid prices where battery
    # will not charge or discharge
    # Store the running profit (sales - purchases) in Battery instance variable aud_profit
    # Returns the change in MWh on the grid by Battery operation
    # Solution 3:
    def mwh_decide(self, rrp, rrp_break, duration_minutes):
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


# Check Original Battery class works with method mwh_charge()
# temporarily change logging level
old_logging_level = logging.getLogger().level
logging.getLogger().setLevel(logging.DEBUG)

# Create a new object of type Battery. 
# Parameters are those for __init__ ignoring the first parameter. Next line equivalent to b = Battery(129, 100) 
b = Battery(mwh_capacity=129, mw_limit=100)
# Call a method on this instance of the Battery supplying the parameter duration_minutes
mwh_grid = b.mwh_charge(30)
logging.info(f"Electricity bought from the grid {mwh_grid:6.2f}MWh")
# Can also call the method this way. In this case self is assigned value of b
mwh_grid = Battery.mwh_charge(b, 30)
logging.info(f"Electricity bought from the grid {mwh_grid:6.2f}MWh")
# Named arguments can also be used
mwh_grid = b.mwh_charge(duration_minutes=30)
logging.info(f"Electricity bought from the grid {mwh_grid:6.2f}MWh")

logging.getLogger().setLevel(old_logging_level)


# Check Solution 2 works with method mwh_discharge()
logging.getLogger().setLevel(logging.DEBUG)
# Call a method on this instance of the Battery supplying the parameter duration_minutes
for _ in range(3):
    mwh_grid = b.mwh_discharge(30)
    logging.info(f"Electricity sold to the grid {mwh_grid:6.2f}MWh")

logging.getLogger().setLevel(old_logging_level)


# Check Solution 3 battery operation with some fluctuating prices.
logging.getLogger().setLevel(15)

for price in [30, 40, 50, 60, 70, 80, 90, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10]:
    b.mwh_decide(price, 60, 30)

logging.getLogger().setLevel(old_logging_level)

# Challenge 4: Use the data from nemlog to calculate the profit possible over a month
# Loop through dataframe prices 'RRP' and decide whether to buy/sell/hold and calculate profit

# Solution 4
price_break = 60

# Quick solution

# Optionally you can reset profit and storage level before running
# b.aud_profit = 0
# b.mwh_level = 0
for price in df['RRP']:
    b.mwh_decide(price, rrp_break=60, duration_minutes=5)
logging.info(f"RRP break point ${price_break:5,.2f}. Profit ${b.aud_profit:12,.2f}  ")

# Longer solution - saves data for later plotting
battery = Battery(129, 100)
for idx in df.index:
    mwh_buy_or_sell = battery.mwh_decide(df.at[idx, 'RRP'], rrp_break=price_break, duration_minutes=5)
    # Store results in DataFrame so can be plotted later
    if mwh_buy_or_sell > 0:
        df.at[idx, 'buy'], df.at[idx, 'sell'] = None, df.at[idx, 'RRP']
    elif mwh_buy_or_sell < 0:
        df.at[idx, 'buy'], df.at[idx, 'sell'] = df.at[idx, 'RRP'], None
    else:
        df.at[idx, 'buy'], df.at[idx, 'sell'] = None, None
    df.at[idx, 'aud_profit'] = -mwh_buy_or_sell * df.at[idx, 'RRP']
    df.at[idx, 'mwh_level'] = battery.mwh_level
# Log results
logging.info(f"RRP break point ${price_break:5,.2f}. Profit ${battery.aud_profit:12,.2f}  ")


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


plot_battery(df)
