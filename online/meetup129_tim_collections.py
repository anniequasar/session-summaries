#! /usr/bin/env python3
r"""MeetUp 129 - Beginners' Python and Machine Learning - 11 Jan 2022 - Collections

Learning objectives:
- built-in and library collections https://docs.python.org/3/library/collections.html
- list tuple dict set defaultdict namedtuple deque ChainMap Counter

Links:
- Colab:   https://colab.research.google.com/drive/1GnHlIDalV7xMd7soYujEebHolaw4MQla
- Youtube: https://youtu.be/GI9fV3p976A
- Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/283046358/
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings
"""

# We have already looked at the built-in collections list, tuple, dict and set
l = [1, 3.0, "five"]
t = (2, 4.0, "six", 3+5j)
d = {10: "ten", 20: "twenty", "thirty": 30, "forty": "forty"}
s = {5, 7, "nine", 5}

# lists and tuples are ordered sequences of values
# lists and tuples are iterable so can be used in a `for` loop
print("Contents of tuple (and list)")
for v in t:
    print(v)

# Refer to individual elements in sequence using a zero-based index in square brackets
# Negative index counts back from the end. (No such thing as -0)
print(f"t[0]={t[0]}, l[-1]={l[-1]}")

# Slicing allows selecting several elements [start:stop] or [start:stop:step]
print(f"l[1:3]={l[1:3]}")
print(f"t[0:3:2]={t[0:3:2]}")

# lists and tuples can be concatenated and multiplied (can't add lists to tuples)
l2 = l + l[::-1]
print(f"l2={l2}")
l3 = l * 3
print(f"l3={l3}")
t2 = t + t[::-1]
print(f"t2={t2}")
t3 = t * 3
print(f"t3={t3}")

# Easy to convert between lists and tuples
l4 = list(t)
t4 = tuple(l)
print(f"l4={l4}")
print(f"t4={t4}")

# lists and tuples can be unpacked when assigning one value to multiple variables
a, b, c = l
print(f"a={a}")
print(f"b={b}")
print(f"c={c}")

# tuples can be packed when assigning multiple values to one variable
t2 = c, a
print(f"t2={t2}, type={type(t2)}")

# position only arguments of a function can be packed into a tuple
def f(*args):
    print(f"args={args}, type={type(args)}")

f(9, "seven", 5)

# What is the difference between lists and tuples?

# tuples are immutable, lists are mutable
# lists can have values added or removed
l5 = l * 3
l6 = [5, 3, 7, 2, 8]
# None of the following lines work with tuples
print(f"Initially                   l5={l5}")
l5[7] = 0.7
print(f"After l5[7] = 0.7,          l5={l5}")
l5.remove(1)
print(f"After remove(1),            l5={l5}")
del l5[4]
print(f"After del l5[4],            l5={l5}")
l5.extend(t)
print(f"After extend(t),            l5={l5}")
l5.append(100)
print(f"After append(100),          l5={l5}")
p = l5.pop()
print(f"After pop(),  p={p},        l5={l5}")
p = l5.pop(0)
print(f"After pop(0), p={p},        l5={l5}")
l6.sort()
print(f"After sort(),               l6={l6}")
l6.insert(4, 100)
print(f"After insert(4, 100)        l6={l6}")
l6[1:3] = (21, 22, 23)
print(f"After l6[1:3]=(21, 22, 23)  l6={l6}")

# Task 1 - achieve similar results with tuples for some of the above operations

print("\nSolution 1 - Always need to create a new tuple from old data. Can't modify in place")
t5 = tuple(3 * l)
t6 = (5, 3, 7, 2, 8)
print(f"Initially                   t5={t5}")
t5 = t5[0:7] + (0.7, ) + t5[8:]
print(f"Equiv l5[7] = 0.7,          t5={t5}")
idx = t5.index(1)
t5 = t5[:idx] + t5[idx+1:]
print(f"Equiv remove(1),            t5={t5}")
t5 = t5[:4] + t5[4+1:]
print(f"Equiv del l5[4],            t5={t5}")
t5 = t5 + t
print(f"Equiv extend(t),            t5={t5}")
t5 = t5 + (100, )
print(f"Equiv append(100),          t5={t5}")
p = t5[-1]
t5 = t5[:-1]
print(f"Equiv pop(),  p={p},        t5={t5}")
p = t5[0]
t5 = t5[1:]
print(f"Equiv pop(0), p={p},        t5={t5}")
t6 = tuple(sorted(t6))
print(f"Equiv sort(),               t6={t6}")
t6 = t6[:4] + (100,) + t6[4:]
print(f"Equiv insert(4, 100)        t6={t6}")
t6 = t6[:1] + (21, 22, 23) + t6[3:]
print(f"Equiv l6[1:3]=(21, 22, 23)  t6={t6}")

# Why would we want to use tuples? They are just harder to use.
# 1. tuples can be hashable so can be keys in a dict. lists are never hashable because they are mutable
# 2. Immutable reduces possibility of programming logic errors (this is not obvious but it is true)
# 3. There can be memory optimisations when using immutables but not if you are using the workarounds from task 1

# Using tuples to store coordinates of a sparse matrix
n = 7
d = {}
for i in range(n):
    d[(i, i)] = "\\"
    d[(i, n-i-1)] = "/"

def display_sparse(dct_sparse):
    for y in range(n):
        for x in range(n):
            # Have to use get because not every coordinate is represented
            print(dct_sparse.get((x, y), ' '), end='')
        print()

display_sparse(d)
print(d)

# Task 2: Put a vertical line of pipes '|' for x = 1

print("\nSolution 2:")
d.update({(1, i): '|' for i in range(n)})
display_sparse(d)

# dict is a collection of key value pairs
# key for dict must be hashable eg int, str, tuple of hashable values
# dict is mutable - so can't be used as key for another dict
# since Python 3.6 dict is now ordered (creation order)

# set is a unique collection of values
# set is mutable
# set is unordered

# Example use of set to find x values used for the even y values in d
lst_x = []     # alternatively can use constructor list()
set_x = set()  # can't use {} because that is empty dict
for t in d:
    # only want tuples where y is even
    if t[1] % 2 == 0:
        lst_x.append(t[0])
        set_x.add(t[0])
print(f"lst_x={lst_x}")
print(f"set_x={set_x}")

# Task 3: Find all the unique values in d

print("\nSolution 3")
print({c for c in d.values()})

# collections standard library
# Since Python 3.6 OrderedDict not really necessary 
from collections import OrderedDict

od = OrderedDict(a=3, b=1, c=5)
print(od, type(od))

# How to convert between dict and OrderedDict
print(dict(od))
print(OrderedDict({'a': 3, 'b': 1, 'c': 5}))

# Let's get data from Brisbane City Council for some examples
# https://www.data.brisbane.qld.gov.au/data/dataset/ferry-terminals/resource/430c7115-f63d-4614-816f-a8aa9265ec7b and click on Data API button
# Sample python code is in Python 2 not Python 3.
#   import urllib
#   url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?resource_id=430c7115-f63d-4614-816f-a8aa9265ec7b&limit=5&q=title:jones'  
#   fileobj = urllib.urlopen(url)
#   print fileobj.read()


from urllib.request import urlopen
url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?resource_id=430c7115-f63d-4614-816f-a8aa9265ec7b&limit=5&q=title:jones'  
fileobj = urlopen(url)
print(fileobj.read())

# Previous result gives us a byte string in json format. Also filter returns no results. We can convert to dict using json library 
# See meetup 74 for more details about json
import json
import pprint
# url without the filter
url = 'https://www.data.brisbane.qld.gov.au/data/api/3/action/datastore_search?resource_id=430c7115-f63d-4614-816f-a8aa9265ec7b'
# filter limit 2 records to inspect data  
dct_terminal = json.load(urlopen(url + '&limit=2'))
print("\nData from BCC")
pprint.pprint(dct_terminal)

# Let's get all the data
dct_terminal = json.load(urlopen(url))
lst_terminal = dct_terminal['result']['records']
print("Number of ferry terminals", len(lst_terminal))
pprint.pprint(lst_terminal[0])

# Want to categorise by their pontoon material
dct_by_material = {}
for t in lst_terminal:
    material = t['PONTOON_MATERIAL']
    if material not in dct_by_material:
        dct_by_material[material] = []
    dct_by_material[material].append(t['DESCRIPTION'])
pprint.pprint(dct_by_material)

from collections import defaultdict
# defaultdict constructor takes a function name to call when creating a new item
dct_by_material = defaultdict(list)
for t in lst_terminal:
    dct_by_material[t['PONTOON_MATERIAL'].strip()].append(t['DESCRIPTION'])
pprint.pprint(dct_by_material)

# Task 4: Categorise ferry terminals by number of boarding gates

print("\nSolution 4:")
dct_by_gates = defaultdict(list)
for t in lst_terminal:
    dct_by_gates[int(t['BOARDING_GATES'])].append(t['DESCRIPTION'])
pprint.pprint(dict(dct_by_gates))

# Counter useful if we only need the frequency of each category
from collections import Counter
lst_gate = [t['BOARDING_GATES'] for t in lst_terminal]
cnt_gate = Counter(lst_gate) 
print(f"lst_gate={lst_gate}")
print(f"cnt_gate={cnt_gate}")

# Task 5: How many have drinking fountains?

print("\nSolution 5:")
c = Counter([t['DRINKING_FOUNTAIN_PRESENT'] for t in lst_terminal])
print(f"Ferry terminals with drinking fountains = {c['Yes']}")

# namedtuples are a lightweight structure which can replace simple classes and can be used where tuples can be used
# They allow named access as well as positional access to elements of tuple
from collections import namedtuple
# we are creating a class so give it title case by convention. 
# named keys can be iterable sequence of strs or single str separated by space and/or comma
Point = namedtuple("Point", "x, y")
p = Point(1, 2)
print(p)

# namedtuples can have equality with normal tuples
p == (1, 2)

# namedtuples can refer to elements by name
print(f"p.x={p.x}, p.y={p.y}, p={p}")

# if you need to refer to attribute name from a str use getattr because p["x"] won't work
getattr(p, "x")

# namedtuple can be used as a key for a dict because they are immutable and hashable 
for i in range(n):
    d[Point(i, 1)] = d[Point(i, n-2)] = d[Point(1, i)] = d[Point(n-2, i)] = '⌗'
display_sparse(d)

pprint.pprint(d)

# Task 6: Convert list of terminals to namedtuple. Note that namedtuple keys can't start with underscore so we will first rename that key
for t in lst_terminal:
    if '_id' in t:
        t['id'] = t.pop('_id')

print("\nSolution 6:")
Terminal = namedtuple("Terminal", lst_terminal[0].keys())
lst_nt_terminal = [Terminal(**t) for t in lst_terminal]
pprint.pprint(lst_nt_terminal)

# Deque is a high performance, thread safe, double ended queue which can act like a stack (LIFO), a queue (FIFO) or even a tail (fixed queue size)
# Lists have good performance with pop and append at the end of list but low performance pop from or insert to the beginning

from collections import deque
print("\nExample of tail. Append at one end. Maximum length automatically pops from other end")
dq = deque([], 5)
for i in range(0, 30, 2):
    dq.append(i)
    print(dq)

print("\nExample of stack LIFO. Append and pop at same end")
dq = deque()
for i in range(4):
    for j in range(5):
        dq.append(i * 10 + j)
    print(dq)
    for j in range(2):
        p = dq.pop()
    print(dq, p)

print("\nExample of queue FIFO. Append and pop at different ends")
dq = deque()
for i in range(4):
    for j in range(5):
        dq.append(i * 10 + j)
    print(dq)
    for j in range(2):
        p = dq.popleft()
    print(dq, p)

print("\nChainMap works like dict.update but doesn't alter underlying dicts")
# Useful if you want defaults which can be overridden
from collections import ChainMap

d1 = {"a": 1, "b": 3, "c": 5}
d2 = {"c": 11, "d": 13, "e": 15}
d3 = {"d": 21, "e": 23, "f": 25}
cm = ChainMap(d3, d2, d1)
print(cm)

print(dict(cm))

# Only the first one is changed by writes and updates
cm['g'] = 31
print(dict(cm), d1, d2, d3)

cm['a'] = 33
print(dict(cm), d1, d2, d3)

