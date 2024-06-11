r"""MeetUp 203 - Beginners' Python and Machine Learning - 15 May 2024 - pandas

Learning objectives:
- Introduction to data handling with pandas

Links:
- Colab:   https://colab.research.google.com/drive/1Xg6MexDX4-7ngkIbkr2pTu9dNOjjuLvi
- Youtube: https://youtu.be/hwOah3cauIc
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/300755291/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

Today we are introducing pandas and some of its features useful for data science. We will collect data from an online API and store in a DataFrame. Then we will perform filtering, converting, calculating and pivoting the data.

- https://pandas.pydata.org

# Using Google Colab / Jupyter Notebooks / IPython

- type into a cell
- press `<shift><enter>` to execute the cell
- cells can be python code or markdown text or input fields
- use ? or Help menu for help
- see Help menu > Keyboard shortcuts
"""
# How to install pandas into a python virtual environment if you are using Python from https://python.org
# python3 -m venv venv187
# source venv187/bin/activate   # Mac or Linux
# venv187\Scripts\Activate.bat  # Windows cmd
# pip install pandas matplotlib

# Anaconda, and Google Colab both preinstall pandas

# How to determine pandas version from the command line (prefix with ! in jupyter notebook)
# pip list | grep pandas

# Start using pandas by importing it. To save time typing 'pd' instead of 'pandas' use an import alias
import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt

# Let's get some data from https://www.data.brisbane.qld.gov.au/data/dataset/public-art and store it in a DataFrame
# Use the pandas method read_csv to read data from URL or from a file
# Good if you know the encoding. I had to try a few before this worked.
# Default encoding is 'utf-8'. I also tried 'latin1' which didn't show quotes correctly
# Update 2024: BCC fixed encoding issues so utf-8 works as does cp1252, latin1
url_art = 'https://www.data.brisbane.qld.gov.au/data/dataset/1e11bcdd-fab1-4ec5-b671-396fd1e6dd70/resource/3c972b8e-9340-4b6d-8c7b-2ed988aa3343/download/public-art-open-data-2023-03-14.csv'
df_art = pd.read_csv(url_art, encoding='utf-8')
# Look at the data
print(f"df_art=\n{df_art}")

# In pandas, DataFrames are a two dimensional array of data.
# Series are a one dimensional array of data. Each column in a DataFrame can be used a Series
# Use [] notation with name of column to isolate just one column
s = df_art['Item_title']
print(f"df_art is a {type(df_art)} and s is a {type(s)}")

# A series has an index as well as a column of values
print(f"Series s=\n{s}")

# To get a sub DataFrame use a list of column names
df_art_3 = df_art[['Item_title', 'Latitude', 'Longitude']]
print(f"df_art_3=\n{df_art_3}")

def scatter_plots(df, colname_pairs, scatter_plot_size=2.5, size=8, alpha=.6):
  plt.figure(figsize=(len(colname_pairs) * scatter_plot_size, scatter_plot_size))
  for plot_i, (x_colname, y_colname) in enumerate(colname_pairs, start=1):
    ax = plt.subplot(1, len(colname_pairs), plot_i)
    ax.scatter(df[x_colname], df[y_colname], s=size, alpha=alpha)
    plt.xlabel(x_colname)
    plt.ylabel(y_colname)
    ax.spines[['top', 'right',]].set_visible(False)
  plt.tight_layout()
  return plt

chart = scatter_plots(df_art_3, *[[['Latitude', 'Longitude']]], **{})
chart.show()

# In colab you can invoke the wizard to create the above code and chart
# Click on wizard to view dataframe in colab,
# Click chart icon to show example charts
# Select chart Longitude vs Latitude
# Add cell
# Edit supplied code to plot Latitude vs Longitude rather then Longitude vs Latitude
# and change scatter_plot_size to 7
df_art.plot(kind='scatter', x='Longitude', y='Latitude', s=7, alpha=.8)

# This is the sample code that used to be generated. It used matplotlib directly rather than through pandas dataframe
# It is modified to show just Latitude (y) versus Longitude (x) with scatter_plot_size=5 and some titles

def scatter_plots_with_titles(df, colname_pairs, scatter_plot_size=2.5, size=8, alpha=.6):
  plt.figure(figsize=(len(colname_pairs) * scatter_plot_size, scatter_plot_size))
  for plot_i, (x_colname, y_colname) in enumerate(colname_pairs, start=1):
    ax = plt.subplot(1, len(colname_pairs), plot_i)
    ax.scatter(df[x_colname], df[y_colname], s=size, alpha=alpha)
    plt.xlabel(x_colname)
    plt.ylabel(y_colname)
    ax.spines[['top', 'right',]].set_visible(False)
    # Add some titles if they are provided
    if "Item_title" in df:
        for idx in df.index:
            if idx % 5 == 0:
                # We can refer to individual items in a DataFrame using .at[row, col]
                x = df.at[idx, x_colname]
                y = df.at[idx, y_colname]
                t = df.at[idx, "Item_title"]
                if y < -27.49 or y > -27.45:
                    # show text next to some data points
                    ax.text(x + 0.001, y + 0.001, t)
  plt.tight_layout()
  return plt

chart = scatter_plots_with_titles(df_art, *[[['Longitude', 'Latitude']]], scatter_plot_size=5, **{})
chart.show()

# Using .at to access a single data element
print(f'\ndf_art.at[4, "Item_title"]=\n{df_art.at[4, "Item_title"]}')

# Methods to access part of DataFrame via named index and columns
# df.at[row, col] => access one element
# df.loc[rows, cols] => access multiple elements

# Methods to access part of DataFrame via numbered index and columns
# df.iat[irow, icol] => access one element by zero based integer indexes
# df.iloc[irows, icols] => access multiple elements by zero based integer indexes

# Using .loc to access a single data element
print(f'\ndf_art.loc[4, "Item_title"]=\n{df_art.loc[4, "Item_title"]}')

# .loc can be used with a sub DataFrame of rows just like we retrieved a sub DataFrame of columns before
# Notice how slice includes ending row which is unusual in Python
print(f'\ndf_art.loc[2:5]=\n{df_art.loc[2:5]}')

# Can also slice on columns, but have to provide a slice for rows. : = all rows
# Notice how we have to provide a space at end of Material because that is in original data
print(f"\ndf_art.loc[:, 'Artist':'Material']=\n{df_art.loc[:, 'Artist':'Material']}")

# List all column names
print(f"\n{df_art.columns=}")

# We can rename columns. Notice how we are using `inplace=True` so we are editing the DataFrame rather than returning a new one.
new_names = {n: n.strip() for n in df_art.columns}
print(f"{new_names=}")
df_art.rename(columns=new_names, inplace=True)
print(f"{df_art.columns=}")

# Save csv file from BCC Open Data to see what caused the spaces at end of column names
# Update 2024: BCC have fixed data so no longer spaces at the end of some column names
from urllib.request import urlopen
with urlopen(url_art) as file_obj:
    with open('public_art.csv', 'wb') as pa_csv:
        pa_csv.write(file_obj.read())
# View the file using the operating system command line rather than python code
# head public_art.csv
print("\nCause of spaces in header names")
with open('public_art.csv', 'rb') as pa_csv:
    print(pa_csv.readline())

# Advanced - Find a line which is not utf-8
# Update 2024: BCC have fixed data so no longer encoded cp1252. Must be ascii
print("\nFINDING NON-UNICODE TEXT IN ART LIST (may be none)")
with open('public_art.csv', 'rb') as pa_csv:
    lines = pa_csv.read().split(b'\r\n')
    for i, line in enumerate(lines):
        try:
            s = line.decode('utf-8')
        except UnicodeDecodeError:
            print(i, line)
            s = line.decode('cp1252')
            print(i, s)
            break

print(f"\ndf_art=\n{df_art}")

# Can use a list of bools on rows or columns to specify which ones to include
df_art_13_from_bools = df_art.loc[:, [True, False, True, False, False, False, False, False]]
print(f"\ndf_art.loc[:, [True, False, True, False, False, False, False, False]]=\n{df_art_13_from_bools}")

# Can create a list of bools using an expression
lst_bools = df_art.columns.str.contains("_")
print(f'\ndf_art.columns.str.contains("_")=\n{lst_bools}')
# Put them together
df_art_13 = df_art.loc[:, df_art.columns.str.contains("_")]
print(f'\ndf_art.loc[:, df_art.columns.str.contains("_")]=\n{df_art_13}')

# Could also use earlier expression df[[column names, ...]]
print(f'\ndf_art[df_art.columns[df_art.columns.str.contains("_")]]=\n{df_art[df_art.columns[df_art.columns.str.contains("_")]]}')

# More common to filter this way on rows
print("\nFind art installed last year")
print(f"df_art.loc[df_art['Installed']>=2023]=\n{df_art.loc[df_art['Installed']>=2023]}")

# Look at traffic data
# https://www.data.brisbane.qld.gov.au/data/dataset/traffic-management-key-corridor-monthly-performance-report/resource/70da5292-87a1-4fd4-8a35-b0a723566884
# Remove bom=True from CSV URL https://www.data.brisbane.qld.gov.au/data/datastore/dump/70da5292-87a1-4fd4-8a35-b0a723566884?bom=True
url_tfc = 'https://www.data.brisbane.qld.gov.au/data/datastore/dump/70da5292-87a1-4fd4-8a35-b0a723566884'
with urlopen(url_tfc) as file_obj:
    with open('traffic.csv', 'wb') as tfc_csv:
        tfc_csv.write(file_obj.read())
# View the file using the operating system command line rather than python code
print('\nFirst few lines of traffic.csv')
with open('traffic.csv', 'rb') as tfc_csv:
    lines = tfc_csv.readlines()
    for line in lines[:3]:
        print(line)
# head traffic.csv

# Read csv from file
df_tfc = pd.read_csv('traffic.csv')
print(f"\ndf_tfc=\n{df_tfc}")

# Perform arithmetical operation on a column and store the result
df_tfc['Volume per hour average'] = df_tfc['Average Weekday Daily Traffic (Veh/day)'] / 24
print("\nAFTER CALCULATING 'Volume per hour average'")
print(f"df_tfc=\n{df_tfc}")


# Calculations can be more complicated, although not every calculation can work
# Operators (+,-,*,/) are overriden so this works.
vol_am = 'Volume per hour AM Peak'
vol_pm = 'Volume per hour PM Peak'
tt_am = 'Average TT AM Peak (seconds)'
tt_pm = 'Average TT PM Peak (seconds)'
tt = 'Average TT Peak (seconds)'
df_tfc[tt] = (df_tfc[tt_am] * df_tfc[vol_am] + df_tfc[tt_pm] * df_tfc[vol_pm]) / (df_tfc[vol_am] + df_tfc[vol_pm])
print("\nAFTER CALCULATING 'Average TT Peak (seconds)'")
print(f"df_tfc=\n{df_tfc}")


# Check data for Site ID 2 in May 2023
avg_tt = (1865 * 1182 + 1899 * 1023) / (1865 + 1899)
assert avg_tt == df_tfc.loc[(df_tfc['Year'] == 2023) & (df_tfc['Month'] == 'May') & (df_tfc['Site ID'] == 2), 'Average TT Peak (seconds)'].values[0]

# Check using query instead of filters
assert avg_tt == df_tfc.query('Year == 2023 & Month == "May" & `Site ID` == 2')['Average TT Peak (seconds)'].values[0]

# To call functions use numpy functions rather than Python functions
# The following won't work
# df_tfc['sin_id'] = math.sin(df_tfc['_id'] * math.pi / 180)

# Use sin from numpy which can work on ndarrays
df_tfc['sin_id'] = np.sin(df_tfc['_id'] * math.pi / 180)
print("\nAFTER CALCULATING 'sin_id'")
print(f"df_tfc=\n{df_tfc}")

# For datetime use pandas.to_datetime
df_tfc['Year Month'] = pd.to_datetime(df_tfc['Year'].astype(str) + df_tfc['Month'], format=("%Y%b"))
print("\nAFTER CALCULATING 'Year Month'")
print(f"df_tfc=\n{df_tfc}")

# Make the Site names more interesting than Site ID and take a portion of the DataFrame
df_tfc['Site Name'] = 'Site ' + df_tfc['Site ID'].astype(str).str.zfill(2)
df_vol = df_tfc[['Site Name', 'Year Month', 'Average Weekday Daily Traffic (Veh/day)']]
print("\nAFTER CALCULATING df_vol")
print(f"df_vol=\n{df_vol}")
df_vol.head(30)

# Now we can pivot data
df_pivot = df_vol.pivot(index='Year Month', columns='Site Name', values='Average Weekday Daily Traffic (Veh/day)')
print("\nAFTER PIVOTING")
print(f"df_pivot=\n{df_pivot}")
