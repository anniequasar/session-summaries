"""
MeetUp 013 - Beginners Python Support Sessions 29-May-2019

Learning objectives:
    Part 1: Web application forms - see https://github.com/timcu/bpss-prime-minister.git
    Part 2: Reading Excel files and inserting into sqlite database

@author D Tim Cummings

The following challenge continues on from MeetUp 011 which read several excel worksheets of bank transactions
and combined them into a single pandas dataframe.
It uses the example excel workbook bank_accounts.xlsx

Challenge: Insert the data from the combined dataframe into an sqlite database

requirements.txt
xlrd
pandas

"""

import pandas as pd
import sqlite3

dct_accounts = pd.read_excel("bank_accounts.xlsx", sheet_name=None, skiprows=0)
for sheet_name, df in dct_accounts.items():
    if len(df) > 0:
        if 'liability' in sheet_name:
            df.Amount *= -1
            df.Balance *= -1
balance = 0
for sheet_name, df in dct_accounts.items():
    if df.shape[0] > 0:
        balance += df.at[0, 'Balance']
        balance -= df.at[0, 'Amount']
    df['Account'] = sheet_name
    df['Amount'] = df['Amount'].round(2)
    # sqlite3 can't save pandas.Timestamp so convert to datetime.date
    df['date_transaction'] = df['Date'].apply(lambda ts: ts.date())

df_combined = pd.concat(dct_accounts.values(), ignore_index=True).sort_values(by="Date")
for index, row in df_combined.iterrows():
    balance += row['Amount']
    df_combined.at[index, 'Balance'] = balance

# Store results in sqlite database

# Connection to database is to a file in the current working directory called db_transactions.sqlite
# PARSE_DECLTYPES tells python to use declared types for converting data, especially declared type 'date'
# which doesn't exist in sqlite3 but python converts dates to text when inserting data and text to dates
# when selecting data for a 'date' field
db = sqlite3.connect(
    database='db_transactions.sqlite',
    detect_types=sqlite3.PARSE_DECLTYPES
)
# By default sqlite3 returns tuples from sql 'select'.
# sqlite3.Row manufactures dict type objects so fields can be referred by name
db.row_factory = sqlite3.Row
# cursor is a database concept common to all databases. While it is possible in sqlite3 to use db.execute() rather
# than db.cursor().execute(), we will use cursors in this example to demonstrate how most databases work.
cursor = db.cursor()
# We are about to create table in the database. This will throw an error if it already exists so drop it first
cursor.execute("drop table if exists tbl_transaction")
# The following sql creates a table and defines its data structure. Unusually sqlite3 doesn't require datatypes
# but we are providing them to be consistent with other databases. Python uses the 'date' datatype to convert dates
cursor.execute("""create table tbl_transaction (
    id integer primary key,
    date_transaction date,
    num_amount numeric,
    num_balance numeric,
    vc_account varchar,
    vc_description varchar
)""")

# sqlite3 can use named bindings (eg :id, :Amount) or unnamed bindings (eg ?, ?). This example uses named bindings
# We use the same sql string for each row of data that is inserted
sql = """insert into tbl_transaction (id, date_transaction, num_amount, num_balance, vc_account, vc_description) 
values (:id, :date_transaction, :Amount, :Balance, :Account, :Description)"""

# create a variable for our unique primary key
pk = 0
# loop through each row in chronological order
for index, row in df_combined.iterrows():
    # convert to dict so can add an extra key,value pair for primary key
    dct = dict(row)
    dct['id'] = pk
    # insert data in database using named bindings and a dict
    cursor.execute(sql, dct)
    # increment primary key
    pk += 1
    print(dct)

# we need to commit our transaction or else none of the data will be saved
db.commit()

# check that data is inserted by retrieving the first 20 records
sql = "select * from tbl_transaction limit 20"
records = cursor.execute(sql).fetchall()
for record in records:
    print(dict(record))
