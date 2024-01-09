#! /usr/bin/env python3
r"""MeetUp 123 - Beginners' Python and Machine Learning - 09 Nov 2021 - Creating spreadsheets from Python

Learning objectives:
- parsing text files
- Saving and reading spreadsheets

The objective today is to parse all the beginners' python and machine learning python scripts for Youtube links and save them in a spreadsheet.

Links:
- Colab:   https://colab.research.google.com/drive/16vB_HDGVMH_EYD4dU3mZA9j5eIJtVqTL
- Youtube: https://youtu.be/XdEsNxbVrQA
- Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/281813250/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings
"""

# Clone the github repository so we can create some data to populate our spreadsheet
# We are going to parse the python scripts from all our meetups and make a table in a spreadsheet
# To run command line operations in google colab, start the line with !. Don't type ! if in Windows macOS or Linux command line.
# !git clone https://github.com/timcu/bpaml-sessions.git

# To run this script
# I recommend creating a virtual environment
#     python3 -m venv bpaml      # Linux or macOS
#     python -m venv bpaml       # Windows
# Activating virtual environment
#     source bpaml/bin/activate  # Linux or macOS
#     bpaml\Scripts\Activate     # Windows
# xlsxwriter doesn't come with python or anaconda so need to install it
# Install xlsxwriter using python (different instructions required for anaconda - see meetup115)
#     pip install xlsxwriter
# Run script
#     python meetup123_tim_creating_spreadsheets.py

# How to read all the python script names in the online directory
# Use pathlib which is Python's object oriented way of using files and directories
# https://docs.python.org/3/library/pathlib.html
from pathlib import Path
online_directory = Path('.')
lst_scripts = list(online_directory.glob("*_tim_*.py"))
# Sort the list using sort method
lst_scripts.sort()
print("Names of python scripts in online directory of session-summaries repo")
for f in lst_scripts:
    print(f)
print("\nDatatype of scripts from pathlib glob", type(f))


# Save list of python scripts to an excel spreadsheet
# xlsxwriter is very good if you don't need to read an excel spreadsheet. 
# xlsxwriter is the most configurable when exporting from pandas DataFrames 
# https://xlsxwriter.readthedocs.io/

# Example of creating workbook with a worksheet called scripts
import xlsxwriter
# use 'with' so don't need to remember to close or if error jumps out of code and misses close command
with xlsxwriter.Workbook("bpaml-links-0.xlsx") as workbook:
    worksheet = workbook.add_worksheet("scripts")
    # enumerate gives index and value for loop because sometimes we want both and this saves a line of code
    for i, script in enumerate(lst_scripts):
        # have to convert PosixPath to str
        # write(row, col, value), row and column are zero indexed
        worksheet.write(i, 0, str(script))

print("\nUsing pathlib PurePath to split filename into parts")
s = lst_scripts[0]
print(f"s         {s}")
print(f"s.name    {s.name}")
print(f"s.stem    {s.stem}")
print(f"s.suffix  {s.suffix}")
print(f"s.parent  {s.parent}")
print(f"s.parents {list(s.parents)}")

# Task 1: Store index i in column "A" and the script name without the suffix in column "B"



# Solution 1: 
with xlsxwriter.Workbook("bpaml-links-1.xlsx") as workbook:
    worksheet = workbook.add_worksheet("scripts")
    # You can also use "A1" type references when using write
    worksheet.write("A1", "Index")
    worksheet.write("B1", "Script name")
    # Set column widths
    worksheet.set_column("B:B", 50)
    for i, script in enumerate(lst_scripts):
        # write is an alias for write_string, write_number, write_blank, write_formula, write_datetime, write_boolean, write_url
        worksheet.write_number(i + 1, 0, i)
        worksheet.write_string(i + 1, 1, script.stem)

# Task 2: Use "A1" type references to write script stems



# Solution 2
with xlsxwriter.Workbook("bpaml-links-2.xlsx") as workbook:
    worksheet = workbook.add_worksheet("scripts")
    # Create horizontal alignment format for first column
    fmt_centre = workbook.add_format({"align": "center"})
    worksheet.write("A1", "Meetup"     , fmt_centre)
    worksheet.write("B1", "Script name")
    # Set column widths
    worksheet.set_column("B:B", 50)
    for i, script in enumerate(lst_scripts):
        row = i + 2
        meetup = int(script.name[6:9])
        worksheet.write(f"A{row}", meetup     , fmt_centre)
        worksheet.write(f"B{row}", script.stem)
    # Calculate total of all meetup numbers (may need to press F9 if opening in LibreOffice)
    worksheet.write(f"A{row+2}", f"=SUM(A2:A{row})", fmt_centre)

# Task 3 Format first row in bold using {"bold", True}



# Solution 3
with xlsxwriter.Workbook("bpaml-links-3.xlsx") as workbook:
    worksheet = workbook.add_worksheet("scripts")
    dcf_col_a = {"align": "center", "num_format": "000"}
    dcf_row_1 = {"bold": True}
    # Merge two dicts without affecting originals (pre Python 3.5) 
    dcf_a1 = {}
    dcf_a1.update(dcf_col_a)  # inherit all formats from column A
    dcf_a1.update(dcf_row_1)  # inherit all formats from row 1
    
    # Merge two dicts without affecting originals (Python 3.5 - 3.8) 
    # dct_a1 = {**dcf_col_a, **dcf_row_1}
    
    # Merge two dicts without affecting originals (Python 3.9) 
    # dct_a1 = dcf_col_a | dcf_row_1
    
    fmt_col_a = workbook.add_format(dcf_col_a)
    fmt_row_1 = workbook.add_format(dcf_row_1)
    fmt_a1 = workbook.add_format(dcf_a1)
    worksheet.write("A1", "Meetup"     , fmt_a1)
    worksheet.write("B1", "Script name", fmt_row_1)
    # Set column widths
    worksheet.set_column("B:B", 50)
    for i, script in enumerate(lst_scripts):
        row = i + 2
        meetup = int(script.name[6:9])
        worksheet.write(f"A{row}", meetup     , fmt_col_a)
        worksheet.write(f"B{row}", script.stem)
    # Calculate total of all meetup numbers (may need to press F9 if opening in LibreOffice)
    worksheet.write(f"A{row+2}", f"=SUM(A2:A{row})", fmt_col_a)

print("\nOpen first file and read the first 10 lines")
# 'with' command ensures file is automatically closed when finished with
with open(lst_scripts[0]) as f:
    # get text from file one line at a time
    # can also use "f.readlines()" or "for line in f" which keep '\n'
    lines = f.read().splitlines()  
    for line in lines[0:10]:
        print(line)

# Task 4: # Open 22nd file and read the first 10 lines



print("\nSolution 4: Open 22nd file and read the first 10 lines")
with open(lst_scripts[21]) as f:
    lines = f.readlines()  
    for line in lines[0:10]:
        print(line.strip())  # strip any white space from end of str including '\n'

# Find the docstring line in file (starts with """ or r""" or f""" or rf""" or ''' or fr''' etc)
import re  # regular expression library - see meetup074
ptn_docstring = re.compile(r"""^[fr]{0,2}['\"]{3}(.*)""")
lst_meetup = []

for script_path in lst_scripts:
    # default encoding is platform dependent
    with open(script_path, "r", encoding="UTF-8") as f:
        for line in f:
            if ptn_docstring.match(line):  # match finds at start of str
                lst_meetup.append(line.strip())
                break  # jump out of enclosing loop
print("\nFirst line in docstring for each script")
for t in lst_meetup:
    print(t)

# We have the title line, can we find the date. To parse the date it needs to be in correct format
import datetime
print("\nParsing dates from different formats")
print(datetime.datetime.strptime("24 Mar 2020", "%d %b %Y").date())
print(datetime.datetime.strptime("24th Mar 2020", "%dth %b %Y").date())

# Find the date for each session
# Pattern is
# one to two digits 
# optionally followed by two letters
# followed by a space
# followed by 3 letters
# followed by a space
# followed by 4 digits
def date_from_meetup(meetup):
    ptn_date = re.compile(r"([0-9]{1,2})([a-zA-Z]{2})? ([a-zA-Z]{3}) ([0-9]{4})")
    m = ptn_date.search(meetup)  # search finds anywhere in str
    if m:
        # full match is in group(0)
        d = m.group(1)  # match in first ()
        b = m.group(3)  # match in third ()
        y = m.group(4)  # match in fourth ()
        return datetime.datetime.strptime(f'{d} {b} {y}', '%d %b %Y').date()

print("\nDates from each meetup")
for t in lst_meetup:
    print(date_from_meetup(t))

# Task 5 use regular expression to find Youtube URL for each meetup



print("\nSolution 5: defined in a function so we can use it later")
def parse_py_lines(path_script, lst_title):
    """Find first of each title in python file"""
    first = {}
    ptn_docstring = re.compile(r"""^[fr]{0,2}['\"]{3}(.*)""")
    dct_ptn_title = {k:re.compile(k.lower() + r":(.*)") for k in lst_title}
    with open(path_script, "r", encoding="UTF-8") as f:
        for line in f:
            m = ptn_docstring.search(line)
            if "docstring" not in first and m:
                first["docstring"] = m.group(1)
            for title in lst_title:
                m = dct_ptn_title[title].search(line.lower())
                if title not in first and m:
                    # m.start gives us the index of the first char in the group
                    first[title] = line[m.start(1):].strip()
        return first

for script_path in lst_scripts:
    dct = parse_py_lines(script_path, ["Youtube"])
    print(dct)

print("\nUsing function 'parse_py_lines' to find several labelled links in first script")
print(parse_py_lines(lst_scripts[0], ["Youtube", "Colab", "Meetup", "Github"]))

# Task 6: Create a spreadsheet with columns
# Meetup, Script in sheet scripts
# Meetup, Date, Youtube, Meetup, Colab, Github, docstring in sheet links



# Solution 6
def url_last(dct, lst_title):
    """Find the last segment of the url given the dict of data from script and the list of titles in order to try to find a url"""
    ptn_url_last = re.compile(r".*/([^/]+)/?")
    for title in lst_title:
        url = dct.get(title, None)
        if url:
            break
    else:
        return None, None
    m = ptn_url_last.search(url)
    if m:
        str_last = m.group(1)
    else:
        str_last = url
    return url, str_last

with xlsxwriter.Workbook("bpaml-links-6.xlsx") as workbook:
    worksheet = workbook.add_worksheet("scripts")
    dcf_col_a = {"align": "center", "num_format": "000"}
    dcf_row_1 = {"bold": True}
    dcf_col_dt = {"align": "center", "num_format": "dd mmm yyyy"}
    fmt_col_a = workbook.add_format(dcf_col_a)
    fmt_row_1 = workbook.add_format(dcf_row_1)
    fmt_col_dt = workbook.add_format(dcf_col_dt)
    fmt_a1 = workbook.add_format({**dcf_col_a, **dcf_row_1})
    # Set column widths
    worksheet.set_column("B:B", 50)
    # Add titles
    worksheet.write("A1", "Meetup"     , fmt_a1)
    worksheet.write("B1", "Script name", fmt_row_1)
    # Add data to 
    for i, script in enumerate(lst_scripts):
        row = i + 2
        meetup = int(script.name[6:9])
        worksheet.write(f"A{row}", meetup     , fmt_col_a)
        worksheet.write(f"B{row}", script.stem)
    # Calculate total of all meetup numbers
    worksheet.write(f"A{row+2}", f"=SUM(A2:A{row})", fmt_col_a)

    worksheet = workbook.add_worksheet("links")
    worksheet.set_column("B:D", 15)
    worksheet.set_column("E:G", 45)
    
    lst_title = ["Youtube", "Meetup", "Colab", "Github", "Source"]
    worksheet.write("A1", "Meetup", fmt_a1)
    worksheet.write("B1", "Date", fmt_a1)
    for j, title in enumerate(lst_title[:4]):
        worksheet.write(0, j + 2, title, fmt_row_1)
    worksheet.write(0, j + 3, "Description", fmt_row_1)
    ptn_meetup_name = re.compile(r".* - (.*)")
    for i, script in enumerate(lst_scripts):
        meetup = int(script.name[6:9])
        dct = parse_py_lines(script, lst_title)
        dt = date_from_meetup(dct['docstring'])
        worksheet.write(i + 1, 0, int(meetup), fmt_col_a)
        worksheet.write(i + 1, 1, dt, fmt_col_dt)
        for j, title in enumerate(lst_title[:3]):
            url, str_last = url_last(dct, [title])
            if url:
                worksheet.write_url(i + 1, j + 2, url, string=str_last)
        url, str_last = url_last(dct, [lst_title[4], lst_title[3]])
        if url:
            worksheet.write_url(i + 1, j + 3, url, string=str_last)
        m = ptn_meetup_name.search(dct["docstring"])
        if m:
            worksheet.write(i + 1, j + 4, m.group(1))

