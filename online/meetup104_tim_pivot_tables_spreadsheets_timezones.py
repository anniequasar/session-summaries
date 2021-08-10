#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MeetUp 104 - Beginners' Python and Machine Learning - 20 Apr 2021 - Pandas pivot tables, spreadsheets and timezones

Colab:   https://colab.research.google.com/drive/1E2UpcfeixraUxQG3PWUyhpIQsKPfcWId
Youtube: https://youtu.be/BrKZI6STurE
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/277479287/
Github:  https://github.com/anniequasar/session-summaries/tree/master/online

Learning objectives:
- Pivoting and unpivoting datasets in pandas
- Saving and reading spreadsheets
- Daylight savings time and timezones
- Cleaning and analysing data from New Zealand electricity generation https://www.emi.ea.govt.nz/Wholesale/Datasets

@author D Tim Cummings

requirements.txt
pandas>=1.2.0
xlrd>=2.0.1
xlsxwriter
openpyxl
pytz
"""
import datetime
import inspect
import packaging.version

import openpyxl
import pytz
import pandas as pd
import pandas.io.excel._util as pd_excel_util

pd.options.display.width = 200
pd.options.display.max_columns = 17

# Read generation data for April 2020
df_raw = pd.read_csv("https://www.emi.ea.govt.nz/Wholesale/Datasets/Generation/Generation_MD/202004_Generation_MD.csv")

# Notice where daylight savings time was introduced
print(f"df_raw.head(10)=\n{df_raw.head(10)}")

"""### Desired format

| Gen_Code<br>POC_Code | twf_12<br>BPE0331| twf_12<br>LTN0331 | white_hill<br>NMA0331| te_rere_hau<br>TWC2201 | twf_3<br>TWC2201 | te_uku<br>TWH0331|te_apiti<br>WDV1101|west_wind<br>WWD1102|west_wind<br>WWD1103|
| --- | --: | --: | --: | --: | ---:| ---:| ---:| ---:| ---:
| UTC_time|
2020-03-31 11:00 |6.06|37.08|5256.95|93.63|2288.15|0.00|1.00|298.00|2.00
2020-03-31 11:30 |0.00|0.00|3148.61|0.57|1166.63|0.00|0.00|13.00|0.00
... 

1. Filter on Fuel_Code is wind
2. Convert TP1 TP2 ... columns to rows
3. Convert times to UTC to remove ambiguity of daylight savings time
4. Change index from 0 1 2 to UTC_Time 
5. Remove unneeded columns Site, Nwk, Fuel and Tech
6. Save to Excel (formatted)
7. Read back from Excel
"""

print(f"{type(df_raw)=}")

print(f"{type(df_raw['Fuel_Code'])=}")

print(f"{df_raw['Fuel_Code'].unique()=}")

print(f"{df_raw['Tech_Code'].unique()=}")

print(f"{df_raw['Gen_Code'].unique()=}")

print(f"{df_raw['Nwk_Code'].unique()=}")

print(f"{df_raw['POC_Code'].unique()=}")

# If we know the fuel we don't necessarily know the tech (gas could be cogen or thermal)
print(f"df_raw.groupby(['Fuel_Code', 'Tech_Code']).size()=\n{df_raw.groupby(['Fuel_Code', 'Tech_Code']).size()}")

# Filter on fuel to get all the wind generators
df_wind = df_raw[df_raw['Fuel_Code'] == 'Wind']
print(f"df_wind.head()=\n{df_wind.head()}")

"""### Task 1
Unpivot the columns TP1, TP2, ..., TP50 using the melt method. Drop any rows which have NaN in kWh column.

||POC_Code|Gen_Code|Trading_date|Trading_period|kWh
-|-:|-:|-:|-:|-:
0|BPE0331|twf_12|2020-04-01|TP1|6.0646
1|BPE0331|twf_12|2020-04-02|TP1|773.2509
...
"""
# help(pd.DataFrame.melt)

# Solution 1
# Create a new column 'Trading_Period' which contains a value TP1, TP2, TP3 etc
df_30min = df_wind.melt(
                    id_vars=['POC_Code', 'Gen_Code', 'Trading_date'],
                    value_vars=[f"TP{i+1}" for i in range(50)],
                    var_name='Trading_period',
                    value_name='kWh').dropna()
print(f"Solution 1: df_30min.head()=\n{df_30min.head()}")

# Check different values of Trading_period and kWh
print(f"Solution 1: Check different values of Trading_period and kWh\n{df_30min[(df_30min['Trading_date'] == '2020-04-01') & (df_30min['Gen_Code'] == 'twf_12')].head()}")

# Check how many days in first week of April use TP49 (and TP50)
print(f"Solution 1: Check how many days in first week of April use TP49 (and TP50)\n{df_30min[(df_30min['Trading_period'] == 'TP49') & (df_30min['Gen_Code'] == 'twf_12')].head(8)}")

# Python timezones with datetime and pytz
# Timezones are one of the most complicated programming problems
# Daylight savings dates can change in the future
# New Zealand stops daylight savings 3am on first Sunday in April

# Create a timezone naive datetime
dt = datetime.datetime.strptime('2020-04-05 00:30', '%Y-%m-%d %H:%M') 
# Convert datetime from timezone naive to timezone aware
dtnz = pytz.timezone('Pacific/Auckland').localize(dt)
for s in ['NZ time + delta', 'Timezone naive', 'NZ time from tz naive', 'UTC from NZ + delta', 'NZ time from UTC', 'Timedelta']:
    print(f"{s:28}", end='')
print()
for i in range(30):
    # Add some hours to timezone aware datetime using timedelta (NZ + delta)
    dtnz1 = dtnz + datetime.timedelta(hours=i)
    # Convert (NZ time + delta) to Timezone naive
    dtnz2 = dtnz1.replace(tzinfo=None)
    # Convert Timezone naive datetime to NZ time when DST stopping
    dtnz3 = pytz.timezone('Pacific/Auckland').localize(dtnz2)
    # Convert NZ time + delta to UTC
    dtutc = dtnz1.astimezone(pytz.utc)
    # Convert UTC to NZ time
    dtnz4 = dtutc.astimezone(pytz.timezone('Pacific/Auckland'))
    td = dtnz4 - dtnz
    print(f"{dtnz1}   {dtnz2}         {dtnz3}   {dtutc}   {dtnz4}   {td}")

# NZ time + delta showing wrong offset
# Timezone naive is useless around daylight savings stop time
# NZ time from tz naive has a two hour gap from 1:30+13:00 to 2:30+12:00
# UTC correct but not clear to user
# NZ time from UTC is correct but requires offset to be meaningful

# Conclusion: Store times in UTC. Convert to NZ time when displaying

# Task 2
# Create a function utc_from_date_and_period which takes the date and period as 
# str and returns a datetime object in UTC timezone

# utc_from_date_and_period('2020-04-01', 'TP1' ) = 2020-03-31 11:00:00+00:00
# utc_from_date_and_period('2020-04-30', 'TP2' ) = 2020-04-29 12:30:00+00:00
# utc_from_date_and_period('2020-04-05', 'TP6' ) = 2020-04-04 13:30:00+00:00
# utc_from_date_and_period('2020-04-05', 'TP8' ) = 2020-04-04 14:30:00+00:00
# utc_from_date_and_period('2020-04-05', 'TP48') = 2020-04-05 10:30:00+00:00
# utc_from_date_and_period('2020-04-06', 'TP48') = 2020-04-06 11:30:00+00:00


def utc_from_date_and_period(str_date, str_period):
    dt = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    dt_nz = pytz.timezone('Pacific/Auckland').localize(dt)
    dt_utc = dt_nz.astimezone(pytz.utc)
    tp = int(str_period[2:])
    return dt_utc + (tp - 1) * datetime.timedelta(minutes=30)


for (d, p) in [('2020-04-01', 'TP1'), ('2020-04-30', 'TP2'), 
               ('2020-04-05', 'TP6'), ('2020-04-05', 'TP8'), 
               ('2020-04-05', 'TP48'), ('2020-04-06', 'TP48')]:
    utc = utc_from_date_and_period(d, p)
    print(f"utc_from_date_and_period({d!r}, {repr(p):6}) = {utc}")

"""### Task 3
Create a new column called 'UTC_time' based on Trading_date and Trading_period

https://forum.emi.ea.govt.nz/thread/daylight-saving-time-and-trading-periods

index|POC_Code|Gen_Code|Trading_date|Trading_period|kWh|UTC_time
-|-:|-:|-:|-:|-:|-:
0|BPE0331|twf_12|2020-04-01|TP1|6.0646|2020-03-31 11:00:00+00:00
1|BPE0331|twf_12|2020-04-02|TP1|773.2509|2020-04-01 11:00:00+00:00
...

"""
# help(pd.DataFrame.apply)


# Solution 3
def apply_utc(row):
    return utc_from_date_and_period(row['Trading_date'], row['Trading_period'])


df_30min['UTC_time'] = df_30min.apply(apply_utc, axis=1)
# Check dates calculated correctly
print(f"Solution 3: \n{df_30min.head()}")

# Check trading periods calculated correctly
print(f"Solution 3: Check trading periods calculated correctly\n{df_30min[(df_30min['Trading_date'] == '2020-04-01') & (df_30min['Gen_Code'] == 'twf_3')].head()}")

# Uncomment following line to see problem with saving to excel. I think openpyxl is default
# df_30min.to_excel("df_30min.xlsx", engine="xlwt")
# df_30min.to_excel("df_30min.xlsx", engine="openpyxl")

# Task 4 
# Ensure times in dataframe are timezone naive by rewriting apply_utc


# Solution 4
def apply_utc(row):
    utc_calc = utc_from_date_and_period(row['Trading_date'], row['Trading_period'])
    return utc_calc.replace(tzinfo=None)


df_30min['UTC_time'] = df_30min.apply(apply_utc, axis=1)
# Check dates calculated correctly
df_30min.head()

# Check it works now
# openpyxl is the default for writing xlsx files if xlsxwriter is not installed
df_30min.to_excel("df_30min.xlsx", engine="openpyxl")

# Which engine is used by default (get_default_writer is _get_default_writer in earlier pandas)
print(inspect.getsource(pd_excel_util.get_default_writer))
print(f"Default writer for 'xlsx' is {pd_excel_util.get_default_writer('xlsx')}")

# What does it look like when we read excel file back in
# help(pd.read_excel)

# engine = 'xlrd' is default for pandas<1.2 .
# xlrd 2.0.0 can no longer read .xlsx files
# df_read = pd.read_excel("df_30min.xlsx", engine="xlrd")
df_read = pd.read_excel("df_30min.xlsx", engine="openpyxl")
# df_read = pd.read_excel("df_30min.xlsx")
print(f"df_read.head()=\n{df_read.head()}")

# openpyxl tries to use microseconds in datetime while xlrd used millisecond
# openpyxl 3.0.7 (released 2021-03-09) fixed this 'bug' because spec says ms
openpyxl_version = packaging.version.parse(openpyxl.__version__)
if openpyxl_version >= packaging.version.parse("3.0.7"):
    print(f"openpyxl version = {openpyxl_version} which includes rounding fix. Don't need to round manually")
else:
    # Remember to round time data when using openpyxl prior to 3.0.7
    df_read['UTC_time'] = df_read['UTC_time'].round("1s")
    print(f"After rounding df_read.head()=\n{df_read.head()}")

# What are the New Zealand wind generators
print(f"New Zealand wind generators = {sorted(df_30min['Gen_Code'].unique())}")

# Task 5 
# Pivot dataframe to show one column for each (wind farm/point of connection combination), index being UTC_time
# help(pd.DataFrame.pivot)

print(f"Task 5: df_30min.head()=\n{df_30min.head()}")


# Solution 5
df_kwh = df_30min.pivot(index='UTC_time', columns=['Gen_Code', 'POC_Code'], values='kWh')
print(f"Solution 5: df_kwh.head()=\n{df_kwh.head()}")

# You can save a pivoted DataFrame to excel
df_kwh.to_excel("df_kwh.xlsx", engine="openpyxl")

# Task 6 Read df_kwh.xlsx into a DataFrame. Set header and index_col parameters
# help(pd.read_excel)

# Solution 6: How to read in DataFrame when column names are a MultiIndex
df_read = pd.read_excel("df_kwh.xlsx", header=[0, 1], index_col=[0], engine="openpyxl")
if openpyxl_version < packaging.version.parse("3.0.7"):
    # Remember to round time data when using openpyxl prior to 3.0.7
    df_read.index = df_read.index.round("1s")
print(f"Solution 6: df_read.head()=\n{df_read.head()}")

# To format the spreadsheet we are saving, we can use xlsxwriter rather than openpyxl
# xlsxwriter has better documentation for using as an engine with pandas
# https://xlsxwriter.readthedocs.io/working_with_pandas.html
writer = pd.ExcelWriter("pretty.xlsx", engine="xlsxwriter", datetime_format="yyyy-MM-dd hh:mm:ss")
df_kwh.to_excel(writer, sheet_name="My report")
wb = writer.book
fmt_dollar = wb.add_format({'num_format': '$#,##0.00_);[Red]($#,##0.00)'})
fmt_kwh = wb.add_format({'num_format': '#,##0.00_)'})
fmt_title = wb.add_format({'bold': True, 'align': 'left'})
ws = wb.sheetnames["My report"]
ws.set_column('A:A', 20)  # Index column width
ws.set_column('B:I', 12, fmt_kwh)  # kWh columns 
ws.set_column('J:J', 12, fmt_dollar)  # Ue $ for last column
ws.freeze_panes('B4')  # Freeze panes around B4 (4 -> 3, B -> 1)
ws2 = wb.add_worksheet("Page Two")
ws2.write('A1', "Some text, a number and a formula", fmt_title)
ws2.write('A2', 3)
ws2.write_formula('A3', '=A2*A2')  # LibreOffice doesn't automatically calc on load. Excel does
writer.save()

