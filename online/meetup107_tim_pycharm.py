#!/usr/bin/env python3
"""MeetUp 107 - Beginners' Python and Machine Learning - 11 May 2021 - PyCharm

Youtube: https://youtu.be/SF7Kq1oozbs
Source:  https://github.com/timcu/bpaml-sessions/raw/master/online/meetup107_tim_pycharm.py
Answers: https://github.com/timcu/bpaml-sessions/raw/master/online/meetup107_tim_pycharm_solution.py
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/278075460/
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

Learning objectives:
- Debugging and other features

@author D Tim Cummings

STEPS
Create new project
Create a new virtual environment (virtualenv for python, conda for anaconda)
Add this file to project
Fix compile errors which prevent running
Run until run time error
Edit run configuration to improve logging
Add a break point and debug (instead of run) to breakpoint
Other things to try in debugger: Step over, step into, step into my code, step out, run to cursor, watch variables, stack
Find to do items
Fix speling mistakes
Add bpaml to dictionary
Fix warnings and other problems
Compare solution to original

ERRORS AND WARNINGS
1. Uninstalled third party module and not in requirements file
2. Package or module has not been imported
3. Class has not been imported from module
4. Mixing tabs and spaces
5. Unused import statement
6. Use of deprecated method
7. IndexError: list index out of range
8. Incompatible with early python version 3.7
9. Code error: identified by assert
10. Unused variable
11. Local variable shadowing global variable
12. Unreachable code
13. Shadow built in function
14. Wrong expected type
15. Positioned arguments after named arguments
16. Not using argument
17. Unresolved attribute
18. Re-declared variable
"""
import argparse
import datetime
import logging
import math  # 5
import warnings

from typing import Optional, Union

import pyfiglet  # 1


if __name__ == "__main__":
    # set up logging if command line argument. Don't override pump_hydro_model.py if started that way
    parser = argparse.ArgumentParser(description="Meetup 107 exercises")
    parser.add_argument('--log', default='INFO', action='store', help='set log level. eg: --log INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
	args = parser.parse_args()  # 4
    numeric_level = getattr(logging, args.log.upper(), None)
    logging.basicConfig(level=numeric_level)
logger = logging.getLogger(__name__)

# create an empty requirements.txt file if it doesn't already exist
if not pathlib.Path('requirements.txt').is_file():  # 2
    with open('requirements.txt', 'a') as f:
        f.write('# add your third party libraries here')

print("\nFunction to convert number to name 0-999 trillion")
numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]  # 7
powers = {1000000000000: "trillion", 1000000000: "billion", 1000000: "million", 1000: "thousand", 100: "hundred"}

def number_to_text(number):
    warnings.warn("number_to_text has been replaced by number_name", DeprecationWarning)
    lst_digits = []
    for num in str(number):  # 11
        lst_digits.append(numbers[int(num)])
    return " ".join(lst_digits)


def number_name(number: int) -> str:
    """Returns the name of any integer between 0 and 1 trillion"""
    s = ""
    # dicts retain order since Python 3.6
    for power, name in powers.items():
        count = number // power
        if count > 0:
            # recursive call of number_name from within number_name
            s += f"{number_name(count)} {name} "
            number -= count * power
    if s != "" and number > 0:
        conjunction = "and"  # 9
    else:
        conjunction = ""
    right = number % 10
    left = number - right
    logger.debug(f"number_name: s={s}, conjunction={conjunction}, left={left}")
    if number == 0 and s != "":
        return s
    elif number < len(numbers):
        return s + conjunction + numbers[number]
    elif right == 0:
        return s + conjunction + tens[left]
    else:
        return s + conjunction + tens[left] + "-" + numbers[right]
    return "unknown"  # 12


# TODO rename num to numerals
num = 345
print(f"number_to_text(num)={number_to_text(num)}")  # 6
print(f"{number_name(num)=}")  # 8
assert number_name(345) == "three hundred and forty-five"
num = 456
num = 12345040302  # 18
print(f"number_name(num)={number_name(num)}")
assert number_name(12345040302) == "twelve billion three hundred and forty-five million forty thousand three hundred and two"


# from meetup088_tim_coding_introduction
def fahrenheit(celsius: float) -> float:
    """Convert temperature in celsius to fahrenheit"""
    return celsius * 1.8 + 32


c = 100
print(f"{c:7.2f}°C is equivalent to {fahrenheit(c):7.2f}°F")
c = 3+4j
print(f"{c:7.2f}°C is equivalent to {fahrenheit(c):7.2f}°F")  # 14


# From meetup079_tim_classes.py
class Document:
    """Base class for Quote and Invoice

    Attributes
        aud_amount: Total value in Australian dollars
        date_document: Date the document was issued
        days_duration: Number of days to calculate date_duration
    """
    date_format = '%d-%b-%Y'

    def __init__(self, str_doc_type: str, str_action: str, aud_amount: Union[float, Decimal], days_duration: int, date_document: Optional[datetime.date] = None):  # 3
        """Document() constructor

        str_doc_type: Document type, eg "Quote", "Invoice", "Sales Order"
        str_action: describes days_duration, eg "valid until" or "payment due" or "deliver by"
        aud_amount: value of charges on document in Australian dollars
        days_duration: number of days eg for terms or for validity depending on doc type
        date_document: Date the document was issued (default today)
        """
        self.str_doc_type = str_doc_type
        self.str_action = str_action
        self.aud_amount = aud_amount
        self.date_document: datetime.date = datetime.date.today() if date_document is None else date_document
        self.days_duration = days_duration
        self.lst_items: list[Item] = []

    def date_duration(self):
        "returns calculated date when duration finished"
        return self.date_document + datetime.timedelta(days=self.days_duration)

    @staticmethod
    def str_currency(aud_amount:Union[float, Decimal]):
        sign = "-" if aud_amount < 0 else " "
        return f"{sign}${abs(aud_amount):>9,.2f}"

    @property
    def str_amount(self):
        return self.str_currency(self.aud_amount)

    def __str__(self):
        """called when str(instance_document) called. Returns one line summary of document"""
        str_date = self.date_document.strftime(self.date_format)
        str_finish = self.date_duration().strftime(self.date_format)
        return f"{self.str_doc_type} for {self.str_amount} dated {str_date} {self.str_action} {str_finish}"

    def add_item(self, item):
        self.lst_items.append(item)

    def report(self):
        """returns a multiline text document report for invoice, sales order or quote"""
        str_amount = f"${self.aud_amount:,.2f}"  # 10
        str_date = self.date_document.strftime(self.date_format)
        str_finish = self.date_duration().strftime(self.date_format)
        s =  f"{' ':25}{self.str_doc_type:20} {str_date}\n"
        s += f"{' ':25}{self.str_action.title():20} {str_finish}\n"
        s += "\n"
        s += "Item " + Item.str_title + "\n"
        aud_total = self.aud_amount
        num = 0  # 11
        for item in self.lst_items:
            num += 1
            s += f"{num:>4d} {item}\n"
            aud_total += item.aud_sell()
        s += "\n"
        s += f"{' ':30} Other charges: {self.str_amount}\n"
        s += f"{' ':30}         Total: {self.str_currency(aud_total)}\n"
        return s


class Invoice(Document):
    def __init__(self, aud_amount, days_terms=30, date_document=None):  # 16
        """Invoice() constructor

        aud_amount: value of charges on invoice in Australian dollars (required)
        days_terms: Number of days before payment of invoice is due (default 30)
        date_document: Date the invoice was issued (default today)
        """
        super().__init__("Invoice", str_action="payment due", aud_amount, days_terms)  # 15

    def date_due(self):
        """returns calculated date when payment must be made by"""
        return self.date_duration()

    @property
    def days_terms(self):
        return self.days_duration

    @days_terms.setter
    def days_terms(self, days_terms):
        self.days_duration = days_terms

    def adjustment_note(self):
        adj_note = Invoice(-self.aud_amount, self.days_terms)
        adj_note.original_invoice = self
        for item in self.lst_items:
            # Because we have typed lst_items as list[Item], PyCharm can flag that we have used an attribute not in Item
            adj_note.add_item(Item(item.description, -item.quantity, item.aud_unit_price))  # 17
        return adj_note


class Item:
    """Line item for quote, sales order or invoice (or other)

    Attributes:
        description: text description of item
        quantity: number of items ordered
        aud_unit_sell: sell price in Australian dollars for each item
    Methods:
        aud_sell(): extended sell price for items = quantity x aud_unit_sell
    """

    # str_title is a class attribute. It will be same for all instances of class (if not overridden)
    # Do not use mutable values in class attributes (eg list)
    str_title = f"{'Description':20} {'Qty':>5}   {'Unit price':>10}   {'Price':>10}"

    def __init__(self, description, quantity, aud_unit_sell):
        """Item constructor"""
        self.description = description
        self.quantity = quantity
        self.aud_unit_sell = aud_unit_sell

    def aud_sell(self):
        """extended sell price for items = quantity x aud_unit_sell"""
        return self.quantity * self.aud_unit_sell

    def __str__(self):
        """one line description of line item showing description, quantity, unit price and extended price, formatted to match str_title"""
        return f"{self.description:20} {self.quantity:>5d}  {Invoice.str_currency(self.aud_unit_sell)}  {Invoice.str_currency(self.aud_sell())}"


iv1 = Invoice(15)
iv1.add_item(Item("quarter", 4, 12.34))
iv1.add_item(Item("half", 2, 4.32))
iv2 = Invoice(Decimal("23.13"))  # 3
iv3 = iv1.adjustment_note()

print(iv3.report())

list = [iv3, iv2, iv1]  # 13

for iv in list:
    print(iv, "adjustment note for", iv.original_invoice)  # 17

print(pyfiglet.figlet_format("Congratulations", font="isometric1", width=300))
