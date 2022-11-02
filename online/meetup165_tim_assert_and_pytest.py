r"""MeetUp 165 - Beginners' Python and Machine Learning - 16 Nov 2022 - Testing

Colab:   https://colab.research.google.com/drive/1R_G45QGwBj-k_h-ZUZU9RsdalMcjj3pO
Youtube: https://youtu.be/EGDKE-RG1iQ
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/289491070/
Github:  https://github.com/timcu/session-summaries/tree/master/online

Learning objectives:
- Automatic testing of Python code
- Test driven development

@author D Tim Cummings

When you write code you check that it is correct for the current environment. But sometimes a future change can result in your function no longer operating correctly. Such changes include:
- updated libraries
- updated python version
- changes in your application such as 
  - other modules
  - other functions
  - changed variable datatypes 

If you have automated tests, after any such change, you can quickly retest your code to ensure everything is still functioning. 

Testing has proved such a successful way of writing robust, reliable code that a common paradigm now is "Test-driven Development" in which the tests are written before the code and the code can be signed off as successfully completed when all the tests pass.

Install Software
- Use a Google account to go to https://colab.research.google.com
 - Doesn't need Python installed on your computer
 - Great for interactive use and data science
 - Not so good for scripting and building apps
- Install Python 3.11.0 from https://www.python.org/downloads/
 - Python 3.7.15 or later will work
 - necessary for running python on your computer
 - alternatively can install anaconda which includes many third party libraries
- Optional: PyCharm Community Edition 2022.2.3 from https://www.jetbrains.com/pycharm/download/
 - Integrated Development Environment (IDE)
 - Easier to write programs
"""

# Challenge 1: Write a function is_leap_year(year) which returns True if year is divisible by 4, otherwise False

# Solution 1
def is_leap_year_1(year):
    return year % 4 == 0

# Check it works
print("Check Solution 1")
print(f"is_leap_year_1(2022)={is_leap_year_1(2022)}")
print(f"is_leap_year_1(2020)={is_leap_year_1(2020)}")

# Check it works programmatically
if is_leap_year_1(2020):
    print("function worked")
else:
    print("function didn't work")

# Check it works programmatically with exception if doesn't work
# otherwise have to manually check all print output
# (change one expected result to trigger exception)
print("\nChecking and raising exceptions if failed")
for (year, tf_leap) in [(2022, False), (2020, True), (2000, True)]:
    if tf_leap != is_leap_year_1(year):
        raise AssertionError(f"is_leap_year_1 didn't work for {year}. Should be {tf_leap}. Actual {is_leap_year_1(year)}")
    print(f"function correctly returned {is_leap_year_1(year)} for {year}")

# use python's assert keyword to achieve the same thing. Normally don't supply optional assertion message
print("\nUsing assert")
for (year, tf_leap) in [(2022, False), (2020, True), (2000, True)]:
    assert tf_leap == is_leap_year_1(year), f"is_leap_year_1 didn't work for {year}. Should be {tf_leap}. Actual {is_leap_year_1(year)}"
    print(f"function correctly returned {is_leap_year_1(year)} for {year}")

# Challenge 3: Assert that 1900 is not a leap year. Fix function so it returns the correct result for 1900

# Solution 3: 
# assert not is_leap_year_1(1900)
def is_leap_year_3(year):
    if year % 100 == 0:
        return False
    return year % 4 == 0
assert not is_leap_year_3(1900)

# Challenge 4: Assert that 2000 is a leap year and fix function so it is so

# Solution 4: 
# assert is_leap_year_3(2000)
def is_leap_year_4(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0
assert is_leap_year_4(2000)

# Challenge 5: Only run asserts if module is run as a script, not imported. When run as a script __name__ == "__main__"
print(f"{__name__=}")

# Solution 5:
def check_is_leap_year():
    assert is_leap_year_4(2016)
    assert not is_leap_year_4(2019)
    assert is_leap_year_4(2000)
    assert not is_leap_year_4(1900)
    print("\nSolution 5: All tests passed")

if __name__ == "__main__":
    check_is_leap_year()

# Challenge 6: Set up project with following structure
# bpaml165
#   |_ main.py
#   |_ tests.py
#   |_ requirements.txt

r"""# Challenge 6: Set up project with following structure

    bpaml165
      |_ main.py
      |_ tests.py
      |_ requirements.txt

`main.py`
``` python
def is_leap_year(year):
    # if year % 400 == 0:
    #     return True
    # if year % 100 == 0:
    #     return False
    return year % 4 == 0
```

`test_main.py`  (must be `test_*.py` or `*_test.py`)
``` python
from main import is_leap_year
import pytest


def test_is_leap_year():
    assert is_leap_year(2016)
    assert not is_leap_year(2019)
    assert is_leap_year(2000)
    assert not is_leap_year(1900)
```

requirements.txt
```
pytest
```

# Install pytest in virtual environment
From the command line in the project directory
create a virtual environment and install pytest

### Windows Python
```shell
py -m venv venv-bpaml165
venv-bpaml165\Scripts\Activate.bat
pip install -r requirements.txt
```

### Linux or Mac with Python
```shell
python3 -m venv venv-bpaml165
source venv-bpaml165/bin/activate
pip install -r requirements.txt
```

### Windows, Linux or Mac with Anaconda
```shell
conda create --name venv_bpaml165 python
conda activate venv_bpaml165
conda install --file requirements.txt
```

# Run pytest
```shell
pytest
```

```
============================================================= test session starts ==============================================================
platform linux -- Python 3.10.6, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/tim/PycharmProjects/bpaml165
collected 1 item                                                                                                                               

test_main.py F                                                                                                                           [100%]

=================================================================== FAILURES ===================================================================
______________________________________________________________ test_is_leap_year _______________________________________________________________

    def test_is_leap_year():
        assert is_leap_year(2016)
        assert not is_leap_year(2019)
        assert is_leap_year(2000)
>       assert not is_leap_year(1900)
E       assert not True
E        +  where True = is_leap_year(1900)

test_main.py:9: AssertionError
=========================================================== short test summary info ============================================================
FAILED test_main.py::test_is_leap_year - assert not True
============================================================== 1 failed in 0.01s ===============================================================
```

Fix main.py by uncommenting code and run pytest again
```
pytest
```
```
============================================================= test session starts ==============================================================
platform linux -- Python 3.10.6, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/tim/PycharmProjects/bpaml165
collected 1 item                                                                                                                               

test_main.py .                                                                                                                           [100%]

============================================================== 1 passed in 0.00s ===============================================================
```

### Use parameters in test function in `test_main.py` using `@pytest.mark.parametrize`
```
@pytest.mark.parametrize(
    ("year", "result"),
    (
            (2016, True),
            (2019, False),
            (2000, True),
            (1900, False),
    )
)
def test_is_leap_year_with_parameters(year, result):
    print("Testing", year, result)
    assert is_leap_year(year) is result
```
"""

