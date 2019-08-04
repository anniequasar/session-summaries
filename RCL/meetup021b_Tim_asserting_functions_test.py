"""
MeetUp 021b - Beginners Python Support Sessions 30-Jul-2019

Learning objectives:
    Testing functions with assert and pytest

@author D Tim Cummings
"""
from mu021a_asserting_functions import is_leap_year, is_leap_year_3, is_leap_year_1
import pytest


# Challenge 8: Create "tests" folder in your project and add a python module called test_your_module.py. In this module
# create a function test_is_leap_year() which asserts the above. Run pytests from your project directory.
# Create run configuration to run automatically
@pytest.mark.filterwarnings("ignore:bad400")
def test_is_leap_year_3():
    assert is_leap_year_3(2016)
    assert not is_leap_year_3(2019)
    assert is_leap_year(2000)
    assert not is_leap_year_3(1900)


# Challenge 9: Change test function to use parameters (year, result). Use @pytest.mark.parametrize to provide parameters
@pytest.mark.parametrize(
    ("year", "result"),
    (
            (2016, True),
            (2019, False),
            (2000, True),
            (1900, False),
    )
)
def test_is_leap_year(year, result):
    print("Testing", year, result)
    assert is_leap_year(year) is result
