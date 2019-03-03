"""
Modules - Beginners Python Session 10b

Demonstrates defining functions in a module that are only called if module is run as a script

@author: Tim Cummings
"""

# Challenge 4: Add three functions to your python program / module. Name one of the functions main().

# Other two functions can be anything eg time left in session and convert celsius to fahrenheit

# main() is to run if program is run as a script but not if imported as a module.

# main() can call other two functions


import logging

import datetime


def td_time_left():

    """Calculate time from now until 8pm tonight and return it as a datetime.timedelta"""

    time_finish = datetime.datetime.combine(datetime.datetime.today(), datetime.time(hour=20))

    time_now = datetime.datetime.now()

    time_delta = time_finish - time_now

    logging.debug("Time left in session is {} (hh:mm:ss.ssssss)".format(time_delta))

    return time_delta


def flt_f_from_c(c):

    """Returns the temperature in Fahrenheit given the temperature in Celsius"""

    try:

        f = c * 1.8 + 32

        logging.debug("Celsius {:.2f}, Farhenheit {:.2f}".format(c, f))

        return f

    except (TypeError, ValueError):

        # exc_info=True outputs a stack trace

        logging.error("flt_f_from_c({!r})".format(c), exc_info=True)



def main():

    """This main function runs only if this module is run as a script, not if imported"""

    logging.debug("Module run as a script, not imported")

    print("Time left {}".format(td_time_left()))

    print("Temperature {:.2f}°C is equivalent to {:.2f}°F".format(0, flt_f_from_c(0)))

    print("Temperature {:.2f}°C is equivalent to {:.2f}°F".format(100, flt_f_from_c(100)))

    print("Temperature {:.2f}°C is equivalent to {:.2f}°F".format(-40, flt_f_from_c(-40)))



if __name__ == "__main__":

    main()

else:

    logging.debug("Module has been imported so it's name is {}".format(__name__))
