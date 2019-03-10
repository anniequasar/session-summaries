"""
Modules - Beginners Python Session 10

Demonstrates how program can tell if it has been run as script or imported as module

@author: Tim Cummings

Every python program file is a module.

A module is a group of python functions, classes, and/or a program which can be used from other python programs.

The module name is the file name less the .py suffix.


Other programs use the 'import' statement to use the module.

'import' runs the python program and makes available functions and classes

Note: make sure all code is in function definitions if you don't want it to run on import.
"""

# Challenge 1: Create a python program which prints the value of variable __name__

# Advanced challenge 1: print the value of variable __name__ using logging

print("__name__ has value {}".format(__name__))



# Challenge 2: Run the python program and see what value gets printed.

# Import as a module and see what gets printed



# script: __name__ has value __main__

# import: __name__ has value s10a_module



# Challenge 3: Detect whether program has been run as a script or imported as a module and

# display a different message for each case



if __name__ == "__main__":

    print("I have been run as a script")

else:

    print("I have been imported as a module and my name is {}".format(__name__))
