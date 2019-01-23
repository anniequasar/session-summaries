# Session 5
#download this .py file and run it in Pycharm Edu


# Data types

my_int = 1     # immutable

my_float = 1.0    # immutable

my_str = 'Hello World'     # immutable, iterable


my_tuple = (1, 2, 3)  # tuples are immutable - this means that when you later try to change the vales into a different variable it will remain unchanged

my_list = [1, 2, 3]   # lists are mutable - try to use immutable data types wherever possible to avoid obscure bugs later


my_dict = {'strings': 1, 'floats': 2.22, 'ints': 3}

# dictionaries have keys and values. Keys can be any immutable type. Values can be any type.

print('Example showing different data types for keys including using a variable name (key = "string") as one of the keys')

key = 'string'

my_dict = {'k': 'the k value', 'm': 123, 'n': [1, 2, 3], (1, 2): "twelve", 'd': {'a': 1}, 3: 9, key: 'what a value'}

print(my_dict)

print("my_dict['string']", my_dict['string'])


# to check a variable type:

print('type(my_int)', type(my_int))      # the console will return <class 'int'>

print('isinstance(my_string, str)', isinstance(my_str, str))     # console will return True or False


# Converting between types

# use int(), float(), str(), tuple(), list(), dict()

print('create new float from int using float(my_int)', float(my_int))

print('create new int from float using int(5.6)', int(5.6))

print('create new int from str using int("45")', int("45"))

print('create new list from tuple using list(my_tuple)', list(my_tuple))

print('create new tuple to list using tuple(my_list)', tuple(my_list))

print('create new list from int using [my_int]', [my_int])

print("create new tuple from str using (my_str, ). Don't forget the trailing comma.", (my_str, ))



# Duck typing. "We don't need to know if it is a duck, only whether it can quack"

# Example: we don't need to know if it is a list only whether it is iterable (ie we can use it with 'in' eg a for loop )

my_var = 'a string'  # iterable

# my_var = 5  # not iterable

try:

    # the following line will throw a TypeError if my_var is not iterable

    my_iter = iter(my_var)

    print('my_var is iterable because it is of type', type(my_var))

except TypeError:

    # Not iterable. Convert my_var to a single value tuple which is then iterable

    print('my_var is not iterable because it is of type', type(my_var))

    my_var = (my_var,)

# for loops can only loop through iterable variables

for c in my_var:

    # Print each letter separately but end the print with a space rather than a new line

    print(c, end=' ')

# finally print a new line

print()



# backslashes can be used to include special characters in a string. This is called escaping

print('Backslash       : \\\\ : >>>\\<<<')

print('New line        : \\n : >>>\n<<<')

print('Tab             : \\t : >>>\t<<<')

print('Single quote    : \\\' : >>>\'<<<')

print("Double quote    : \\\" : >>>\"<<<")

print('Bell            : \\a : >>>\a<<<')

print('Backspace       : \\b : >>>\b<<<')

print('Carriage return : \\r : >>>\r<<<')

print('Carriage return : \\r : example on previous line')

print('Vertical tab    : \\v : >>>\v<<<')

print('Hexadecimal byte: \\xff : >>>\x41<<<')

print('Octal byte      : \\000 : >>>\101<<<')

print('Backslash at end of line can ignore the new line')


# Strings with words such as don't and she's need a backstroke (\) in order to ignore end of string character

print('She didn\'t know what\'s going to happen next!')

# Alternatively use different quote style to avoid the need for escaping

print("We didn't")

print('He said "Do!"')

print("""He said "Don't" again.""")

print('''She said "Can't use triple double quote if last character is double quote as in this string"''')


# types of strings

s = u'abc'  # unicode string - default for python 3. Each character can be 1, 2, 3, or 4 (or more) bytes so can include Chinese, Hebrew, emojis, etc

t = b'abc'  # bytes string - default for python 2. Each character is 1 byte. Can't be used for non-ASCII characters (Chinese, Hebrew, emojis, etc)

q = r'\a\bc'  # raw string - doesn't interpret special characters such as backslash. They are used literally, ie exactly as typed.


print('Three string types, unicode, bytes, raw', s, t, q)


# Bytes are often used in serial communications over RS232 or Bluetooth.

# One byte = 8 bits. One bit is either a 0 or a 1

# Serial means one bit after the other like a single queue.

# Parallel means side by side like many queues

# HARDWARE HISTORY

# In the early days parallel was much faster than serial because many bits

# were transferred at each clock cycle. As faster clock cycles were used it

# became impossible to ensure all bits travelling down a parallel cable arrived

# at the same time so serial has now overtaken parallel.

# Parallel printer cables have been replaced with USB (Universal Serial Bus)

# PATA hard drive cables have been replaced with SATA (Serial ATA)



# Triple quotes (' or ") can be used for multi-line strings

# However be careful with indents because the white space from an indent is included in the string

if True:

    c_string = '''This multi-line

string was created

with triple single quotes'''

    print(c_string)

d_string = 'This string was created with single single quotes  \

and entered over multiple lines by escaping the end of each \

line with a backslash'

print(d_string)

e_string = 'This multi-line string was created with single single quotes\nand the new line in the middle was created using \\n'

print(e_string)


string_a = u'abc \n 😊' #unicode will allow you to use anything, any unicode character including hebew, chinese characters etc.,

string_b = b'abc' #byte / ascii only, can not use non-unicode characters, it will say emoji and other characters are an error

string_c = r'abc \n 😊'  #raw string doesn't use the backslash as the escape character, it prints it exactly as you typed it

string_d = r'hello\world'


# repr(var) displays how the value is represented internally to python


print('unicode string', type(string_a), repr(string_a), string_a)

print('bytes string', type(string_b), repr(string_b), string_b)

print('raw string', type(string_c), repr(string_c), string_c)

print('raw string', type(string_d), repr(string_d), string_d)


# Operators

# + is addition

# - is subtraction

# * is multiplication

# / is division with remainder - even when using integers it will return a float

# // is floor division, will only give the answer to the whole number - always returns an int,rounded down

# %  is the modulo which will give the remainder of an operation

# ** power - note that the carrot ^ is not used for powers in python as it will just add the numbers

# &  (ampersand) bitwise and - binery

# |  (pipe) bitwise or - binery excluse one or the other but not both



my_float = 1.1+2.2  # returns 3.3000000000003 because the mathematical conversion of 0.1 base 10 to base 2 is not exact

# python stores floats internally in base 2 and displays in base 10. The conversion back and forth loses data

# The conversion of integers is exact

# Thus this is not a problem for integer arithmetic or scientific applications but is a problem for financial applications

print("Addition of floats", 1.1, "+", 2.2, "=", my_float)


# to avoid this we need to import a module called Decimal

from decimal import Decimal

d1 = Decimal('1.10')

d2 = Decimal('2.200')

print("Addition of Decimals", d1, "+", d2, "=", d1+d2)    #result is 3.300, console will return the minimal number of values as specified <class 'decimal.Decimal'>

d3 = d1+d2

print("Type of the result is", type(d3))



# some operaters will also work on strings

# concatenating strings

string_e = "abc" + "def"

print('str addition: string_e = "abc" + "def" =', "abc" + "def")


# slicing strings

print("str slicing: string_e[3:6] =", string_e[3:6])


# and some operators will also work on lists

list_a = [1, 2, 3] + [4, 5, 6]

print("list addition: [1,2,3] + [4,5,6] =", list_a)


list_b = [1, 2, 3] * 3

print('list multiplication: list_b = [1,2,3] * 3 =', list_b)


print('list slicing: list_b[:4]', list_b[:4])


n = 0

print('use modulo operator (%) to only print even numbers', end=' ')

while n < 10:

    if n % 2 == 0:

        print(n, end=' ')

    n += 1

print()



# for loops

print("for n in [4, 3, 2, 1]:", end=' ')

for n in [4, 3, 2, 1]:

    print(n, end=' ')

print()



# for n in range(stop):  # from 0 to stop not including stop

# for n in range(start, stop):  # from start to stop not including stop

# for n in range(start, stop, step):  # from start to stop excluding stop incrementing by step each time

# if stop is less than start then step has to be negative


print("for n in range(4, 0, -1):", end=' ')

for n in range(4, 0, -1):

    print(n, end=' ')

print()


# to print the key and it's correlated value side by side:

print('Iterate through keys of dict')

for k in my_dict:

    # Show types of keys and values in a diverse dict

    print("Key:", k, type(k), "  Value:", my_dict[k], type(my_dict[k]))

print('Iterate through keys and values of dict')

for k, v in my_dict.items():

    print(k, ":", v)



# how to format strings

string_j = "sell price ${0:>8.2f}".format(3.2)  # in the {} the 8 = width, .2 = decimal places, f = floating point, > right aligned, < left aligned, ^ centred

print(string_j)
