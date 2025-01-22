r"""MeetUp 210 - Beginners' Python and Machine Learning - 11 Dec 2024 - pandas and polars

Learning objectives:
- Introduction to data handling with 2 dataframe libraries, pandas and polars

Links:
- Colab:   https://colab.research.google.com/drive/1jAG4QzzLHInMQrmiVfcR5j24HXj42xC1
- Youtube: https://youtu.be/wTL7pK5wtc8
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/304789652/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

Today we are introducing polars and comparing it to pandas for use in data science. We will collect data from an online API and store in a DataFrame. Then we will perform filtering, converting, calculating and pivoting the data.

Polars is a fast DataFrame library for Rust and Python using the Apache Arrow memory model. Pandas 2 now uses Apache Arrow also.

- https://pola.rs
- https://pandas.pydata.org

To prepare your python virtual environment

Linux or Mac or Windows bash

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U polars pandas altair requests numpy pyarrow matplotlib
```

Windows cmd

```cmd
py -m venv venv
venv\Scripts\Activate.bat
pip install -U polars pandas altair requests numpy pyarrow matplotlib
```

Other references

- https://docs.pola.rs/user-guide/migration/pandas/
- https://realpython.com/polars-python/
- https://medium.com/cuenex/pandas-2-0-vs-polars-the-ultimate-battle-a378eb75d6d1
"""

# How to determine pandas and polars version from the command line using grep with Extended regular expressions (Linux or Mac or Windows bash)
#   pip list | grep -E "polars|pandas"
# How to determine pandas and polars version from the command line using grep with Extended regular expressions (Windows cmd)
#   pip list
# If missing (Linux or Mac or Windows)
#   pip install polars
#   pip install pandas

# Start using pandas and polars by importing them. To save time typing 'pd' instead of 'pandas' use an import alias
import pandas as pd
import polars as pl

import time  # used for timing comparisons between polars and pandas

# Let's get some data from https://data.brisbane.qld.gov.au/explore/dataset/public-art/information/ and store it in a local files
# polars can't read directly from url while pandas can
# saving to file first is faster anyway for our purposes
url_art = 'https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/public-art/exports/csv?lang=en&timezone=Australia%2FBrisbane&use_labels=true&delimiter=%2C'
url_cyc = 'https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/bikeway-counts/exports/parquet?lang=en&timezone=Australia%2FBrisbane'
url_tfc = 'https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/traffic-management-key-corridor-monthly-performance-report/exports/parquet?lang=en&timezone=Australia%2FBrisbane'

import requests

# Download the file to a temporary location
response = requests.get(url_art)
art_filename = 'bcc_art.csv'
with open(art_filename, 'wb') as art_file:
    art_file.write(response.content)

response = requests.get(url_cyc)
cyc_filename = 'bcc_cyc.parquet'
with open(cyc_filename, 'wb') as cyc_file:
    cyc_file.write(response.content)

response = requests.get(url_tfc)
tfc_filename = 'bcc_tfc.parquet'
with open(tfc_filename, 'wb') as tfc_file:
    tfc_file.write(response.content)

# Check files created (Linux or Mac or Windows bash)
#   ls -l
# Check files created (Windows cmd)
#   dir

# pandas read_csv can read from filename or url
dfd_art = pd.read_csv(art_filename, encoding='utf-8')
# Look at the data
print(f"after pandas.read_csv, dfd_art is\n{dfd_art}\n")

# Polars has a read_csv method (which is eager) which can read from a filename but not url
dfl_art = pl.read_csv(art_filename, encoding='utf8')
# Look at the data. Notice that Polars dataframes do not have an index
# (My sample data has a column called 'Index' just to be confusing)
print(f"after polars.read_csv, dfl_art is\n{dfl_art}\n")

# Polars also has a scan_csv method (which is lazy, use lazy wherever possible)
# query can include filters and aggregation and sorting
dfl_bronze = pl.scan_csv(art_filename).filter(pl.col('Material') == 'bronze').collect()
print(f"after polars.scan_csv, dfl_bronze is\n{dfl_bronze}\n")

# Read cycle data in parquet format as both pandas and polars dataframes
dfd_cyc = pd.read_parquet(cyc_filename)
dfl_cyc = pl.read_parquet(cyc_filename)
# Look at the data
print(f"after pandas.read_parquet, dfd_cyc is\n{dfd_cyc}\n")


# For our pandas dataframe let us use the BCC index as our index.
# Will make it easier when comparing loc and iloc
dfd_art = dfd_art.set_index("Index")
print(f"after pandas set_index to 'Index', dfd_art is\n{dfd_art}\n")


# In pandas, DataFrames are a two dimensional array of data.
# Series are a one dimensional array of data. Each column in a DataFrame can be used a Series
# Use [] notation with name of column to isolate just one column
sd = dfd_art['Item title']
print(f"dfd_art is a {type(dfd_art)} and sd is a {type(sd)}")

# A series has an index as well as a column of values
print(f"Series from pandas DataFrame has index and column of data. sd is\n{sd}\n")

# In polars, DataFrames are a two dimensional array of data.
# Series are a one dimensional array of data. Each column in a DataFrame can be used a Series
# Use [] notation with name of column to isolate just one column
sl = dfl_art['Item title']
print(f"After using polars [] notation to get sl, dfl_art is a {type(dfl_art)} and sl is a {type(sl)}")

# A polars series doesn't have an index
print(f"After using polars [] notation to get sl without an index, sl is\n{sl}\n")

# Better to select column using expression API. Returns a one column DataFrame rather than a Series
dfl_title = dfl_art.select('Item title')
print(f"After using polars select() dfl_art is a {type(dfl_art)} and dfl_title is a {type(dfl_title)}")

print(f"After using polars select() dfl_title is\n{dfl_title}\n")

# To get a sub pd.DataFrame use a list of column names
print(f"Pandas dfd_art[['Item title', 'Latitude', 'Longitude']] is\n{dfd_art[['Item title', 'Latitude', 'Longitude']]}\n")

# To get a sub pl.DataFrame use a list of column names
print(f"Polars dfl_art[['Item title', 'Latitude', 'Longitude']] is\n{dfl_art[['Item title', 'Latitude', 'Longitude']]}\n")

# However a better method is to use the expression API
print(f"Polars dfl_art.select(['Item title', 'Latitude', 'Longitude']) is\n{dfl_art.select(['Item title', 'Latitude', 'Longitude'])}\n")

# Pandas: matplotlib is required for .plot. Already installed in google colab
      
dfd_art.plot(kind='scatter', x='Longitude', y='Latitude', s=7, alpha=.8);

# Polars: altair>=5.4.0 is required for `.plot`.
# Google colab version is 4.2.2 which needs to be upgraded
#   pip list | grep altair
#   pip install -U altair
# May need to restart session if using google colab and you had already referred to altair

# Polars syntax different from pandas
# Polars plot implementation is considered unstable and could change without warning
# https://docs.pola.rs/api/python/stable/reference/dataframe/plot.html
# df.plot.point(**kwargs) is shorthand for alt.Chart(df).mark_point(tooltip=True).encode(**kwargs).interactive()
# (and plot.scatter is provided as an alias)
dfl_art.plot.point(x='Longitude', y='Latitude')

# By default altair starts axes at 0 so need to turn that off.
# Can also add tooltips easily
import altair as alt
dfl_art.plot.point(
    x=alt.X('Longitude', scale=alt.Scale(zero=False)),
    y=alt.Y('Latitude', scale=alt.Scale(zero=False)),
    tooltip=['Item title', 'Location', 'Material'])

# Selecting data in pandas

# pandas DataFrame via named index and columns
# df.at[row, col] => access one element
# df.loc[rows, cols] => access multiple elements

# Methods to access part of DataFrame via numbered index and columns
# df.iat[irow, icol] => access one element by zero based integer indexes
# df.iloc[irows, icols] => access multiple elements by zero based integer indexes

# Using .at to access a single data element in a pandas dataframe
print(f'Pandas - Using .at for single data element {dfd_art.at[5, "Item title"]=}')

# loc[index value, column name]
print(f'Pandas - Using .loc for single data element {dfd_art.loc[5, "Item title"]=}')
# Could also do slicing
# dfd_art.loc[4:6, "Item title":"Material"]
# Or selecting specific rows and columns
# dfd_art.loc[[4, 6], ["Item title", "Material"]]

# iat[index int position, column int position] is like iloc but only ever for a single data element
print(f'Pandas - Using .iat for single data element {dfd_art.iat[4, 0]=}')

# iloc[index int position, column int position]
print(f'Pandas - Using .iloc for single data element {dfd_art.iloc[4, 0]=}')
# Could also do slicing
# dfd_art.iloc[4:6, 0:3]
# Or selecting specific rows and columns
# dfd_art.iloc[[4, 6], [0, 1, 3]]

# Select column by name as series, and then select item in series with index value == 5
# This is less efficient than other methods
print(f'Pandas - Using [column name][index] for single data element {dfd_art["Item title"][5]=}')

# Filtering in pandas
# dfd_art[dfd_art['Material']=='aluminium']
# Setting data can trigger SettingWithCopyWarning
print(f'\nAbout to try setting a value but inadvertently doing it with copy\n')
dfd_art[dfd_art['Material']=='aluminium']['Item title list'] = 'A, Aluminium sculpture'
# No values actually changed
print(f"Pandas - After setting with copy there has actually been no change. dfd_art[dfd_art['Material']=='aluminium'].head() is still\n{dfd_art[dfd_art['Material']=='aluminium'].head()}\n")
# Correct way to do this would be
# dfd_art.loc[dfd_art['Material']=='aluminium', 'Item title list'] = 'A, Aluminium sculpture'
# dfd_art[dfd_art['Material']=='aluminium'].head()

"""# Selecting data in polars

As there is no index in Polars there is no `.loc` or `iloc` method in Polars - and there is also no `SettingWithCopyWarning` in Polars.

However, the best way to select data in Polars is to use the expression API.
"""

# Selecting a column in polars
# Equivalent to dfd_art['Item title'] or dfd_art.loc[:, 'Item title']

print(f'Polars - Using .select for column dfl_art.select("Item title") is\n{dfl_art.select("Item title")}\n')

# Similar to iloc, can select on rows and columns
# dfl_art[4:9, 1:3]

# dfl_art[4]



# Equivalent to using pandas DataFrame.loc to access a single data element
# dfd_art.loc[5, "Item title"]
print(f"Polars - Using .filter.select for single data element {dfl_art.filter(pl.col('Index')==5).select('Item title').item()=}\n")

# Equivalent to pandas DataFrame.loc with a sub DataFrame of rows
# Notice how slice includes ending row which is unusual in Python
# dfd_art.loc[2:5]
print(f'Polars - Using .filter.is_between for slicing dfl_art.filter(pl.col("Index").is_between(2, 5)) is\n{dfl_art.filter(pl.col("Index").is_between(2, 5))}\n')
# can specify is_between(2, 5, closed='left' or 'right' or 'none' or 'both' (default)) for inclusivity

# pandas column names are stored as an Index
print(f'Pandas - {dfd_art.columns=}\n')

# polars column names are stored in a list
print(f'Polars - {dfl_art.columns=}\n')

# Equivalent to pandas DataFrame.loc with slice on columns
# dfd_art.loc[:, 'Artist':'Material'].head()
# Polars needs column locations
# Because columns is just a list can use list method `index()`
start_idx = dfl_art.columns.index("Artist")
end_idx = dfl_art.columns.index("Material") + 1
# We can then use the iloc equivalent as we saw before to select a slice of columns
print(f'Polars equivalent to iloc dfl_art[:, start_idx:end_idx] is\n{dfl_art[:, start_idx:end_idx]}\n')

# If we want to use `select()`
print(f'Polars equivalent to iloc using select dfl_art.select(dfl_art.columns[start_idx:end_idx]) is\n{dfl_art.select(dfl_art.columns[start_idx:end_idx])}\n')

# In pandas can select columns using regex
print(f"Pandas filtering with regex dfd_cyc.filter(regex='^.*pedestrian$') is\n{dfd_cyc.filter(regex='^.*pedestrian$')}\n")

# In polars can select columns using regex
print(f"Polars filtering with regex dfl_cyc.select(pl.col('^.*pedestrian$')) is\n{dfl_cyc.select(pl.col('^.*pedestrian$'))}\n")

# Can use a list of bools on rows or columns to specify which ones to include
print(f'Pandas using list of bool to select columns\n{dfd_art.loc[:5, [True, True, False, True, False, False, False, False, False, False, False, False, False]]}\n')

# Can create a list of bools using an expression
print(f'Pandas creating list of bool {dfd_art.columns.str.contains(" ")=}\n')

# Put them together
print(f'Pandas using dynamic list of bool dfd_art.loc[:5, dfd_art.columns.str.contains(" ")] is\n{dfd_art.loc[:5, dfd_art.columns.str.contains(" ")]}\n')

# Could also use earlier expression df[[column names, ...]]
print(f'Pandas using df[[column names, ...]] dfd_art[dfd_art.columns[dfd_art.columns.str.contains(" ")]] is\n{dfd_art[dfd_art.columns[dfd_art.columns.str.contains(" ")]]}\n')

# More common to filter this way on rows
# Find art installed last year
print(f"Pandas filtering on rows dfd_art.loc[dfd_art['Installed']>=2023] is\n{dfd_art.loc[dfd_art['Installed']>=2023]}\n")

# Alternatively, filter on rows by supplying a list of booleans. (List of str filters on columns, List of int filters on index positions)
print(f"Pandas filtering on rows using bools dfd_art[dfd_art['Installed']>=2023] is\n{dfd_art[dfd_art['Installed']>=2023]}\n")

# Read traffic data from parquet file into pandas and check data types
dfd_tfc = pd.read_parquet(tfc_filename)
print("Pandas after read_parquet of traffic file. Check out the data types. dfd_tfc.info() returns")
dfd_tfc.info()

# object columns are str so need to convert to numeric (int or float) after reading
# Values of 'NA' are converted to NaN
# object_cols = ['year', 'avg_weekday_daily_traffic_veh_day', 'avg_veh_hr_am_peak_7_9am', 'avg_veh_hr_pm_peak_4_7pm', 'travel_time_am_peak_7_9am_seconds', 'travel_time_pm_peak_4_7pm_seconds']
object_cols = dfd_tfc.select_dtypes(include=['object']).columns
dfd_tfc[object_cols] = dfd_tfc[object_cols].apply(pd.to_numeric, errors='coerce')
# use column 'index' as pandas dataframe index and rename columns with spaces rather than underscores
# want to remove underscores so table display is more compact later
new_names = {k:k.replace('_', ' ') for k in dfd_tfc.columns}
dfd_tfc = dfd_tfc.set_index('index').rename(columns=new_names)
print("Pandas after converting str to number. dfd_tfc.info() returns")
dfd_tfc.info()
print(f"Pandas contents of dfd_tfc is now\n{dfd_tfc}\n")

# Polars can read from parquet file and do conversions as it reads
# additional filters could also be done at same time
# `strict=False` will convert 'NA' to null in data
dfl_tfc = (pl.scan_parquet(tfc_filename)
            .with_columns(pl.col(pl.String).cast(pl.Int64, strict=False))
            .rename(new_names)
            .collect())
print(f'Polars scan_parquet renaming and converting columns during scan dfl_tfc.schema is\n{dfl_tfc.schema}')

# Notice how columns can be Int64 with null in polars while in pandas they have to be float64 with Nan
print(f"Polars contents of dfl_tfc is now\n{dfl_tfc}\n")


# Perform arithmetical operation on a column and store the result
dfd_tfc['Volume per hour average'] = dfd_tfc['avg weekday daily traffic veh day'] / 24
print(f"Pandas contents of dfd_tfc after creating column 'Volume per hour average' is\n{dfd_tfc}\n")


# Calculations can be more complicated, although not every calculation can work
# Operators (+,-,*,/) are overriden so this works.
vol_am = 'avg veh hr am peak 7 9am'
vol_pm = 'avg veh hr pm peak 4 7pm'
tt_am = 'travel time am peak 7 9am seconds'
tt_pm = 'travel time pm peak 4 7pm seconds'
tt = 'Average TT Peak (seconds)'
dfd_tfc[tt] = (dfd_tfc[tt_am] * dfd_tfc[vol_am] + dfd_tfc[tt_pm] * dfd_tfc[vol_pm]) / (dfd_tfc[vol_am] + dfd_tfc[vol_pm])
print(f"Pandas contents of dfd_tfc after creating column '{tt}' is\n{dfd_tfc}\n")


# Use array of True and False to filter rows that contain Month of May
print(f"Pandas filtering on month of May dfd_tfc[dfd_tfc['month']==5] is\n{dfd_tfc[dfd_tfc['month']==5]}\n")

# Check data for Site ID 1 in May 2024
avg_tt = (4894 * 529 + 4557 * 407) / (4894 + 4557)

# Check using assert and filters
assert avg_tt == dfd_tfc.loc[(dfd_tfc['year'] == 2024) & (dfd_tfc['month'] == 5) & (dfd_tfc['site id'] == 1), tt].values[0]
print(f"Pandas data check one {avg_tt=}, {dfd_tfc.loc[(dfd_tfc['year'] == 2024) & (dfd_tfc['month'] == 5) & (dfd_tfc['site id'] == 1), tt]=}")

# Check using query instead of filters
assert avg_tt == dfd_tfc.query('year == 2024 & month == 5 & `site id` == 1')[tt].values[0]
print(f"Pandas data check two {avg_tt=}, {dfd_tfc.query('year == 2024 & month == 5 & `site id` == 1')[tt]=}")

# To call functions use numpy functions rather than Python functions
import math
# The following won't work
# dfd_tfc['sin index'] = math.sin(dfd_tfc.index * math.pi / 180)

# Use sin from numpy which can work on ndarrays
import numpy as np
dfd_tfc['sin index'] = np.sin(dfd_tfc.index * math.pi / 180)
print(f"Pandas contents of dfd_tfc after creating column 'sin index' is\n{dfd_tfc}\n")


# For datetime use pandas.to_datetime
dfd_tfc['Year Month'] = pd.to_datetime(dfd_tfc['year'].astype(str)+dfd_tfc['month'].astype(str).str.zfill(2), format=("%Y%m"))
print(f"Pandas contents of dfd_tfc after creating column 'Year Month' is\n{dfd_tfc}\n")

# Filter out anything earlier than 2021
dfd_tfc = dfd_tfc[dfd_tfc['year'] >= 2021]
print(f"Pandas contents of dfd_tfc after filtering out anything earlier than 2021 is\n{dfd_tfc}\n")


# Make the Site names more interesting than Site ID and take a portion of the DataFrame
dfd_tfc['Site Name'] = 'Site ' + dfd_tfc['site id'].astype(str).str.zfill(2)
dfd_tfc = dfd_tfc[['Site Name', 'Year Month', tt]]
# Sort chronologically
dfd_tfc = dfd_tfc.sort_values(['Year Month', 'Site Name'])
print(f"Pandas dfd_tfc after creating column 'Site Name' and sorting chronologically is\n{dfd_tfc.head(30)}\n")

# Now we can pivot data
dfd_pivot = dfd_tfc.pivot(index='Year Month', columns='Site Name', values=tt)
print(f"Pandas after pivoting on 'Site Name'\n{dfd_pivot}\n")

# In polars can use LazyFrame rather then DataFrame
# Here are all the steps we did on the pandas DataFrame starting from reading the parquet file
lf = pl.scan_parquet(tfc_filename)
lf = lf.with_columns(pl.col(pl.String).cast(pl.Int64, strict=False))
lf = lf.rename(new_names)
lf = lf.with_columns((pl.col('avg weekday daily traffic veh day') / 24).alias('Volume per hour average'))
lf = lf.with_columns(((pl.col(tt_am) * pl.col(vol_am) + pl.col(tt_pm) * pl.col(vol_pm)) / (pl.col(vol_am) + pl.col(vol_pm))).alias(tt))
lf = lf.with_columns((pl.col("index") * math.pi / 180).sin().alias("sin index"))
lf = lf.with_columns(pl.date(year="year", month="month", day=1).alias("Year Month"))
lf = lf.filter(pl.col('year') >= 2021)
lf = lf.with_columns((pl.lit("Site ") + pl.col("site id").cast(str).str.pad_start(2, "0")).alias("Site Name"))
lf = lf.select(pl.col(['Year Month', 'Site Name', tt]))
lf = lf.sort(['Year Month', 'Site Name'])

# naive query plan - nothing has been done yet
# If you have graphviz installed then uncomment the next line https://graphviz.org/download/
# lf.show_graph(optimized=False)

# text version of same plan
print("\nPolars unoptimised plan for all the same steps")
print(lf.explain(optimized=False))

# optimised plan
# If you have graphviz installed then uncomment the next line https://graphviz.org/download/
# lf.show_graph()

# Sometimes easier to read in text format
# Notice that doesn't even read columns from file 'avg_weekday_daily_traffic_veh_day', 'speed_am_peak_7_9am_km_hr', 'speed_pm_peak_4_7pm_km_hr'
# Doesn't calculate 'Volume per hour average' or 'sin index'
# It also calculates new columns in parallel rather than in series
print("\nPolars optimised plan")
print(lf.explain())

# Now we want to evaluate all these steps we call collect() to convert from 'lazy' to 'eager'
dfl_tfc = lf.collect()
print(f'Polars after running optimised plan\n{dfl_tfc}\n')

# Pivot is an eager function only. No lazy equivalent
dfl_pivot = dfl_tfc.pivot(index='Year Month', on='Site Name', values=tt)
print(f"Polars after pivoting on 'Site Name'\n{dfl_pivot}\n")
