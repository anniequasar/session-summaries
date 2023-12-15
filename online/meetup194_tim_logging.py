#!/usr/bin/env python3
r"""
# MeetUp 194 - Beginners' Python and Machine Learning -  29 Nov 2023 and 06 Dec 2023 - Logging

Learning objectives:
- How to use logging and loggers
- How to configure logging
- Logging handlers
- bash redirections to stdout, stderr and files

Links:
- Colab:   https://colab.research.google.com/drive/1T6EZenMYY6SdcY9BuEsbwWedjFIMYoyG
- Youtube: https://youtu.be/fojZ1RVyCNw
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/297274786/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

References:

- Python howto: https://docs.python.org/3/howto/logging.html
- Python logging config: https://docs.python.org/3/library/logging.config.html
- Python cookbook: https://docs.python.org/3/howto/logging-cookbook.html
- Logging in colab: https://colab.research.google.com/github/aviadr1/learn-advanced-python/blob/master/content/15_logging/logging_in_python.ipynb

# Mac or Linux - zsh or bash - Setup virtual environment to isolate this project from other projects
python3 -m venv venv194
source venv194/bin/activate

# Windows CMD - Setup virtual environment to isolate this project from other projects
py -m venv venv194
venv194\Scripts\Activate.bat

# Update pip and setuptools
pip list
pip install -U pip setuptools
pip list

# Install third party library logging_tree so we can see how logging is configured
pip install logging_tree

# Run script. Because in virtual environment, can use python or python3
python meetup194_tim_logging.py

# At the end of script output are instructions for running in demo mode by adding demo argument for this script
python meetup194_tim_logging.py demo

# Logging

Output messages during the running of code to track issues in data or code.
"""
# Standard libraries
import json
import logging
import logging.config
import os
import sys
# Third party library
import logging_tree
# Set up a couple of constants for later use
LOG_CONFIG = "logging-config.json"
LOG_CONFIG_WITH_FILTER = "logging-config-with-filter.json"



# Before we start, check if we are running demo mode for short demo program that you can run yourself
# For now just skip to END DEMO below
def filter_maker(level):
    # function filter_maker must be defined before calling logging.dictConfig with a filter
    level = getattr(logging, level)
    def filter(record):
        return record.levelno <= level
    return filter


if sys.argv[-1] == 'demo':
    with open(LOG_CONFIG_WITH_FILTER) as f:
        logging.config.dictConfig(json.load(f))
    logger = logging.getLogger(__name__)
    if logger.isEnabledFor(logging.DEBUG):
        logging_tree.printout()
    logger.debug(f'This is my 😂 debug message')
    logger.info(f'This is my 💜 info message ')
    logger.warning(f'This is my 🤔 warning message')
    logger.error(f'This is my error 😱message')
    logger.critical(f'This is my 😭 critical message')
    sys.exit()

#
# END DEMO
#

print("# Can log with print() function")
for i in range(5):
    print("in for loop")
    if i == 5:
        print("We are waiting for i to get to 5 to do an important task")

print("# Doesn't tell us much other than i doesn't get to 5")

print("\n# Can log with print() function and f-strings")
print("# especially self-documenting f-string expressions {i=}")
for i in range(5):
    print(f"in for loop {i=}")
    if i == 5:
        print("We are waiting for i to get to 5 to do an important task")

print("# We can see from the output that range(5) goes from 0 to 4")

print("\n# The problem with print statements is that once you have solved the problem you have to delete them.")
print("# Introduce logging which can be turned on and off easily")
print("# Should only ever call basicConfig once. If need to call a second time use force=True")
print("# in colab need to set force=True because colab setup must call it itself")
logging.basicConfig(force=True)

def when_three():
    for i in range(5):
        logging.warning(f"in for loop {i=}")
        if i == 3:
            logging.error("We are waiting for i to get to 3 to do an important task")

when_three()

print("\n# There are 6 predefined logging levels which are just ints.")
print(f"{logging.NOTSET=}")
print(f"{logging.DEBUG=}")
print(f"{logging.INFO=}")
print(f"{logging.WARNING=}")
print(f"{logging.ERROR=}")
print(f"{logging.CRITICAL=}")

print("\n# Challenge 1: Rewrite when_three to log at debug level in loop and info level when i==3")
print("# Solution 1:")
def when_three():
    for i in range(5):
        logging.debug(f"in for loop {i=}")
        if i == 3:
            logging.info("We are waiting for i to get to 3 to do an important task")

when_three()

print("\n# No output. But we can change the log level to DEBUG")
logging.basicConfig(force=True, level=logging.DEBUG)
when_three()

# Remember - you wouldn't normally re-call logging.basicConfig
# basicConfig is for initial settings
print("\n# Change level to INFO")
logging.basicConfig(force=True, level=logging.INFO)
when_three()

print('\n# can log to a file. filemode can be "a" (append) (default) "w" (overwrite)')
print("\n# force=True removes existing handlers (console) but doesn't change level")
logging.basicConfig(filename="log-file.log", filemode="w", force=True)
when_three()
logging.warning("script finished")

print("cat log-file.log  # run this command in bash to see contents of log-file.log")
print("type log-file.log  # run this command in Windows cmd to see contents of log-file.log")


# Let's make our own cat function in Python
def cat(filename):
    print(f"\nDisplaying contents of file {filename} using Python")
    with open(filename) as f:
        print(f.read())


cat("log-file.log")

# set level back to WARNING (which is the default) and remove existing handlers
logging.basicConfig(force=True, level=logging.WARNING)

print("\n# Can create more levels if you need another level e.g. trace")
for ll in range(1, 33):
    logging.log(ll, f"Logging at level {ll}")

print("\n# Individual loggers - can create loggers with different names")
print("# Notice how logger name is in log output")
logger = logging.getLogger('my_logger')
logger.debug(f'This is my 😂 debug message')
logger.info(f'This is my 💜 info message ')
logger.warning(f'This is my 🤔 warning message ')
logger.error(f'This is my error 😱message ')
logger.critical(f'This is my 😭 critical message ')

print("\n# Typical design pattern is to create a logger in every module")
print("# Use python special property __name__ to get the name of the current module or __main__ if called in the main module.")
logger = logging.getLogger(__name__)
logger.warning(f"Using logger {__name__}")

print("\n# Challenge 2: Rewrite when_three using a named logger other than the root logger")
print("# Solution 2:")
def when_three():
    for i in range(5):
        logger.debug(f"in for loop {i=}")
        if i == 3:
            logger.info("We are waiting for i to get to 3 to do an important task")

when_three()
print("\n# Each named logger can be set to a different log level")
logger.setLevel(logging.DEBUG)
when_three()

print("\n# Logging an exception - full stack trace when set exc_info=True")
try:
    exceptional_calc = 1/0
except ZeroDivisionError as e:
    logger.error("Wow! Something really went wrong.", exc_info=True)

print("""
## Summary

The only things you need to remember when writing code are

1. Every module create a logger using `logger = logging.getLogger(__name__)`
2. Pepper your code with log statements of different levels based on how important logging is:
    1. Critical if statement is about to terminate your application
    2. Error if there is something gone seriously wrong but you can recover from
    3. Warning if there is some issue that is possible to cause another problem later on.
    4. Info for information which may help someone understanding what is going on
    5. Debug for verbose output that you couldn't run all the time for fear of creating huge log files but is necessary for debugging code.
3. Include stack traces in logs if they will help using `exc_info=True`

---
## Configuring logging

Configuring logging you will usually only do once when writing or deploying application so you are unlikely to remember how to do it. Three ways of configuring logging
- **basicConfig**: used for simple demos
- **fileConfig**: uses config.ini type file based configuration. File based configuration allows devops to configure logging rather than developer. The config.ini format doesn't allow full range of configurations so no longer recommended
- **dictConfig**: most flexible form of configuration. Can be used with files or in code or network configuration Schema at <https://docs.python.org/3/library/logging.config.html#logging-config-dictschema>

Schema summary
- formatters
- filters
- handlers
- loggers
- root
- incremental  (default False)
- disable_existing_loggers  (default True)

When creating a formatter, use any of LogRecord's attributes <https://docs.python.org/3/library/logging.html#logrecord-attributes>
""")

print("\n# config which doesn't disable existing loggers but does replace existing handlers")
print("# You wouldn't normally create a dict to create json to create config file")
print("# Normally create json config file, then read in and convert to dict and then apply config")
print("# To use SMTP I setup a Postfix satellite on localhost (which is ubuntu)")
d = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "S {asctime} - {levelname:10s} - {name} - {message}", "style": "{"},
        "error": {"format": "E {asctime} - {levelname:10s} - {name} - {message}", "style": "{"},
    },
    "handlers": {
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1000,
            "backupCount": 3,
            "filename": "bpaml194.log",
            "formatter": "standard",
            "level": "INFO"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        },
        "stderror": {
            "class": "logging.StreamHandler",
            "formatter": "error",
            "level": "WARNING",
            "stream": "ext://sys.stderr"
        },
        "email": {
            "class": "logging.handlers.SMTPHandler",
            "formatter": "standard",
            "level": "ERROR",
            "mailhost": ["localhost", 25],
            "fromaddr": "logger@mydomain.com",
            "toaddrs": ["pythonatordev@gmail.com"],
            "subject": "Logged errors"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["file_handler", "console", "stderror"]
    },
    "loggers": {"my_logger": {"level": "DEBUG", "handlers": ["file_handler", "console", "stderror"]}}
}
with open(LOG_CONFIG, "w") as f:
    json.dump(d, f, indent=2)
cat(LOG_CONFIG)

# Now read config file and convert to dict
with open(LOG_CONFIG, "rb") as f:
    logging.config.dictConfig(json.load(f))

print("\n# logging_tree")
logging_tree.printout()

print("\n# Challenge 3: Send info and debug logs to the root logger and to my_logger")
print("# Check the logs in the file bpaml194.log")
print("# Work out why there are duplications")
print("# Solution 3")
root_logger = logging.getLogger()
my_logger = logging.getLogger("my_logger")
root_logger.debug("A debug from root")
root_logger.info("An info from root")
my_logger.debug("A debug from my_logger")
my_logger.info("An info from my_logger")
cat("bpaml194.log")

print("\n# We are getting duplications because we have handlers on both my_logger and root and my_logger propagates to root.")
print('# Propagation follows names with dots my_logger.sub -> my_logger -> "" (root)')
print("# This works well for python modules in packages")
print("# Remove the handlers (normally do this in the config file)")
while len(my_logger.handlers) > 0:
    my_logger.removeHandler(my_logger.handlers[-1])

print("\n# Test by rerunning")
root_logger.debug("A debug from root")
root_logger.info("An info from root")
my_logger.debug("A debug from my_logger")
my_logger.info("An info from my_logger")
cat("bpaml194.log")


print("\n# Challenge 4: Send a warning log to root logger and to my_logger")
print("# Solution 4")
root_logger.warning("A warning from root")
my_logger.warning("A warning from my_logger")

print("\n# The duplicates now have different formatters (first character S or E)")
print("# We have two handlers sending to the same place - the console (stdout and stderr)")
print("# We want stdout to not get warning or above. Need to create a filter")

print("""\n### How to create a handler which handles everything below a certain level

For example:
- stdout handles DEBUG and INFO
- stderr handles WARNING and ERROR and CRITICAL

Creating a function filter_maker as described at
https://docs.python.org/3/howto/logging-cookbook.html#custom-handling-of-levels

We have included this function at the start in the demo section so it can also be used by demo
""")

# The Google Colab notebook shows how to create config files using bash. This script shows how create config files using Python.
# # Create a json config file using bash rather than python
# # < take stdin from file
# # > send stdout to new file
# # >> send stdout to existing file (appends)
# # 2> send stderr to new file
# # 2>> send stderr to existing file (appends)
# # <<EOF ... EOF  # take heredoc for multiline files. EOF can be any delimiter not in file. Can use environment variables. Need to escape $
# # | pipe stdout from one application to stdin for another
# # cat is an executable which
# # tee is an application which takes one input (stdin) and has two outputs with same content (file and stdout)
d = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "oformat": {"format": "O %(levelname)-8s - %(message)s"},
        "eformat": {"format": "E %(levelname)-8s - %(message)s"}
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "oformat",
            "stream": "ext://sys.stdout",
            "filters": ["info_and_below"]
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "eformat",
            "stream": "ext://sys.stderr"
        }
    },
    "filters": {
        "info_and_below": {
            "()" : "__main__.filter_maker",
            "level": "INFO"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "stderr",
            "stdout"
        ]
    }
}
with open(LOG_CONFIG_WITH_FILTER, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2)
cat(LOG_CONFIG_WITH_FILTER)


print("\n# Using the filter we can see that the duplication problem is fixed")
with open(LOG_CONFIG_WITH_FILTER, "rb") as f:
    logging.config.dictConfig(json.load(f))
my_logger.info("An info from my_logger")
my_logger.critical("A critical from my_logger")

print("\n# Running built in demo in this script using python. Both stdout and stderr will go to console")
print("# Equivalent to running `python meetup194_tim_logging.py demo`")
# It is not common to call python scripts from python this way but useful in special cases such as this (calling itself with arguments). Usually use import
os.system('python meetup194_tim_logging.py demo')

print("\n# Challenge 5 - Change root logger to INFO not DEBUG")
print("# Solution 5 - Best is to edit config file directly but here is solution using python")
d["root"]["level"] = "INFO"
with open(LOG_CONFIG_WITH_FILTER, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2)
cat(LOG_CONFIG_WITH_FILTER)

print("\n# Now run demo built in this script from the command line with logging configured to have INFO level. Both stdout and stderr will go to console")
print("python meetup194_tim_logging.py demo")

print("\n# Redirect stdout to a new file (overwrite with >) but leave stderr going to console")
print("python meetup194_tim_logging.py demo >demo-stdout.txt")

print("\n# Check contents of file - Mac or Linux - bash or zsh")
print("cat demo-stdout.txt")

print("\n# Check contents of file - Windows CMD")
print("type demo-stdout.txt")

print("\n# Redirect stdout and stderr to different files (appending with >>)")
print("python meetup194_tim_logging.py demo >>demo-stdout.txt 2>>demo-stderr.txt")

print("\n# Redirect stderr to where stdout is currently going (to pipe)")
print("# Then redirect stdout to file demo-stdout.txt")
print("# Then pipe into stdin of tee to create teed-stderr.txt")
print("python meetup194_tim_logging.py demo 2>&1 >>demo-stdout.txt | tee teed-stderr.txt")

print("\n# Check contents of files - Mac or Linux - bash or zsh")
print("cat demo-stdout.txt")
print("cat demo-stderr.txt")
print("cat teed-stderr.txt")

print("\n# Check contents of files - Windows CMD")
print("type demo-stdout.txt")
print("type demo-stderr.txt")
print("type teed-stderr.txt")
