# 6th session summary part B
# exploring pandas
# for those using PyCharm Edu - you need to install pandas by installing the library in your requirements.txt file in the same directory as your python file.
# do not call your file pandas.py because when you import pandas, python will import your python file not the pandas library.  

import pandas as pd

df_raw = pd.read_csv('run_results.csv')
print(df_raw)

# df_raw is our variable name which stores a pandas DataFrame of the raw data from the csv file.
# In pandas a DataFrame is a two dimensional collection of data (many rows and many columns),
# In pandas a Series is a one dimensional collection of data (many rows and one column)
# A DataFrame has an index, columns and values
# For df_raw the index is the numbers 0 to 80,
# columns are the heading names from the first line in the csv file ('race', 'runner', 'time')
# values are the data from all remaining lines in the csv file
#
# DataFrame.pivot(index=None, columns=None, values=None) is used to return a reshaped DataFrame organized by given index / column values.

df = df_raw.pivot(index='runner', columns='race', values='time')
print(df)
# For df the index is the names of the runners ('Annie', 'Bennie', ... 'Sam')
# columns are the dates of the races as strings ('2019-01-28', '2019-02-04', ... '2019-04-01')
# values are the times for each runner for each race (1521, 1596, ... 1772)


# to print who won each race we can use the for loop 
# df.columns contains all the race dates as strings

for race in df.columns:
    # race is a string containing the date of the race, eg '2019-01-28'
    # times is a pandas Series containing all the times of the race sorted in ascending order. If runner didn't run that race their time is NaN (not a number)
    # times.index is the names of the runners for those times. It is the index of the pandas Series times.
    times = df[race].sort_values()
    print(times)
    # times[0] is the fastest time because times is in ascending order
    # times.index[0] is the runner who had the fastest time
    print(times[0], times.index[0], race)


# DataFrame.transpose will transpose index and columns i.e., reflect the DataFrame over its main diagonal by writing rows as columns and vice-versa. 
# The property T is an accessor to the method transpose().

dft = df.T

# the challenge is to find the fastest time of each runner

print(dft)

# the solution

for runner in dft.columns:
    fastest_time = dft[runner].sort_values()
    print(runner+"\'s fastest time is", fastest_time[0])


# advanced challenge:
#   display the place of each runner in each race checking for tied places (times are equal)
#   display the results using a format string
#   display times in minutes and seconds not just seconds

for race in df.columns:
    # race is a string containing the date of the race, eg '2019-01-28'
    # times is a pandas Series containing all the times of the race sorted in ascending order. If runner didn't run that race their time is dropped (dropna())
    # times.index is the names of the runners for those times. It is the index of the pandas Series times.
    times = df[race].sort_values().dropna()
    place = 0
    tied = 0  # number of runners with the same time for this race
    prev_time = -1  # time of previous runner. checking for ties
    # To loop through runner's name and time use .items() just as you would for a dict 'for key, value in dict.items():'
    for runner, time in times.items():
        if time == prev_time:
            tied += 1
        else:
            place += tied + 1
            tied = 0
            prev_time = time
        print('Race {race}: place {place} is {runner} with a time of {minutes:02d}:{seconds:02d}'.format(place=place, race=race, runner=runner, minutes=(int(time) // 60), seconds=(int(time) % 60)))
