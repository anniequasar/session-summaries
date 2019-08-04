"""
MeetUp 021a - Beginners Python Support Sessions 30-Jul-2019

Learning objectives:
    Testing functions with assert and pytest
    Variable scope in functions

@author D Tim Cummings

Challenge 1: Write a function is_leap_year(year) which returns True if year is divisible by 4, otherwise False

Challenge 2: Assert that 2016 is divisible by 4 and that 2019 is not

Challenge 3: Assert that 1900 is not a leap year. Fix function so it returns the correct result for 1900

Challenge 4: Assert that 2000 is a leap year. Don't fix function yet

Challenge 5: Prevent asserts running all the time, only when called

Challenge 6: Only run asserts if module is run as a script, not if imported. When run as a script __name__ == "__main__"

Challenge 7: Add pytest to your virtual environment
Add pytest to requirements.txt

Challenge 8: Create "tests" folder in your project and add a python module called test_your_module.py. In this module
create a function test_is_leap_year() which asserts the above. Run pytests from your project directory.
Create run configuration to run automatically

Challenge 9: Change test function to use parameters (year, result). Use @pytest.mark.parametrize to provide parameters

Demo: Show sas-select tests, conftest.py, with pytest.raises, with app.app_context

Challenge 10: Variable scope: Create a global variable my_global and a function which displays the value of my_global.

Challenge 11: Create a function to assign a new value to my_global and display its value.
Display value my_global after calling function.

Challenge 12: Create a function to increment value of my_global by one (try keyword global).

Challenge 13: Create nested functions and refer to variable from outer function in inner function. (try keyword nonlocal)

Challenge 14: Create a triple nested function and see whether nonlocal refers to one level up or all levels up

Challenge 15: Create a function with one argument which has a default which is a dictionary e.g. {'key': 5}
Function doubles the value associated with 'key' and returns the modified dictionary. Test
    assert double_key() == {'key': 10}
    assert double_key() == {'key': 10}  # this may fail even though first time passed


"""


# Challenge 1: Write a function is_leap_year(year) which returns True if year is divisible by 4, otherwise False
def is_leap_year_1(year):
    return year % 4 == 0


# Challenge 2: Assert that 2016 is divisible by 4 and that 2019 is not
assert is_leap_year_1(2016)
assert not is_leap_year_1(2019)


# Challenge 3: Assert that 1900 is not a leap year. Fix function so it returns the correct result for 1900
def is_leap_year_3(year):
    warnings.warn(UserWarning("bad400 does not work every 400 years"))
    if year % 100 == 0:
        return False
    return year % 4 == 0


# assert not is_leap_year_3(1900)


# Challenge 4: Assert that 2000 is a leap year. Don't fix function yet
# assert is_leap_year_3(2000)


# Challenge 5: Prevent asserts running all the time, only when called
def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


def check_is_leap_year():
    assert is_leap_year(2016)
    assert not is_leap_year(2019)
    assert is_leap_year(2000)
    assert not is_leap_year(1900)
    print("All tests passed")


# Challenge 6: Only run asserts if module is run as a script, not imported. When run as a script __name__ == "__main__"
if __name__ == "__main__":
    check_is_leap_year()
