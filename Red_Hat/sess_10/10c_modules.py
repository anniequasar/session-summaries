"""
Modules - Beginners Python Session 10c

Demonstrates importing your own module in another module.

@author: Tim Cummings
"""

# Challenge 5: Write a python program which imports the module created earlier

# and calls the functions other than main().


import logging

logging.getLogger().setLevel(logging.DEBUG)


import 10b_modules

from 10b_modules import flt_f_from_c as fc


print(fc(28))

10b_modules.main()


# Challenge 6: Make sure your python scripts are using a combination of printing and logging.

# Run the scripts from the command line and notice the order the logging and printing combine.


# python 10c_modules.py


# Challenge 7: Run scripts from the command line sending the standard output of the script to a file

# and yet logging/standard error output goes to screen


# python 10c_modules.py > s10c_out.txt


# Challenge 8: Run scripts from the command line sending the print output to one file and the logging output to a different file.


# python 10c_modules.py > s10c_out.txt 2> s10c_err.txt


# Challenge 9: Run scripts from the command line sending the print output to one file and the logging output to the same file.


# python 10c_modules.py > s10c_out.txt 2>&1


# Challenge 9: Run scripts from the command line APPENDING the print output to one file and the logging output to the same file.


# python 10c_modules.py >> s10c_out.txt 2>&
