#!/usr/bin/env python3
"""MeetUp 216 - Beginners' Python and Machine Learning - 18 Jun 2025 - Object Oriented Programming

- Colab:   https://colab.research.google.com/drive/1mg55pLdJcevT8NLw3NyhOvn-LgZWVTQD
- Youtube: https://youtu.be/Qy5F-ji42xs
- Github:  https://github.com/timcu/bpaml-sessions/blob/master/online/
- Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/308274927/

Python classes allow you to use object oriented programming style. OOP makes it simpler to organise all the code for an 'object'
into a class. This breaks the programming problem down into smaller compartments where each class can be debugged on its own. It
also allows inheritance meaning you can build classes which inherit all the properties of existing classes.

References:
- https://docs.python.org/3/tutorial/classes.html
- https://docs.python.org/3/reference/datamodel.html#basic-customization

@author D Tim Cummings
"""

import datetime
from pprint import pprint

# example of an object of class complex
c = 3 + 4j
print(f"c = {c}, type(c) = {type(c)}, repr(c) = {repr(c)}")

# c is an instance of class complex
print(f"Is c an instance of complex ? {isinstance(c, complex)}")

# Attributes of an object are accessed by dot notation
print(f"c has data attributes c.real={c.real} and c.imag={c.imag}")

# Attributes can be data or functions. Functions that can be called on an object are called methods
print(f"The conjugate of {c} is {c.conjugate()}")

# When instantiating an object of a non-builtin type, use ClassName(args)
c2 = complex(3, 4)
print(f"c: {c}, c2: {c2}, c==c2: {c==c2}")


# How to define a simple class (convention is to use title case for class names eg MyClassName)
class MySimpleClass:
    pass


# How to create an instance of this class
msc_instance = MySimpleClass()

# New attributes can be set on instances of the class
msc_instance.a = "value a"

# Values of attributes can be retrieved using dot notation
print(f"The repr of msc_instance.a is {msc_instance.a!r}")


# We could define our own class Complex
class Complex:
    """Example of a class with three methods"""
    def __init__(self, real, imag):
        """__init__ is called when an object is instantiated (instance is created)"""
        self.real = real
        self.imag = imag

    def __str__(self):
        """__str__ is a method called when user calls str(this instance)"""
        return f"({self.real}{'+' if self.imag >= 0 else ''}{self.imag}j)"

    def conjugate(self):
        return Complex(self.real, -self.imag)


d = Complex(5, 12)
print(f"Conjugate of {d} is {d.conjugate()}")

# attributes of d, instance of Complex
print(f"Attributes of d {type(d)}")
print(d.__dict__)

# attributes of class show methods
print("Attributes of class Complex")
pprint(Complex.__dict__)

# Task 1: Create a class Invoice which takes parameters aud_amount, days_terms, date_document


# Solution 1:
class Invoice:
    """Invoice for sale of goods or services

    Attributes
        aud_amount: value of charges on invoice in Australian dollars
        days_terms: Number of days before payment of invoice is due (default 30)
        date_document: Date the invoice was issued (default today)
    Methods
        date_due: Calculates when the payment of invoice must be made by
    """
    def __init__(self, aud_amount, days_terms=30, date_document=None):
        """Invoice() constructor"""
        self.aud_amount = aud_amount
        self.days_terms = days_terms
        self.date_document = datetime.datetime.today() if date_document is None else date_document

    def date_due(self):
        "returns calculated date when payment must be made by"
        return self.date_document + datetime.timedelta(days=self.days_terms)


iv = Invoice(350)
print(f"Solution 1: Invoice for ${iv.aud_amount:,.2f} dated {iv.date_document.strftime('%d %B %Y')} "
      f"is due {iv.date_due().strftime('%d %B %Y')}")

# Calling a method can be done two ways. This is reason for self parameter
print(f"iv.date_due()        {iv.date_due()}")
print(f"Invoice.date_due(iv) {Invoice.date_due(iv)}")

# Task 2: Add a __str__ method to class so that easier to print invoice


# Solution 2
def str_invoice(self):
    return f"Invoice for ${self.aud_amount:,.2f} dated {self.date_document.strftime('%d %B %Y')} " + \
           f"is due {self.date_due().strftime('%d %B %Y')}"


Invoice.__str__ = str_invoice
print(f"Solution 2: {iv}")

# Solution 2 using lambda (off topic)
Invoice.__str__ = lambda self: f"Invoice for amount ${self.aud_amount:,.2f} dated {self.date_document.strftime('%d %b %Y')} " + \
                               f" is due {self.date_due().strftime('%d %b %Y')}"
print(f"Creating __str__ using lambda: {iv}")

# Task 3: Create a class for Quote which has values for amount, days_valid, date_quote and method date_valid_to


# Solution 3 using inheritance
class Document:

    date_format = '%d-%b-%Y'  # class variable

    def __init__(self, str_doc_type, str_action, aud_amount, days_duration, date_document=None):  # class constructor method
        self.str_doc_type = str_doc_type
        self.str_action = str_action  # instance variable
        self.aud_amount = aud_amount
        self.date_document = datetime.datetime.today() if date_document is None else date_document
        self.days_duration = days_duration

    def date_duration(self):  # class method
        return self.date_document + datetime.timedelta(days=self.days_duration)

    def __str__(self):  # class method called whenever str(instance of Document) is called
        str_amount = f"${self.aud_amount:,.2f}"
        str_date = self.date_document.strftime(self.date_format)
        str_finish = self.date_duration().strftime(self.date_format)
        return f"{self.str_doc_type} for {str_amount} dated {str_date} {self.str_action} {str_finish}"


class Invoice(Document):

    def __init__(self, aud_amount, days_terms=30, date_document=None):
        super().__init__("Invoice", "payment due", aud_amount, days_terms, date_document)

    def date_due(self):
        return self.date_duration()


class Quote(Document):

    def __init__(self, aud_amount, days_valid=14, date_document=None):
        super().__init__("Quote", "valid until", aud_amount, days_valid, date_document)

    def date_valid_until(self):
        return self.date_duration()


q = Quote(346)
print(f"Solution 3 with inheritance: {q}")

# Task 4: Create an SalesOrder class which has days_deliver when goods need to be delivered


# Solution 4
class SalesOrder(Document):

    def __init__(self, aud_amount, days_deliver=7, date_document=None):
        super().__init__("Sales Order", "deliver by", aud_amount, days_deliver, date_document)

    def date_deliver(self):
        "returns calculated date by which sales order must be delivered"
        return self.date_duration()


so = SalesOrder(1234)
print(f"Solution 4: {so}")

# Task 5: Create a class Item which can represent a line item on a quote, sales order or invoice
# It needs a description, quantity and a unit_price


# Solution 5:
class Item:
    def __init__(self, description, quantity, aud_unit_sell):
        self.description = description
        self.quantity = quantity
        self.aud_unit_sell = aud_unit_sell

    def aud_sell(self):
        return self.quantity * self.aud_unit_sell

    def __str__(self):
        return f"{self.description:20} {self.quantity:>5d}  ${self.aud_unit_sell:>10,.2f}  ${self.aud_sell():>10,.2f}"

    # str_title is a class attribute. It will be same for all instances of class (if not overridden)
    # Do not use mutable values in class attributes (eg list)
    str_title = f"{'Description':20} {'Qty':>5}   {'Unit price':>10}   {'Price':>10}"


def document_add_item(self, item):
    # easier to check for attribute here than rewrite __init__. Better to rewrite __init__
    if not hasattr(self, "lst_items"):
        self.lst_items = []
    self.lst_items.append(item)


# Here we are modifying class on the fly. Full final defs of classes at end of this notebook
Document.add_item = document_add_item

q.add_item(Item("Thingamee", 2, 123.45))
q.add_item(Item("Doodad", 5, 34.60))
print(Item.str_title)
for i in q.lst_items:
    print(i)

# Task 6: Create a report in Document for all documents


# Solution 6:
def document_report(self):
    str_date = self.date_document.strftime(self.date_format)
    str_finish = self.date_duration().strftime(self.date_format)
    s = f"{' ':25}{self.str_doc_type:20} {str_date}\n"
    s += f"{' ':25}{self.str_action.title():20} {str_finish}\n"
    s += "\n"
    s += "Item " + Item.str_title + "\n"
    aud_total = self.aud_amount
    num = 0
    for item in self.lst_items:
        num += 1
        s += f"{num:>4d} {item}\n"
        aud_total += item.aud_sell()
    s += "\n"
    s += f"{' ':30} Other charges: ${self.aud_amount:10,.2f}\n"
    s += f"{' ':30}         Total: ${aud_total:10,.2f}\n"
    return s


Document.report = document_report
# print(iv.report())
print(q.report())

# Check inheritance of our values
for d in (q, so, iv):
    print(f"{str(d):70}", end=' ')
    for t in (Document, Quote, SalesOrder, Invoice):
        print(f"{t.__name__}={str(isinstance(d, t)):5}", end=' ')
    print()

# Example adding items to invoice
# Have to create a new invoice because previous invoice did not inherit Document
iv2 = Invoice(15)
iv2.add_item(Item("Thingamee", 20, 123.45))
iv2.add_item(Item("Doodad", 15, 34.60))
print(iv2.report())

# Task 7: Add a method to Invoice so users can check value of days_terms without having to know subclass name date_duration


# We can use decorators to modify behaviour of functions
@property
def days_terms(self):
    return self.days_duration


Invoice.days_terms = days_terms
print(f"Solution 7: iv2.days_terms={iv2.days_terms}")

# Can't assign a value using attribute notation as we have created a read only property
try:
    iv2.days_terms = 35
    print(f"After change iv2.days_terms={iv2.days_terms}")
except AttributeError as ae:
    print(ae)

# Task 8: Make days_valid a property for Quote


# We can use decorators to modify behaviour of functions
@property
def days_valid(self):
    return self.days_duration


@days_valid.setter
def days_valid(self, days_valid):
    self.days_duration = days_valid


Quote.days_valid = days_valid
print(f"Solution 8: q.days_valid={q.days_valid}")
q.days_valid = 21
print(f"After change q.days_valid={q.days_valid}")


# Variable naming with underscores (advanced topic)
# 0 underscores : public variable accessible as an attribute
# 1 underscore  : private variable (by convention). Recommend don't access it
# 2 underscores : subclass accessible private variable (Python name mangling)
class MyBase:
    my_one = "my public class var"
    _my_one = "my private class var"
    __my_one = "my double underscore (dunder) class var"
    my_two = "my public class var defined same way as my_one"
    _my_two = "my private class var defined same way as _my_one"
    __my_two = "my double underscore (dunder) class var defined same way as __my_one"

    def __init__(self, s):
        self.my_two = f"my public instance var {s}"
        self._my_two = f"my private instance var {s}"
        self.__my_two = f"my dunder instance var {s}"
        self.my_three = f"my public instance var {s[::-1]}"
        self._my_three = f"my private instance var {s[::-1]}"
        self.__my_three = f"my dunder instance var {s[::-1]}"

    def dunder_one(self):
        return self.__my_one

    def dunder_two(self):
        return self.__my_two

    def dunder_three(self):
        return self.__my_three

    def sunder_two(self):
        return self._my_two


my_ins = MyBase("bpaml")

print("my_one:   assigned as a class variable")
print("my_two:   assigned as a class variable and an instance variable with a str parameter")
print("my_three: assigned as an instance variable with a reversed str parameter")
print()
for suffix in ['my_one', 'my_two', 'my_three']:
    for prefix in ['', '_', '__', '_MyBase__']:
        attr_name = prefix + suffix
        try:
            print(f"my_ins.{attr_name:20}={getattr(my_ins, prefix+suffix)!r}")
        except AttributeError as ae:
            print(f"my_ins.{attr_name:20} {ae}")
        try:
            print(f"MyBase.{attr_name:20}={getattr(MyBase, prefix+suffix)!r}")
        except AttributeError as ae:
            print(f"MyBase.{attr_name:20} {ae}")
print(f"my_ins.dunder_one()        ={my_ins.dunder_one()!r}")
print(f"my_ins.dunder_two()        ={my_ins.dunder_two()!r}")
print(f"my_ins.dunder_three()      ={my_ins.dunder_three()!r}")
print(f"my_ins.sunder_two()        ={my_ins.sunder_two()!r}")


class MySub(MyBase):
    my_one = "the public subclass var"
    _my_one = "the private subclass var"
    __my_one = "the dunder subclass var"
    my_two = "the public class var defined same way as my_one"
    _my_two = "the private class var defined same way as _my_one"
    __my_two = "the double underscore (dunder) class var defined same way as __my_one"

    def __init__(self, s):
        super().__init__("subclassed")
        self.my_two = f"the public instance var {s} {super().my_two}"
        self._my_two = f"the private instance var {s} {super()._my_two}"
        try:
            self.__my_two = f"the dunder instance var {s} {super().__my_two}"
        except AttributeError as ae:
            print(ae)
        self.my_three = f"the public instance var {s[::-1]}"
        self._my_three = f"the private instance var {s[::-1]}"
        self.__my_three = f"the dunder instance var {s[::-1]}"


my_si = MySub("inheritance")

print("my_one:   assigned in base class and subclass as a class variable")
print("my_two:   assigned in base class and subclass as a class variable and as instance variable with a str parameter")
print("my_three: assigned in base class and subclass as an instance variable with a reversed str parameter")
print()
for suffix in ['my_one', 'my_two', 'my_three']:
    for prefix in ['', '_', '__', '_MyBase__', '_MySub__']:
        attr_name = prefix + suffix
        try:
            print(f"my_si.{attr_name:20}={getattr(my_si, prefix+suffix)!r}")
        except AttributeError as ae:
            print(f"my_si.{attr_name:20} {ae}")
        try:
            print(f"MySub.{attr_name:20}={getattr(MySub, prefix+suffix)!r}")
        except AttributeError as ae:
            print(f"MySub.{attr_name:20} {ae}")
print(f"my_si.dunder_one()        ={my_si.dunder_one()!r}")
print(f"my_si.dunder_two()        ={my_si.dunder_two()!r}")
print(f"my_si.dunder_three()      ={my_si.dunder_three()!r}")
print(f"my_si.sunder_two()        ={my_si.sunder_two()!r}")


# Multiple inheritance possible in Python
class MyComplexSub(Complex, MyBase):
    def __init__(self, r, i):
        # how to call multiple super classes
        super().__init__(r, i)
        super(Complex, self).__init__(str(self))


mi = MyComplexSub(5, 12)
print(mi)
print(mi.my_one)
print(mi.my_two)
print(mi.my_three)
print("Method resolution order")
print(MyComplexSub.__mro__)

# How to design base classes to make use in multiple inheritance easier
# Capture all keyword arguments and pass through unused ones to super


class BaseZero:
    def __init__(self, **kwargs):
        print(f"BaseZero.__init__ with {kwargs}")
        super().__init__(**kwargs)


class SubOne(BaseZero):
    def __init__(self, key_one, **kwargs):
        print(f"SubOne.__init__ with {kwargs}")
        self.key_one = key_one
        super().__init__(**kwargs)


class SubTwo(BaseZero):
    def __init__(self, key_two, **kwargs):
        print(f"SubTwo.__init__ with {kwargs}")
        self.key_two = key_two
        super().__init__(**kwargs)


class SubSubThree(SubOne, SubTwo):
    def __init__(self, **kwargs):
        print(f"SubSubThree.__init__ with {kwargs}")
        super().__init__(**kwargs)


ss = SubSubThree(key_two="TWO", key_one="ONE")
print(f"ss.key_one={ss.key_one}")
print(f"ss.key_two={ss.key_two}")


# Full class definitions including documentation
class Document:
    """Base class for Quote and Invoice

    Attributes
        aud_amount: Total value in Australian dollars
        date_document: Date the document was issued
        days_duration: Number of days to calculate date_duration
    """
    date_format = '%d-%b-%Y'

    def __init__(self, str_doc_type, str_action, aud_amount, days_duration, date_document=None):
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
        self.date_document = datetime.datetime.today() if date_document is None else date_document
        self.days_duration = days_duration
        self.lst_items = []

    def date_duration(self):
        "returns calculated date when duration finished"
        return self.date_document + datetime.timedelta(days=self.days_duration)

    def __str__(self):
        "called when str(instance_document) called. Returns one line summary of document"
        str_amount = f"${self.aud_amount:,.2f}"
        str_date = self.date_document.strftime(self.date_format)
        str_finish = self.date_duration().strftime(self.date_format)
        return f"{self.str_doc_type} for {str_amount} dated {str_date} {self.str_action} {str_finish}"

    def add_item(self, item):
        self.lst_items.append(item)

    def report(self):
        """returns a multiline text document report for invoice, sales order or quote"""
        str_date = self.date_document.strftime(self.date_format)
        str_finish = self.date_duration().strftime(self.date_format)
        s = f"{' ':25}{self.str_doc_type:20} {str_date}\n"
        s += f"{' ':25}{self.str_action.title():20} {str_finish}\n"
        s += "\n"
        s += "Item " + Item.str_title + "\n"
        aud_total = self.aud_amount
        num = 0
        for item in self.lst_items:
            num += 1
            s += f"{num:>4d} {item}\n"
            aud_total += item.aud_sell()
        s += "\n"
        s += f"{' ':30} Other charges: ${self.aud_amount:10,.2f}\n"
        s += f"{' ':30}         Total: ${aud_total:10,.2f}\n"
        return s


class Invoice(Document):
    def __init__(self, aud_amount, days_terms=30, date_document=None):
        """Invoice() constructor

        aud_amount: value of charges on invoice in Australian dollars (required)
        days_terms: Number of days before payment of invoice is due (default 30)
        date_document: Date the invoice was issued (default today)
        """
        super().__init__("Invoice", "payment due", aud_amount, days_terms, date_document)

    def date_due(self):
        "returns calculated date when payment must be made by"
        return self.date_duration()

    @property
    def days_terms(self):
        return self.days_duration

    @days_terms.setter
    def days_terms(self, days_terms):
        self.days_duration = days_terms


class Quote(Document):
    def __init__(self, aud_amount, days_valid=14, date_document=None):
        """Quote() constructor

        aud_amount: Total value of quote in Australian dollars (required)
        days_valid: Number of days quote is valid for (default 14)
        date_document: Date the quote was issued (default today)
        """
        super().__init__("Quote", "valid until", aud_amount, days_valid, date_document)

    def date_valid_until(self):
        "returns calculated date after which quote is no longer valid"
        return self.date_duration()

    @property
    def days_valid(self):
        return self.days_duration

    @days_valid.setter
    def days_valid(self, days_valid):
        self.days_duration = days_valid


class SalesOrder(Document):
    def __init__(self, aud_amount, days_deliver=7, date_document=None):
        """SalesOrder() constructor

        aud_amount: value of charges on sales order in Australian dollars (required)
        days_deliver: Number of days within which goods need to be delivered (default 7)
        date_document: Date the sales_order was received (default today)
        """
        super().__init__("Sales Order", "to be delivered by", aud_amount, days_deliver, date_document)

    def date_deliver(self):
        "returns calculated date by which sales order must be delivered"
        return self.date_duration()

    @property
    def days_deliver(self):
        return self.days_duration

    @days_deliver.setter
    def days_deliver(self, days_deliver):
        self.days_duration = days_deliver


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
        """one line description of line item showing description, quantity, unit and extended price, formatted to match str_title"""
        return f"{self.description:20} {self.quantity:>5d}  ${self.aud_unit_sell:>10,.2f}  ${self.aud_sell():>10,.2f}"
