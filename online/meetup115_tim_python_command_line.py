#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MeetUp 115 - Beginners' Python and Machine Learning - 14 Sep 2021 - Run Python scripts from the command line

Youtube: https://youtu.be/0Uf_RTLycnQ
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/280569331/
Github:  https://github.com/anniequasar/session-summaries.git

Learning objectives:
- Create virtual environment
- Run Python scripts from the command line
- Redirect input to and output from a Python script
- Parse command line arguments

Prerequisites:
- Need to have python 3.7 or later installed on your computer from python.org or anaconda.com

@author D Tim Cummings

# Task 1. Running python3 console from command line
python3     # Mac and Linux
python.exe  # Windows if it is on your PATH
py.exe      # This is the Python launcher on Windows. It is always on PATH

# Task 2. Create a virtual environment
# Windows
py -m venv venv115
venv115\Scripts\activate

# Mac or Linux
python3 -m venv venv115
source venv115/bin/activate

# Anaconda
conda create --name venv115 python  # run from shell launched with conda
conda activate venv115

# Task 3. Create a simple python script that prints out the value of __name__
notepad my_name.py  # Windows
nano my_name.py     # Mac or Linux

print(f"My name is {__name__}")

# Task 4. Run as a script
py my_name.py       # Windows
python3 my_name.py  # Mac or Linux

# Task 5. Run python console and import as an alternative way of running script
py
python3
import my_name
import my_name

# Task 6. Use importlib to import more than once
import importlib
importlib.reload(my_name)

# Task 7. Posix command line has a flexible way of linking file to executable called shebang

#! /usr/bin/env python3

# This is the most versatile form because it references PATH in system environment and virtual environment
# Substitute python3 with python3.6 or python2 etc for specific versions of python
# On Windows python launcher py will parse shebang line

# On Unix make sure file is executable
chmod +x my_name.py
./my_name.py

# Might find that you can double click on file although window will disappear quickly after running
# ./ required on Unix because normally current directory is not on PATH.
# DOS and Windows have current directory on PATH. Powershell may not have current directory on PATH

# Task 8. Command line has ability to redirect input and output and use piping.
#!/usr/bin/env python3
import logging
import sys
print(f"My name is {__name__}")
logging.warning(f"Python version is {sys.version}")

./my_name.py > my_name.txt  # create new file with output
./my_name.py >> my_name.txt  # append to existing file
./my_name.py > my_name.txt 2> my_name.log  # capture stdout and stderr

notepad in_reader.py

#!/usr/bin/env python3
import sys
print(f"My arguments are {sys.argv}")
for line in sys.stdin:
    print(line[::-1])

type my_name.log | py in_reader.py    # windows
cat my_name.log | ./in_reader.py   # unix

# Task 9. Only running code if run as script, not imported as module

#!/usr/bin/env python3
import sys
if __name__ == "__main__":
    print(f"Running {sys.argv[0]} as script")
else:
    print(f"Importing {__name__}")

# Task 10. command line arguments
notepad arg_reader.py

#!/usr/bin/env python3
import sys
print(f"My arguments are {sys.argv}")
if __name__ == "__main__":
    for i, a in enumerate(sys.argv):
        print(f"{i}: argument {a} has type {type(a)}")

arg_reader.py one 2 three "[four]" f i v e
arg_reader.py -h -vv --log info

# Task 11. Using argparse. See meetup110_tim_virtual_printer.py and this file for use case
notepad num_words.py

#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()

num_words.py --help
num_words.py -h
num_words.py 213

# Task 12. Add positional argument using parser.add_argument("number")

# Solution 12: Also shows how to retrieve arguments and convert them to int
#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser(description="MeetUp115 Running Python from Command Line - convert number to words")
parser.add_argument("number", help="Number in digits to be converted to words eg 123", type=int)
args = parser.parse_args()
print(f"{args.number=} which has {type(args.number)=}")

# Task 13. Looking at code for meetup 110, accept an optional parameter for log level

# Solution 13. Shows how to accept log level in upper case or lower case, and how to provide short form of arg name
#!/usr/bin/env python3
import argparse
import logging
parser = argparse.ArgumentParser(description="MeetUp115 Running Python from Command Line - convert number to words")
parser.add_argument("number", help="Number in digits to be converted to words eg 123", type=int)
parser.add_argument("-l", "--log", default="INFO", action="store", help="set log level. eg: --log INFO", type=str.upper,
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
args = parser.parse_args()
numeric_level = getattr(logging, args.log, None)
logging.basicConfig(level=numeric_level, format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")
logging.info(f"{args.number=} which has {type(args.number)=}")
print(args.number)

# Task 14. Add an argument to output results in upper case

# Solution 14. Shows how to use an optional argument name which doesn't need an argument value
#!/usr/bin/env python3
import argparse
import logging
parser = argparse.ArgumentParser(description="MeetUp115 Running Python from Command Line - convert number to words")
parser.add_argument("number", help="Number in digits to be converted to words eg 123", type=int)
parser.add_argument("-l", "--log", default="INFO", action="store", help="set log level. eg: --log INFO", type=str.upper,
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
parser.add_argument("-u", "--upper", action="store_true", help="Return results in upper case, otherwise lower case")
args = parser.parse_args()
numeric_level = getattr(logging, args.log, None)
logging.basicConfig(level=numeric_level, format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")
logging.info(f"{args.number=} which has {type(args.number)=}")
if args.upper:
    print(args.number, "in upper case")
else:
    print(args.number, "in lower case")
"""
import argparse
import logging

numbers = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
           "nineteen", "twenty")
tens = {20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'}
powers = {1000000000000: "trillion", 1000000000: "billion", 1000000: "million", 1000: "thousand", 100: "hundred"}


def number_name(number: int) -> str:
    """Returns the name of any integer between 0 and 1 trillion - see meetup 102"""
    logger.debug(f"number_name({number})")
    s = ""
    # dicts retain order since Python 3.6
    for power, name in powers.items():
        count = number // power
        if count > 0:
            # recursive call of number_name from within number_name
            s += f"{number_name(count)} {name} "
            number -= count * power
    if s != "" and number > 0:
        conjunction = "and "
    else:
        conjunction = ""
    right = number % 10
    left = number - right
    if number == 0 and s != "":
        return s
    elif number < len(numbers):
        return s + conjunction + numbers[number]
    elif right == 0:
        return s + conjunction + tens[left]
    else:
        return s + conjunction + tens[left] + "-" + numbers[right]


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MeetUp115 Running Python from Command Line - convert number to words")
    parser.add_argument("number", help="Number in digits to be converted to words eg 123", type=int)
    parser.add_argument("-l", "--log", default="INFO", action="store", help="set log level. eg: --log INFO",
                        type=str.upper, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    parser.add_argument("-u", "--upper", action="store_true", help="Return results in upper case, otherwise lower case")
    args = parser.parse_args()
    numeric_level = getattr(logging, args.log, None)
    logging.basicConfig(level=numeric_level, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')
    logger.debug(f"{args=}")
    if args.upper:
        print(number_name(args.number).upper())
    else:
        print(number_name(args.number))
else:
    logger.debug(f"{__name__} was imported")
