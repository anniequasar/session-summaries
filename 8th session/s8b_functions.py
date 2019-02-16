# -*- coding: utf-8 -*-
"""
Functions - Beginners Python Session 8 - s8b_function.py

@author: Tim Cummings

Demonstrates: Logging, Exceptions, Testing

"""
import logging
import datetime
import decimal

# Can be useful to include logging in function
# Challenge set logging level to DEBUG and confirm that logging output
logging.basicConfig(level=logging.DEBUG)     # plain python, PyCharm
logging.getLogger().setLevel(logging.DEBUG)  # Spyder, Jupyter, PyCharm, probably plain Python too

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")


# Challenge: Add logging to td_time_left and dt_same_time_tomorrow
def td_time_left():
    """Calculate time from now until 8pm tonight and return it as a datetime.timedelta"""
    time_finish = datetime.datetime.combine(datetime.datetime.today(), datetime.time(hour=20))
    time_now = datetime.datetime.now()
    time_delta = time_finish - time_now
    logging.debug("Time left in session is {} (hh:mm:ss.ssssss)".format(time_delta))
    return time_delta


def dt_same_time_tomorrow():
    """Returns the date and time one day after this function is called"""
    time_today = datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    time_tomorrow = time_today + one_day
    logging.debug("Time now {}, same time tomorrow {}".format(time_today, time_tomorrow))
    return time_tomorrow


td_time_left()
dt_same_time_tomorrow()


# Log at ERROR level if an exception. Otherwise log at DEBUG level
def flt_f_from_c(c):
    """Returns the temperature in Fahrenheit given the temperature in Celsius"""
    try:
        f = c * 1.8 + 32
        logging.debug("Celsius {:.2f}, Farhenheit {:.2f}".format(c, f))
        return f
    except TypeError:
        # exc_info=True outputs a stack trace
        logging.error("flt_f_from_c({!r})".format(c), exc_info=True)


flt_f_from_c(0)
flt_f_from_c(100)
flt_f_from_c(-40)
flt_f_from_c("20°C")


# Challenge: error level log if price_incl_gst throws an exception, otherwise debug level
def price_incl_gst(price_excl_gst, gst_rate=0.1):
    """Calculates price including GST

    Parameters
    ----------
    price_excl_gst : decimal.Decimal or float or int or str
        The price excluding GST
    gst_rate : decimal.Decimal or float or int or str
        The GST rate as a fraction (not a percent). gst_rate=0.1 is equivalent to a GST rate of 10%

    Returns
    -------
    decimal.Decimal
        The price including GST

    Raises
    ------
    decimal.InvalidOperation
        If either price_excl_gst or gst_rate is a str which cannot go to decimal.Decimal eg "one"
    TypeError
        If either price_excl_gst or gst_rate is a type which cannot go to decimal.Decimal eg {1}
    ValueError
        If either price_excl_gst or gst_rate is a value which cannot go to decimal.Decimal eg [1]
    """
    try:
        lcl_price_incl_gst = round(decimal.Decimal(price_excl_gst) * decimal.Decimal(1 + gst_rate), 2)
        logging.debug("price_incl_gst(price_excl_gst={!r}, gst_rate={!r}) -> {!r}".format(price_excl_gst, gst_rate, lcl_price_incl_gst))
        return lcl_price_incl_gst
    except (ValueError, TypeError, decimal.InvalidOperation) as e:
        # we are only catching 3 exception types. To catch all use 'except Exception as e:'
        # logging.exception can only be called within 'except' code block
        logging.exception("Here is the stack trace")
        # format strings !r equivalent to caling repr(value)
        logging.error("price_incl_gst(price_excl_gst={!r}, gst_rate={!r}) produces exception {!r}"
                      .format(price_excl_gst, gst_rate, e))
        # re-raise the exception if you don't want to swallow it
        raise e


# Challenge: Modify test_price_incl_gst to ensure correct exceptions are raised.
# Hint: Can't use assert. Can use python's built-in exception handling
# Hint: Can raise an AssertionError the same as if assert had failed
def test_price_incl_gst():
    D = decimal.Decimal
    assert price_incl_gst(10) == D("11")
    assert price_incl_gst(0) == 0
    assert price_incl_gst(-2.2, 0.1) == D("-2.42")
    assert price_incl_gst(D("1.1")) == D("1.21")
    assert price_incl_gst(D("1.10")) == D("1.21")
    assert price_incl_gst(D("1.1"), D("0.15")) == D("1.26")
    # When calling a function you can supply parameters in a different order by using their names
    assert price_incl_gst(gst_rate=D("0.15"), price_excl_gst=D("1.1")) == D("1.26")
    # When calling a function you can supply parameters by expanding a list of the parameters
    my_list = [12.345, 0.125]
    assert price_incl_gst(*my_list) == D("13.89")
    # When calling a function you can supply parameters by expanding a dict of the named parameters
    my_dict = {'gst_rate': 1/3, 'price_excl_gst': 6.0}
    assert price_incl_gst(**my_dict) == D("8.00")
    try:
        price_incl_gst("one")
        raise AssertionError('price_incl_gst("one") should raise a decimal.InvalidOperation exception but raised nothing')
    except decimal.InvalidOperation:
        pass
    except Exception as e:
        raise AssertionError('price_incl_gst("one") should raise a decimal.InvalidOperation exception but raised {!r}'.format(e))
    try:
        price_incl_gst({1})
        raise AssertionError('price_incl_gst({1}) should raise a TypeError exception but raised nothing')
    except TypeError:
        pass
    except Exception as e:
        raise AssertionError('price_incl_gst({{1}}) should raise a TypeError but raised {!r}'.format(e))
    try:
        price_incl_gst([1])
        raise AssertionError('price_incl_gst([1]) should raise a ValueError exception but raised nothing')
    except ValueError:
        pass
    except Exception as e:
        raise AssertionError('price_incl_gst([1]) should raise a ValueError but raised {!r}'.format(e))


test_price_incl_gst()
