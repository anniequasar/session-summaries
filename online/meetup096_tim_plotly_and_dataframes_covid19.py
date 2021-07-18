#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MeetUp 096 - Beginners Python and Machine Learning - 23 Feb 2021 - Charting COVID-19 doubling rate with plotly

This continues on from MeetUp 095.

Colab:   https://colab.research.google.com/drive/1X2BNBYuks6pvW2JntcX7HmRTemeLJjrh
Youtube: https://youtu.be/sF_VOxj42b4
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/276491844/
Github:  https://github.com/anniequasar/session-summaries/tree/master/online

Learning objectives:
- pandas DataFrames and Series
- plotly.py


To install third party library requirements

    pip install numpy pandas plotly

@author D Tim Cummings
"""

# Colab only: Google colab uses an old version of plotly. We need 4.5 or later. Uncomment following line in colab
# !pip list | grep plotly

# Colab only: Uncomment following line in colab to upgrade for session
# !pip install --upgrade plotly

import math
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px

# Load data from the covid-19 data set from Johns Hopkins site on github
df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
print(f"DataFrame downloaded from Johns Hopkins confirmed cases\n{df_confirmed.head()=}")

# List the states in alphabetical order. Need to drop NaN because otherwise sort will break
ar_state = df_confirmed['Province/State'].dropna().unique()
ar_state.sort()
print(f"{type(ar_state)=}")
print(f"{ar_state=}")

# Challenge 1: Print the list of countries in alphabetical order with no repeats

# Solution 1: Don't need to dropna because there are none. No harm if left in apart from slightly slower
ar_country = df_confirmed['Country/Region'].unique()
ar_country.sort()
print(f"Solution 1: {ar_country=}")

# Filtering DataFrames

# First set some options on displaying DataFrames
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

# how to filter by country
print(f'Filter by country: {df_confirmed[df_confirmed["Country/Region"]=="Australia"]=}')

# how to filter by state
print(f'Filter by state: {df_confirmed[df_confirmed["Province/State"] == "Queensland"]=}')

# how to filter by state and country should two countries have state with same name
print(f'Filter by state and country: {df_confirmed[(df_confirmed["Province/State"]=="Queensland") & (df_confirmed["Country/Region"]=="Australia")]=}')

# Challenge 2: define a function which takes 3 arguments, df, country, state and 
# will return the dataframe filtered by country, by state or by country and state


# Solution 2
def df_for_location(df, country=None, state=None):
    filt = [True] * df.shape[0]
    if country:
        filt = filt & (df["Country/Region"] == country)
    if state:
        filt = filt & (df["Province/State"] == state)
    return df[filt]


# check it works
print(f'Solution 2: {df_for_location(df_confirmed, country="New Zealand")=}')

df_confirmed_for_location = df_for_location(df_confirmed, country="Australia")
print(f'{df_confirmed_for_location=}')

# sum the dataframe along the index axis (sum iterating over index) and return a series
total = df_confirmed_for_location.sum(axis="index")

print(f'{type(total)=}')
print(f'total=\n{total}')

# Don't want the first four rows so can slice
series_sum = total[4:]
print(f'series_sum=\n{series_sum}')

# index is currently str but would prefer datetime. Value is float but would like int
series_sum.index = pd.to_datetime(series_sum.index)
series_sum = series_sum.astype('int64')
print(f'df_confirmed_for_location.T[7:]=\n{df_confirmed_for_location.T[7:]}')
print(f'series_sum[3:]=\n{series_sum[3:]}')

# Challenge 3: define a function which returns a series of values for a given df and country and/or state 
# Index for series should be a DateTimeIndex


# Solution 3
def series_sum_for_location(df, country=None, state=None):
    series = df_for_location(df=df, state=state, country=country).sum(axis="index")[4:].astype('int64')
    series.index = pd.to_datetime(series.index)
    return series


# check it works
print(f'Solution 3: {series_sum_for_location(df_confirmed, country="Australia")=}')

# Challenge 4: Define a function location_name which takes country and/or state and 
# returns a name for that location
# location_name(country="Australia") should return "Australia"
# location_name(state="Queensland") should return "Queensland"
# location_name() should return "everywhere"
# location_name(country="Australia", state="Queensland") should return "Queensland - Australia"


# Solution 4:
def location_name(country=None, state=None):
    locations = []
    if state:
        locations.append(state)
    if country:
        locations.append(country)
    return " - ".join(locations) if len(locations) > 0 else "everywhere"


# We can use function specification to test we wrote function correctly
assert location_name(country="Australia") == "Australia"
assert location_name(state="Queensland") == "Queensland"
assert location_name() == "everywhere"
assert location_name(country="Australia", state="Queensland") == "Queensland - Australia"

# To get the index for values greater than a starting value (in this case 100) use a filter
series_sum = series_sum_for_location(df_confirmed, country="Australia")
print(f'series_sum > 100=\n{series_sum > 100}')
print(f'series_sum.index[series_sum >= 100]=\n{series_sum.index[series_sum >= 100]}')

# To convert to dataframe and label the data column 'confirmed'
df_sum = pd.DataFrame(series_sum, columns=['confirmed'])
print(f"DataFrame construction with column called 'confirmed'\n{df_sum}")

# Now we want to calculate the number of active cases. There is data for recovered and deaths but it is not maintained as accurately as confirmed
# Instead we are going to calculate active cases as confirmed cases as of today less confirmed cases as of 28 days ago
df_sum['confirmed-lag'] = df_sum['confirmed'].shift(28, fill_value=0)
print(f"Add column called 'confirmed-lag'\n{df_sum}")

df_sum['active'] = df_sum['confirmed'] - df_sum['confirmed-lag']
print(f"Add column called 'active'\n{df_sum}")

# Challenge 5: Find the date the number of active cases exceeded 100 and what the count was on that day

# Solution 5
idx_start = df_sum.index[df_sum['active'] >= 100][0]
num_start_actual = df_sum.at[idx_start, 'active']
print(f"Solution 5: {idx_start=} {num_start_actual=}")

# Challenge 6: Create a DataFrame which starts when current is >= 100

print("Solution 6: Slice the Dataframe to only include those records starting when first reached 100")
df_plot = df_sum[df_sum["active"] >= 100]  # could use filter
print(f"df_sum[df_sum['active'] >= 100]\n{df_plot}")  
df_plot = df_sum.loc[idx_start:]  # or could use loc
print(f"df_sum.loc[idx_start:]\n{df_plot}")  
i_row = df_sum.index.get_loc(idx_start)  # or could use iloc if we knew the row number
df_plot = df_sum.iloc[i_row:]  
print(f"i_row from index={i_row} df_sum.iloc[i_row:]\n{df_plot}")  
i_row = (df_sum["active"] < 100).sum()  # reverse the filter and then we can sum Trues (True == 1)
df_plot = df_sum.iloc[i_row:]  
print(f"i_row from bools={i_row} df_sum.iloc[i_row:]\n{df_plot}") 

# Repeat the exercise starting at 200 to see why we can't use filters for this challenge

# Challenge 7: Write a function which takes dataframe of confirmed cases, 
# country and state and returns dataframe of active cases


# Solution 7:
def df_active_for_location(df, country=None, state=None):
    series = series_sum_for_location(df, country=country, state=state)
    df_active = pd.DataFrame(series, columns=['confirmed'])
    df_active['confirmed-lag'] = df_active['confirmed'].shift(28, fill_value=0)
    df_active['active'] = df_active['confirmed'] - df_active['confirmed-lag']
    return df_active


print(f'Solution 7:df_active_for_location(df_confirmed, country="US")=\n{df_active_for_location(df_confirmed, country="US")}')

# Challenge 8: Write a function to plot those numbers after starting count reached. Default starting count=100
# Advanced: plot count on a logarithmic scale


# Solution 8:
def plot_for_location(df, country=None, state=None, num_start=100):
    df_active = df_active_for_location(df, country, state)
    idx_for_start = df_active.index[df_active['active'] >= num_start][0]

    df = df_active.loc[idx_for_start:]
    location = location_name(country=country, state=state)
    fig = go.Figure(
        data=[go.Scatter(x=df.index, y=df['active'], name=location, showlegend=True, mode="lines")],
        layout=go.Layout(
            title=go.layout.Title(text=f"Solution 8: Active cases for {location} starting from {num_start}"),
        )
    )
    fig.update_yaxes(type='linear')
    return fig


plot_for_location(df_confirmed, country="United Kingdom").show()

# arithmetic on numpy arrays or pandas dataframe columns
lst = [234, 345, 46, 876, 43, 83, 44]
ar = np.array(lst)
try:
    print(f"lst + 5 = {lst + 5}")
except TypeError as te:
    print("lst + 5", te)
try:
    print(f"ar + 5 = {ar + 5}")
except TypeError as te:
    print("ar + 5", te)

print(f'{ar * 3=}')

# Numpy can automatically override operators but not functions. 
# It provides its own functions so you can manually override
try:
    print(f"math.log10(ar)={math.log10(ar)}")
except TypeError as te:
    print(f"math.log10(ar)", te)
try:
    print(f"np.log10(ar)={np.log10(ar)}")
except TypeError as te:
    print(f"np.log10(ar)", te)

r"""# Challenge 9: Calculate number of days to double using formula (latex formatted)

$days_{double} = \frac {days_{average}}{\log_{2}(\frac{active_{now}}{active_{then}})}$

where 

- $days_{double}$ = number of days for active cases to double
- $days_{average}$ = number of days to average over
- $active_{now}$ = number of active cases now
- $active_{then}$ = number of active cases $days_{average}$ days ago
"""

# Solution 9:
days_average = 5
df_sum['active-lag'] = df_sum['active'].shift(days_average, fill_value=0)
df_sum['days-double'] = days_average / np.log2(df_sum['active'] / df_sum['active-lag'])
df_sum['days-double'].clip(lower=-100, upper=100, axis='index', inplace=True)
px.line(df_sum, y='days-double').show()
# Positive is days to double, negative is days to halve.

df_sum['days-double'] = days_average / np.log2(df_sum['active'] / df_sum['active-lag'])  # remove the clip
df_sum['days-double-inverse'] = 1 / df_sum['days-double']
px.line(df_sum, y='days-double-inverse', title='Solution 9: higher is worse').show()

# Challenge 10: Create a function taking country and state and minimum active cases to start, and number of days to average over and plot days to double inverse
# Advanced: Plot at same time as count using plotly subplots


# Solution 10
def df_plot_doubling_for_location(df, country=None, state=None, num_start=50, averaged_days=3):
    df_active = df_active_for_location(df, country, state)
    df_active['active-lag'] = df_active['active'].shift(averaged_days, fill_value=0)
    df_to_plot = df_active[df_active['active'] >= num_start].copy()  # otherwise get an error when setting later
    df_to_plot['doubling days'] = averaged_days / np.log2(df_to_plot['active'] / df_to_plot['active-lag'])
    df_to_plot['inverse of doubling days'] = 1 / df_to_plot['doubling days']
    df_to_plot['doubling days'].clip(lower=-100, upper=100, axis="index", inplace=True)
    return df_to_plot


def plot_doubling_for_location(df, country=None, state=None, num_start=50, averaged_days=3):
    df_to_plot = df_plot_doubling_for_location(df, country, state, num_start, averaged_days)
    location = location_name(country=country, state=state)
    fig = go.Figure(
        data=[go.Scatter(x=df_to_plot.index, y=df_to_plot['inverse of doubling days'], name=location, showlegend=True, mode="lines")],
        layout=go.Layout(
            title=go.layout.Title(text=f"Solution 10: Active cases for {location} starting from {num_start}. Inverse of days to double averaged over {averaged_days} days"),
        )
    )
    return fig


plot_doubling_for_location(df_confirmed, country="Australia", averaged_days=15).show()

# Can superimpose traces
fig1 = plot_doubling_for_location(df_confirmed, country="Australia", averaged_days=15)
df_plot_uk = df_plot_doubling_for_location(df_confirmed, country="United Kingdom", averaged_days=15)
fig1.add_trace(go.Scatter(x=df_plot_uk.index, y=df_plot_uk['inverse of doubling days'], mode='lines', name="United Kingdom"))
fig1.update(layout_title_text='Compare two countries for inverse of days to double for active cases')
fig1.show()


# Advanced solution to challenge 10
def plot_for_location(df, country=None, state=None, num_start=100, averaged_days=3):
    df_to_plot = df_plot_doubling_for_location(df, country, state, num_start, averaged_days)
    location = location_name(country=country, state=state)
    fig = plotly.subplots.make_subplots(
        rows=3, cols=1, shared_xaxes=True, 
        specs=[[{"rowspan": 2}], [None], [{}]],
        subplot_titles=["Active cases on a logarithmic scale",  
                        f"Inverse days to double averaged over last {averaged_days} days. Higher is worse"]
    )
    fig.update_layout(
        title_text=f"Advanced solution 10: Active cases {location} starting from {num_start}",
        height=600
    )
    fig.add_trace(
        go.Scatter(x=df_to_plot.index, y=df_to_plot['active'], mode='lines', name=location),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df_to_plot.index, y=df_to_plot['inverse of doubling days'], mode='lines', showlegend=False),
        row=3, col=1
    )
    fig.update_yaxes(title_text='Cases', type='log', row=1, col=1)
    idx_at_start = df_to_plot.index[0]
    idx_end = df_to_plot.index[-1]
    duration = (idx_end - idx_at_start).days
    doubler = 6  # draw a line for doubling every 6 days
    num_at_start_actual = df_to_plot.loc[idx_at_start, 'active']
    num_at_end = int(num_at_start_actual * 2 ** (duration / doubler))
    fig.add_trace(
        go.Scatter(x=[idx_at_start, idx_end], y=[num_at_start_actual, num_at_end], mode='lines', name=f'every {doubler} days'),
        row=1, col=1
    )
    return fig


plot_for_location(df_confirmed, country="United Kingdom").show()

# Challenge 11: Add lines on log chart for doubling every 2, 3, 4, 5 days


# Solution 11
def plot_for_location(df, country=None, state=None, num_start=100, averaged_days=3):
    df_to_plot = df_plot_doubling_for_location(df, country, state, num_start, averaged_days)
    location = location_name(country=country, state=state)
    fig = plotly.subplots.make_subplots(
        rows=3, cols=1, shared_xaxes=True, 
        specs=[[{"rowspan": 2}], [None], [{}]],
        subplot_titles=["Active cases on a logarithmic scale",  
                        f"Inverse days to double averaged over last {averaged_days} days. Higher is worse"]
    )
    fig.update_layout(
        title_text=f"Solution 11: Active cases {location} starting from {num_start}",
        height=600
    )
    fig.add_trace(
        go.Scatter(x=df_to_plot.index, y=df_to_plot['active'], mode='lines', name=location),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df_to_plot.index, y=df_to_plot['inverse of doubling days'], mode='lines', showlegend=False),
        row=3, col=1
    )
    fig.update_yaxes(title_text='Cases', type='log', row=1, col=1)
    idx_at_start = df_to_plot.index[0]
    idx_end = df_to_plot.index[-1]
    duration = (idx_end - idx_at_start).days

    num_at_start_actual = df_to_plot.loc[idx_at_start, 'active']
    for doubler in (2, 3, 4, 5, 6):  # draw a line for doubling every 6 days
        num_end = int(num_at_start_actual * 2 ** (duration / doubler))
        fig.add_trace(
            go.Scatter(x=[idx_at_start, idx_end], y=[num_at_start_actual, num_end], mode='lines', name=f'every {doubler} days'),
            row=1, col=1
        )
    return fig


plot_for_location(df_confirmed, country="United Kingdom", num_start=100).show()
