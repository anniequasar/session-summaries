# -*- coding: utf-8 -*-
"""
Functions - Beginners Python Session 9

@author: Tim Cummings

Demonstrates: Variable scope, Mutable defaults

"""

# Scope of variables - what happens when you use the same variable name in a function as outside a function
# Using a variable in a script assumes it is global
# Assigning a value to a variable in a script assumes variable is local
# Try not to shadow global variables with local variables
# Specify global if you want to assign a value to a global variable
# Specify nonlocal if you want to assign a value outside function code block but not in global eg nested functions

a = 5


def show_global_a():
    """Uses variable 'a' from global scope.
    Violates principle of functional programming but can be useful."""
    print("show_global_a(): global a={}".format(a))


def show_assigned_local_a():
    """Assigns value to a local variable 'a' and displays it.
    Normally avoid shadowing global variables with local variables of the same name"""
    a = 4
    print("show_assigned_local_a(): local a={}".format(a))


def show_assigned_global_a():
    """Assigns value to global variable 'a' and displays it.
    Violates principle of functional programming but can be useful."""
    global a
    a = 3
    print("show_assigned_global_a(): global a={}".format(a))


def outer_nested_function():
    """Example of accessing variable local to outer_nested_function from inner_nested_function"""
    a = 2  # local variable

    def inner_nested_function():
        nonlocal a
        a = 1
        print("inner__nested_function(): nonlocal a={}".format(a))

    print("outer__nested_function(): before local a={}".format(a))
    inner_nested_function()
    print("outer__nested_function(): after  local a={}".format(a))


show_global_a()
print("main code: global a={}".format(a))
show_assigned_local_a()
print("main code: global a={}".format(a))
show_assigned_global_a()
print("main code: global a={}".format(a))
outer_nested_function()
print("main code: global a={}".format(a))


# Challenge: Create a triple nested function and see whether nonlocal refers to one level up or all levels up
# Conclusion: nonlocal works up the nesting until it finds the next local variable which it refers to.
def level1():
    b = 11
    c = 21
    d = 31
    print("level1 a={}, b={}, c={}, d={}".format(a, b, c, d))

    def level2():
        nonlocal b
        nonlocal c
        a = -2
        print("level2 a={}, b={}, c={}, d={}".format(a, b, c, d))

        def level3():
            nonlocal a
            nonlocal c
            a = -3
            b = 13
            print("level3 a={}, b={}, c={}, d={}".format(a, b, c, d))

            def level4():
                nonlocal a
                nonlocal b
                nonlocal d
                a = -4
                b = 14
                c = 24
                d = 34
                print("level4 a={}, b={}, c={}, d={}".format(a, b, c, d))
            level4()
            print("level3 a={}, b={}, c={}, d={}".format(a, b, c, d))
        level3()
        print("level2 a={}, b={}, c={}, d={}".format(a, b, c, d))
    level2()
    print("level1 a={}, b={}, c={}, d={}".format(a, b, c, d))


level1()
print("main code: global a={}".format(a))


# Challenge: create a function with one argument which has a default which is a dictionary e.g. {'key': 5}
# Function doubles the value associated with 'key' and returns the new dictionary
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
print( double_key_good({'key': 100}) )
print( double_key_good({'key': 100, 'key2': 50}) )
print( double_key_good())
print( double_key_good())
print( double_key_good(None) )

assert double_key_bad({'key': 100}) == {'key': 200}
assert double_key_bad({'key': 100, 'key2': 50}) == {'key': 200, 'key2': 50}
assert double_key_bad() == {'key': 10}
assert double_key_bad() == {'key': 10}  # this line fails with double_key_bad because default parameter is a mutable value
assert double_key_bad(None) == {'key': 10}
print( double_key_bad({'key': 100}) )
print( double_key_bad({'key': 100, 'key2': 50}) )
print( double_key_bad())
print( double_key_bad())
print( double_key_bad(None) )
