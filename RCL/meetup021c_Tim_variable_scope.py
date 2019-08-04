"""
MeetUp 021c - Beginners Python Support Sessions 30-Jul-2019 - Variable scope

Learning objectives:
    Testing functions with assert and pytest
    Variable scope in functions

@author D Tim Cummings
"""
# Challenge 10: Variable scope: Create a global variable my_global and a function which displays the value of my_global.
my_global = 73


def show_my_global():
    print("show_my_global: my_global = {}".format(my_global))


show_my_global()

# Challenge 11: Create a function to assign a new value to my_global and display its value.
# Display value my_global after calling function.
def assign_my_global():
    my_global = 2  # really only sets a local variable called my_global
    print("assign_my_global: my_global = {}".format(my_global))


assign_my_global()
show_my_global()


# Challenge 12: Create a function to increment value of my_global by one (use keyword global).
def increment_my_global():
    global my_global
    my_global += 1
    print("increment_my_global: my_global = {}".format(my_global))


increment_my_global()
show_my_global()


# Challenge 13: Create nested functions and refer to variable from outer function in inner function. (try keyword nonlocal)
a = 0
b = 1


def outer1():
    global b
    a = 2
    b = 3
    c = 4
    d = 5
    print("outer1: a = {}, (global) b = {}, c = {}, d = {}".format(a, b, c, d))

    def inner1():
        nonlocal d
        a = 6
        b = 7
        c = 8
        d = 9
        print("inner1: a = {}, (nonlocal) b = {}, c = {}, (nonlocal) d = {}".format(a, b, c, d))
    inner1()
    print("outer1: a = {}, (global) b = {}, c = {}, d = {}".format(a, b, c, d))


outer1()
print("module: a = {}, b = {}".format(a, b))


# Challenge 14: Create a triple nested function and see whether nonlocal refers to one level up or all levels up
def outer2():
    global b
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    print("outer2: a = {}, (global) b = {}, c = {}, d = {}, e = {}".format(a, b, c, d, e))

    def inner2a():
        nonlocal c
        nonlocal d
        b = 7
        c = 8
        d = 9
        e = 10
        print("inner2a: a = {}, b = {}, (nonlocal) c = {}, (nonlocal) d = {}, e = {}".format(a, b, c, d, e))

        def inner2b():
            nonlocal a
            nonlocal d
            nonlocal e
            a = 11
            b = 12
            c = 13
            d = 14
            e = 15
            print("inner2b: (nonlocal) a = {}, b = {}, c = {}, (nonlocal) d = {}, (nonlocal) e = {}".format(a, b, c, d, e))
        inner2b()
        print("inner2a: a = {}, b = {}, (nonlocal) c = {}, (nonlocal) d = {}, e = {}".format(a, b, c, d, e))
    inner2a()
    print("outer2: a = {}, (global) b = {}, c = {}, d = {}, e = {}".format(a, b, c, d, e))


outer2()
print("module: a = {}, b = {}".format(a, b))


# Advanced Challenge 15: Create a function with one argument which has a default which is a dictionary e.g. {'key': 5}
# Function doubles the value associated with 'key' and returns the modified dictionary. Test
# assert double_key() == {'key': 10}
# assert double_key() == {'key': 10}  # this may fail even though first time passed
def double_key_bad(x={'key': 5}):
    x['key'] = 2 * x['key']
    return x


# Challenge: fix double_key_bad by removing mutable data in default
def double_key_good(x=None):
    if x is None:
        x = {'key': 5}
    x['key'] = 2 * x['key']
    return x


assert double_key_good({'key': 100}) == {'key': 200}
assert double_key_good({'key': 100, 'key2': 50}) == {'key': 200, 'key2': 50}
assert double_key_good() == {'key': 10}
assert double_key_good() == {'key': 10}  # this line fails with double_key_bad because default parameter is a mutable value
assert double_key_good(None) == {'key': 10}
print(double_key_good({'key': 100}))
print(double_key_good({'key': 100, 'key2': 50}))
print(double_key_good())
print(double_key_good())
print(double_key_good(None))

assert double_key_bad({'key': 100}) == {'key': 200}
assert double_key_bad({'key': 100, 'key2': 50}) == {'key': 200, 'key2': 50}
assert double_key_bad() == {'key': 10}
# assert double_key_bad() == {'key': 10}  # this line fails with double_key_bad because default parameter is a mutable value
# assert double_key_bad(None) == {'key': 10}  # fails because can't set value for a key on None
print(double_key_bad({'key': 100}))
print(double_key_bad({'key': 100, 'key2': 50}))
print(double_key_bad())
print(double_key_bad())
# print(double_key_bad(None))  # fails because can't set value for a key on None
