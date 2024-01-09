#!/usr/bin/env python3
r"""MeetUp 084 - Beginners' Python and Machine Learning - 03 Nov 2020 - turtle graphics for absolute beginners

Youtube: https://youtu.be/QJKRgPodeRA
Source:  https://github.com/timcu/bpaml-sessions/raw/master/online/meetup084_tim_turtle.py
Answers: https://github.com/timcu/bpaml-sessions/raw/master/online/meetup084_tim_turtle_with_answers.py

Learning objectives
 - learn coding concepts using the educational turtle graphics

Reference:
https://docs.python.org/3/library/turtle.html
python3 -m turtledemo

@author D Tim Cummings

Requires Python 3 capable of tkinter installed on your computer
tkinter is included in the standard or anaconda python3 install on Mac and Windows

Alternatively use online
https://repl.it/languages/python_turtle

Task 1. Create new virtual environment. I find I need to inherit global site packages (sometimes)
python3 -m venv venv --system-site-packages

# Create virtual environment
python -m venv venv                                # Windows
python3 -m venv venv --system-site-packages        # Mac or Linux
conda create --name venv-bpaml-tkinter python=3.9  # Anaconda

# activate virtual environment
source venv/bin/activate                    # Mac or Linux or Windows Bash
conda activate venv-bpaml-tkinter           # Anaconda
venv\Scripts\activate.bat                   # Windows command prompt
venv\Scripts\Activate.ps1                   # Windows powershell
"""

# Demo 1: Simple Python turtle graphics
# Everything after a # is a comment and ignored (excluding # in quotes)
# turtle is a standard library so it doesn't need to be installed separately
import turtle  # libraries which are not built-in need to be imported so you can use them
import random

t = turtle.Turtle()  # create a turtle to start drawing with
t.shape("turtle")

# The following 7 lines are to speed up early tasks when we are doing later tasks. Ignore for now
fast_until_task = 1
if fast_until_task > 1:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)           # speed 10 is the fastest animation, speed 1 is the slowest animation. speed 0 is no animation

t.forward(150)       # move forward 150 pixels drawing a line as we go (because pen starts off down)
t.left(120)          # turn left 120 degrees
t.forward(300)       # move forward 300 pixels
t.goto(0, 0)         # absolute positioning can also be used instead of relative position

# There will be a line turtle.done() at the end of this file to keep window open.

# What we have learnt - Beginner
# 1. How to write and run a Python script
# 2. How to use a non-built-in library, import turtle
# 3. How to use text strings eg "turtle"
# 4. How to use integers eg 0, 150, 120, 300
# 5. How to store a value in a variable eg t =
# 6. How to comment code (start with #)
# 7. How to branch with a conditional if-else statement
# 8. How to create turtle graphics (straight lines) using absolute or relative methods
# What we have learnt - Intermediate
# 9. How to create an object of type Turtle (turtle.Turtle()) and call methods on that object (t.forward(150))

if fast_until_task > 2:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)           # speed 10 is the fastest animation, speed 1 is the slowest animation. speed 0 is no animation

# Task 2: Draw the same image rotated 180 degrees

t.right(120 + 180)
t.forward(150)
t.left(120)
t.forward(300)
t.goto(0, 0)

# Solution 2: Using all relative movements

t.setheading(90)  # absolute heading to get started
# Calculate length of final side
b = (300 * 300 - 150 * 150) ** 0.5  # Pythagoras a² + b² = c²

t.forward(150)
t.left(120)
t.forward(300)
t.left(150)
t.forward(b)

# What we have learnt - Beginner
# 1. Arithmetic on numbers, multiplication, subtraction, power, order of operations, ((300 * 300 - 150 * 150) ** 0.5)
# 2. Using literal values (150, 120) and variables (b) as arguments in a function or method (in parentheses)

if fast_until_task > 3:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

# Task 3: Draw with the 30° vertex in the centre

t.forward(b)
t.right(90)
t.forward(150)
t.right(120)
t.forward(300)
t.right(150)

# Solution 3: Using a loop

t.reset()  # clear all previous drawings
if fast_until_task > 3:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

t.color("red")
t.setheading(45)
for a in (70, 80, 90, 100):  # line before code block will end in :
    # code block is indented, usually 4 spaces but can be anything as long as consistent
    # code block will be run 4 times. Each time variable count will have a different value
    c = 2 * a
    b = (c * c - a * a) ** 0.5
    t.forward(b)
    t.right(90)
    t.forward(a)
    t.right(120)
    t.forward(c)
    t.right(60)
# Draw a circle around triangles
t.penup()    # stops turtle drawing
t.forward(c)
t.pendown()  # starts turtle drawing again
t.left(90)
t.circle(c)  # draws a circle. equivalent to t.circle(c, 360) to draw all 360° of arc anticlockwise

# What have we learnt - Beginner
# 1. How to use variables in arithmetic expressions (eg 2 * a)
# 2. How to create a tuple (sequence) of integers (70, 80, 90, 100)
# 3. How to do a for loop (for a in (70, 80, 90, 100):)
# 4. Turtle graphics to draw circles and arcs, turn on and off pen, clear screen

if fast_until_task > 4:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

# Task 4: draw a clock face, circle with radius 250 with short lines at hours of 3, 6, 9 and 12 being radius from 85% to 92%

radius = 250
t.penup()
t.goto(0, -radius)
t.setheading(0)
t.pendown()
t.circle(radius, 360)
for hour in (3, 6, 9, 12):
    t.penup()
    t.goto(0, 0)
    t.setheading(90 - hour * 30)
    t.forward(radius * 0.85)
    t.pendown()
    t.forward(radius * 0.07)


# Solution 4:
def jump_to(the_turtle, x, y):
    the_turtle.penup()
    the_turtle.goto(x, y)
    the_turtle.pendown()


def jump(the_turtle, distance):
    the_turtle.penup()
    the_turtle.forward(distance)
    the_turtle.pendown()


radius = 350
jump_to(t, 0, -radius)
t.color("#3333FF")
t.setheading(0)
t.circle(radius, 360)
for hour in range(1, 13):  # range(start, stop) iterates over sequence of integers from start up to but not including stop
    jump_to(t, 0, 0)
    t.setheading(90 - hour * 30)
    jump(t, radius * 0.85)
    t.forward(radius * 0.07)
jump_to(t, 0, radius + 10)
t.write("Turtle Time", align="center", font=("Arial", 20, "normal"))

# What we have learnt - Beginner
# 1. How to define a function (def jump(the_turtle, distance):)
# 2. How to use arguments/parameters in a function (the_turtle.penup())
# 3. How to use range(start, stop) in a for loop. Alternatives are range(stop), range(start, stop, step). see help(range)
# 4. Named arguments in a function (align="center", font=("Arial", 20, "normal")) as an alternative to positional arguments
# 5. Turtle graphics how to draw text (t.write)

if fast_until_task > 5:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

# Task 5: show clock numbers on clock

for hour in range(1, 13):  # range(start, stop) iterates over sequence of integers from start up to but not including stop
    jump_to(t, 0, 0)
    t.setheading(90 - hour * 30)
    jump(t, radius * 0.95)
    if fast_until_task < 6:
        t.write(hour)


# Solution 5:
FONT_SIZE = 20


def write_centre(the_turtle, text):
    """align text centred vertically and horizontally"""
    position = the_turtle.position()  # position() returns a tuple of (x, y) coordinates
    print(f"{position=}")
    original_y = position[1]          # x is position[0], y is position[1]
    the_turtle.penup()
    the_turtle.sety(original_y - 2/3 * FONT_SIZE)
    the_turtle.write(text, align="center", font=("Arial", FONT_SIZE, "normal"))
    the_turtle.sety(original_y)
    the_turtle.pendown()


hour = 1
while hour <= 12 and fast_until_task < 7:  # while loops until condition is false
    jump_to(t, 0, 0)
    t.setheading(90 - hour * 30)
    jump(t, radius * 0.8)
    write_centre(t, hour)
    hour += 1
jump_to(t, 20, 0)


# What we have learnt - Beginner
# 1. Variable naming - upper case for constants, lower case for variables (convention only)
# 2. Conditional expressions which return True or False (hour <= 12)
# 3. while loop
# 4. How to use square brackets to refer to members of a tuple by index (0 based)
# 5. Turtle graphics how to get and set position t.position(), t.setposition(), t.sety(), t.setx()
# 6. How to increment value of a variable "hour += 1" means the same as "hour = hour + 1" (almost. slight difference for mutable data types)

if fast_until_task > 6:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

# Task 6:
# Animated turtle follow the circle radius 295 all the way around leaving an arc width proportional to hour (1° per hour)

radius = 295
jump_to(t, 0, radius)
t.setheading(180)
t.color("green")
for hour in range(12, 0, -1):
    t.pendown()
    t.circle(radius, extent=hour)
    t.penup()
    t.circle(radius, extent=30-hour)

# Solution 6:
if fast_until_task < 7:
    radius = 260
    jump_to(t, 0, radius)
    t.setheading(0)
    t.penup()
    t.circle(-radius, extent=360 / 24)  # negative radius says do circle clockwise
    for hour in range(1, 13):
        extent = 360 / 24 - hour
        t.circle(-radius, extent=extent)
        for dot in range(hour):
            t.circle(-radius, extent=1)
            t.dot(3)
            t.circle(-radius, extent=1)
        t.circle(-radius, extent=extent)

# What we have learnt - Beginner
# 1. Using variable name same as class method name (dot)
# 2. Turtle graphics, clockwise circle, dot,

if fast_until_task > 7:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

# Task 7 - Clear a circle of radius 265 in centre of screen

# Solution 7
radius = 265
jump_to(t, 0, -radius)
t.setheading(0)
t.fillcolor("white")
t.begin_fill()
t.circle(radius)  # how to draw a circle which is filled with white colour
t.end_fill()

if fast_until_task > 8:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

# Task 8 - Melbourne Cup Day - Draw a stick horse

jump_to(t, -100, 0)
t.pd()
t.seth(90)
t.fd(50)
t.rt(90)
t.fd(50)
t.rt(90)
t.fd(50)
t.bk(50)
t.lt(135)
t.fd(50)
t.seth(0)


# Solution 8: def a function which includes a default scaling value
def draw_horse_38(the_turtle, scale=1):
    """function to draw a stick horse. Uses the Walrus operator := so requires Python 3.8 or later"""
    the_turtle.left(tail_angle := 15)  # turn left 15° AND assign 15 to variable tail_angle
    the_turtle.forward(tail := 5 * scale)
    the_turtle.right(tail_angle)
    the_turtle.forward(back := 5 * scale)
    the_turtle.left(neck_angle := 30)
    the_turtle.forward(neck := 5 * scale)
    the_turtle.right(head_angle := 90)
    the_turtle.forward(head := 3 * scale)
    the_turtle.back(head)
    the_turtle.left(head_angle)
    the_turtle.back(neck)
    the_turtle.right(neck_angle)
    the_turtle.right(90)
    the_turtle.forward(girth := 2 * scale)
    the_turtle.left(leg_angle := 45)
    the_turtle.forward(leg := 5 * scale)
    the_turtle.back(leg)
    the_turtle.right(90 + leg_angle)
    the_turtle.forward(back)
    the_turtle.left(90 - leg_angle)
    the_turtle.forward(leg)
    the_turtle.back(leg)
    the_turtle.right(180 - leg_angle)
    the_turtle.forward(girth)
    the_turtle.right(90)  # return to original heading


def draw_horse_36(the_turtle, scale=1):
    """function to draw a stick horse. Doesn't use the Walrus operator := so works in Python 3.6 or later (and probably earlier)"""
    tail_angle = 15
    tail = 5 * scale
    back = 5 * scale
    neck_angle = 30
    neck = 5 * scale
    head_angle = 90
    head = 3 * scale
    girth = 2 * scale
    leg_angle = 45
    leg = 5 * scale
    the_turtle.left(tail_angle)
    the_turtle.forward(tail)
    the_turtle.right(tail_angle)
    the_turtle.forward(back)
    the_turtle.left(neck_angle)
    the_turtle.forward(neck)
    the_turtle.right(head_angle)
    the_turtle.forward(head)
    the_turtle.back(head)
    the_turtle.left(head_angle)
    the_turtle.back(neck)
    the_turtle.right(neck_angle)
    the_turtle.right(90)
    the_turtle.forward(girth)
    the_turtle.left(leg_angle)
    the_turtle.forward(leg)
    the_turtle.back(leg)
    the_turtle.right(90 + leg_angle)
    the_turtle.forward(back)
    the_turtle.left(90 - leg_angle)
    the_turtle.forward(leg)
    the_turtle.back(leg)
    the_turtle.right(180 - leg_angle)
    the_turtle.forward(girth)
    the_turtle.right(90)


t.penup()
t.goto(0, 0)
t.pendown()
t.pensize(5)
t.color("brown")
draw_horse_36(t, 15)  # use draw_horse_39 if using python 3.8

# What we have learnt
# 1. Create a function with default values for parameters
# 2. Python 3.9 walrus operator
# 3. Turtle graphics abbreviated method names

if fast_until_task > 9:
    t.hideturtle()
    t.speed(0)
else:
    t.showturtle()
    t.speed(3)

# Task 9: Register shape using begin_poly, end_poly, register_shape and set this shape to turtle

jump_to(t, 0, 100)
t.pensize(1)
t.begin_poly()
draw_horse_38(t, 1)  # or draw_horse_36(t)
t.end_poly()
turtle.register_shape("horse", t.get_poly())
t.hideturtle()
t = turtle.Turtle()  # This shouldn't be necessary but seems to be required to take shape, speed and showturtle
t.shape("horse")
print(f"{t.speed()=}")  # remove = if using earlier than python 3.8
t.showturtle()
jump_to(t, 0, 200)
if fast_until_task < 10:
    t.forward(100)


# Solution 9:
t.penup()
# Important to set position and heading before beginning polygon as prior example showed
t.goto(0, 0)
t.setheading(90)
t.begin_poly()
draw_horse_38(t)  # or draw_horse_36(t)
t.end_poly()
turtle.register_shape("horse", t.get_poly())
t.shape("horse")
t.forward(100)

# How to create additional turtles
t1 = turtle.Turtle()
t1.color("aqua")
t1.fillcolor("blue")
t1.speed(3)
t1.shape("horse")
t2 = turtle.Turtle()
t2.color("violet")
t2.speed(3)
t2.shape("horse")
# Create dicts which have information about each turtle
r1 = {"turtle": t1, "radius": 255, "laps": 0}
r2 = {"turtle": t2, "radius": 245, "laps": 0}
racers = [r1, r2]  # a list of dicts (dictionaries)
for r in racers:
    jump_to(r['turtle'], 0, -r['radius'])
while r1['laps'] < 1 and r2['laps'] < 1:
    for r in racers:
        prev_heading = r['turtle'].heading()
        r['turtle'].circle(r['radius'], random.choice([3, 4, 5]))
        if r['turtle'].heading() < prev_heading:
            r['laps'] += 1

# What we have learnt - Beginner
# 1. How to use dict (create, get value for key, set value for key)
# 2. How to generate random numbers using standard library random
# 3. How to use multiple turtles, create shapes, register shapes


turtle.done()        # keep window open so program doesn't quit immediately it gets to the end
# Now check out the demo
# From terminal type 'python -m turtledemo' (without the quotes)
