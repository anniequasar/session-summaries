"""
MeetUp 011 - Beginners Python Support Sessions 15-May-2019

@author D Tim Cummings

Challenges:

The following challenges will develop some tools for you to analyse your bank account data using Python.
They use the example excel workbook bank_accounts.xlsx

Challenge 9: Read first two sheets of excel workbook and calculate the total opening balance of those accounts

Challenge 10: Calculate and plot the total balance of 'savings' and 'credit_card' on a chart versus date

Advanced challenge 10A: All lines on plot to be vertical or horizontal (no diagonal) to represent balance in accounts
Advanced challenge 10B: If balance goes up and down on same day just show final balance

Challenge 11: Read all sheets from excel spreadsheet. Assume sheets are asset values unless they contain the
word liability in which case amounts and balances have to be negated to convert from liabilities to negative assets.

If using PyCharm Edu:

requirements.txt
xlrd
pandas

"""

import pandas as pd
# from pandas.plotting import register_matplotlib_converters
# import matplotlib.pyplot as plt

# register_matplotlib_converters()  # required to show dates on plots
sheet_name = 'savings'
dct_accounts = pd.read_excel("bank_accounts.xlsx", sheet_name=[sheet_name])
# print("Type of dct_accounts", type(dct_accounts))
df = dct_accounts[sheet_name]
# print(df.tail())
# print(df.shape)
print("Closing balance = ", df.at[df.shape[0]-1, 'Balance'])


# Challenge 9: Read sheets 'savings' and 'credit_card' of excel workbook and calculate the combined opening balance

dct_accounts = pd.read_excel("bank_accounts.xlsx", sheet_name=["savings", "credit_card"])
balance = 0
for sheet_name, df in dct_accounts.items():
    print(sheet_name)
    print(df.head())
    if df.shape[0] > 0:
        balance += df.at[0, 'Balance']
        balance -= df.at[0, 'Amount']
print(balance)

# Challenge 10: Calculate and plot the combined balance of 'savings' and 'credit_card' on a chart versus date
# Advanced challenge 10A: All lines on plot to be vertical or horizontal (no diagonal) to represent balance in accounts
# Advanced challenge 10B: If balance goes up and down on same day just show final balance

import matplotlib.pyplot as plt

# following required to stop warning about dates on plots
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df_combined = pd.concat(dct_accounts.values(), ignore_index=True).sort_values(by="Date")
dct_balance = {}
for index, row in df_combined.iterrows():
    balance += row['Amount']
    df_combined.at[index, 'Balance'] = balance
    dct_balance[row['Date']] = balance
print(df_combined)


plt.figure(figsize=(10, 10))
plt.plot(dct_balance.keys(), dct_balance.values(), drawstyle="steps-post")
# plt.plot(dct_balance.keys(), dct_balance.values())
# plt.plot(df_combined["Date"], df_combined["Balance"], drawstyle="steps-post")
plt.xticks(rotation='vertical')
plt.show()

# Challenge 11: Read all sheets from excel spreadsheet. Assume sheets are asset values unless they contain the
# word liability in which case amounts and balances have to be negated to convert from liabilities to negative assets.

dct_accounts = pd.read_excel("bank_accounts.xlsx", sheet_name=None, skiprows=0)
for sheet_name, df in dct_accounts.items():
    if len(df) > 0:
        if 'liability' in sheet_name:
            df.Amount *= -1
            df.Balance *= -1
df_combined = pd.concat(dct_accounts.values(), ignore_index=True).sort_values(by="Date")
dct_balance = {}
for index, row in df_combined.iterrows():
    balance += row['Amount']
    df_combined.at[index, 'Balance'] = balance
    dct_balance[row['Date']] = balance
print(df_combined)

plt.figure(figsize=(10, 10))
plt.plot(dct_balance.keys(), dct_balance.values(), drawstyle="steps-post")
plt.xticks(rotation='vertical')
plt.show()
