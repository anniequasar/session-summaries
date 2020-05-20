#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 058 - Beginners' Python and Machine Learning - Tue 05 May 2020 - pythonator

https://youtu.be/h3IwMGri428

Learning objectives:
- python for absolute beginners
- use python to build in a Minetest 3D virtual world

To follow these tasks you will need to install:
- Python 3.6 or later  https://python.org
- PyCharmEdu 2020.1 or PyCharm Community Edition 2020.1 with EduTools plugin  https://jetbrains.com
- Minetest 5 or later  https://www.minetest.net

For instructions on how to install go to https://pythonator.com

It is recommended you run these tasks inside PyCharm Edu but you can alternatively run this script on its own.
To do this you will need to install ircbuilder using pip or requirements.txt
    pip install ircbuilder>=0.0.8

Then fill in your connection details in Task 0 for mtuser, mtuserpass and player_z.

@author D Tim Cummings
"""
from ircbuilder import MinetestConnection

###################################################################################
# Task 0 - Configure your connection details with Minetest
mtuser = "your_username"      # your minetest username
mtuserpass = "your_password"  # your minetest password. This file is not encrypted so don't use anything you want kept secret
player_z = 10                 # your z value from sign in minetest with your username on it
# The following must match your settings in minetest server > Settings > Advanced Settings > Mods > irc > Basic >
ircserver = "irc.triptera.com.au"  # same as IRC server
mtbotnick = "mtserver"  # same as Bot nickname
channel = "#pythonator"  # same as Channel to join
mc = MinetestConnection.create(ircserver, mtuser, mtuserpass, mtbotnick, channel)

###################################################################################
# Tasks 1 to 3: Build a glass cube with coloured wool in the centre

ref_x = 100
ref_y = 14
ref_z = player_z
wool = "wool:yellow"
glass = "default:glass"

seq_x = (ref_x - 1, ref_x, ref_x + 1)
seq_y = (ref_y - 1, ref_y, ref_y + 1)
seq_z = (ref_z - 1, ref_z, ref_z + 1)
mc.build(seq_x, seq_y, seq_z, glass)
mc.build(ref_x, ref_y, ref_z, wool)
mc.send_building()

###################################################################################
# Tasks 4 and 5: Build a glass tunnel with a stone floor and torches every 4 blocks
# BUILDING LOCATION
x_max = 93
x_min = 70
floor_y = 14

# BUILDING SIZE
tunnel_height = 7
tunnel_width = 5

# BUILDING MATERIALS
air = "air"
wall = "default:glass"
floor = "default:stone"
torch = "default:torch"

# ENGINEERING CALCULATIONS

tunnel_length = x_max - x_min + 1

wall_z = ref_z - tunnel_width // 2
# x values for tunnel glass and air
range_x = range(x_min, x_min + tunnel_length)
# y and z values for tunnel glass (external)
range_y_ext = range(floor_y, floor_y + tunnel_height)
range_z_ext = range(wall_z, wall_z + tunnel_width)
# y and z values for tunnel air (internal)
range_y_int = range(floor_y + 1, floor_y + tunnel_height - 1)
range_z_int = range(wall_z + 1, wall_z + tunnel_width - 1)
# x values for torches
range_x_torch = range(x_min, x_max, 4)

# BUILD
# build a solid cuboid of glass first which is 7 blocks high and 5 blocks wide
mc.build(range_x, range_y_ext, range_z_ext, wall)
# replace the internal glass with air so left with a hollow tunnel
mc.build(range_x, range_y_int, range_z_int, air)
# replace the floor with stone
mc.build(range_x, floor_y, range_z_int, floor)
# place torches
mc.build(range_x_torch, floor_y + 1, ref_z + 1, torch)
mc.send_building()

###################################################################################
# Task: Arches

# BUILDING LOCATION
# x value at start of stone path heading +x direction
path_x_min = 105
# y value of stone in path
floor_y = 9

# BUILDING SIZE
# height of arch in number of blocks (external dimension)
arch_height = 7
# width of arch in number of blocks (external dimension)
arch_width = 5
# path length
path_length = 16

# BUILDING MATERIALS
air = "air"
wall = "default:glass"
floor = "default:stone"
torch = "default:torch"

# ENGINEERING CALCULATIONS
# z value of side of arch (where wall_z < player_z)
wall_z = ref_z - arch_width // 2

# x value for arch location
range_x_arch = range(path_x_min, path_x_min + path_length, 4)

# external dimensions of arch
range_y_ext = range(floor_y, floor_y + arch_height)
range_z_ext = range(wall_z, wall_z + arch_width)
# internal dimensions of arch
range_y_int = range(floor_y + 1, floor_y + arch_height - 1)
range_z_int = range(wall_z + 1, wall_z + arch_width - 1)

# BUILD
# clear any existing structure or ground
mc.build(range(path_x_min, path_x_min + 40), range(floor_y + 1, floor_y + 31), range(ref_z - 4, ref_z + 5), air)
# build a solid cuboid of glass first which is 7 blocks high and 5 blocks wide
mc.build(range_x_arch, range_y_ext, range_z_ext, wall)
# replace the internal glass with air so left with a hollow tunnel
mc.build(range_x_arch, range_y_int, range_z_int, air)
# replace the floor with stone
mc.build(range_x_arch, floor_y, range_z_int, floor)
# place a torch in each arch
mc.build(range_x_arch, floor_y + 1, ref_z + 1, torch)
mc.send_building()

###################################################################################
# Task: Castle

# BUILDING LOCATION
# x value at start of stone path heading +x direction
path_x_min = 105
# x value at start of castle
castle_x_min = 121
# y value of floor of castle
floor_y = 9

# BUILDING SIZE
# castle length (in x direction)
castle_length = 9
# castle width (in z direction)
castle_width = 5
# castle height excluding roof including floor
castle_height = 5

# BUILDING MATERIALS
air = "air"
castle = "default:stone"
# player looking in x direction to look through this window
window_x = {"name": "xpanes:bar_flat", "direction": "+x"}
# player looking in z direction to look through this window
window_z = {"name": "xpanes:bar_flat", "direction": "+z"}
# player looking in x direction to climb this ladder.
ladder = {"name": "default:ladder_wood", "direction": "+x"}
carpet = "wool:red"
# direction specifies which way player is facing when opening door.
door = {"name": "doors:door_wood_a", "direction": "+x"}
# torches. Direction specifies which way player facing to view torch
torch_n = {"name": "default:torch_wall", "direction": "-z"}
torch_s = {"name": "default:torch_wall", "direction": "+z"}


# ENGINEERING CALCULATIONS
# z values of sides of castle
wall_z1 = ref_z - castle_width // 2
wall_z2 = ref_z + castle_width // 2
# external dimensions of castle base
range_x_castle_ext = range(castle_x_min, castle_x_min + castle_length)
range_y_castle_ext = range(floor_y, floor_y + castle_height)
range_z_castle_ext = range(wall_z1, wall_z1 + castle_width)
# internal dimensions of castle base
range_x_castle_int = range(castle_x_min + 1, castle_x_min + castle_length - 1)
range_y_castle_int = range(floor_y + 1, floor_y + castle_height)
range_z_castle_int = range(wall_z1 + 1, wall_z1 + castle_width - 1)
# height of side windows from 2 above floor to height of castle
range_y_window = range(floor_y + 2, floor_y + castle_height)
# place side windows every 2 blocks starting from second block from door
range_x_window = range(castle_x_min + 2, castle_x_min + castle_length - 2, 2)
# external dimensions of castle roof
range_x_roof_ext = range(castle_x_min - 1, castle_x_min + castle_length + 1)
range_y_roof_ext = range(floor_y + castle_height, floor_y + castle_height + 3)
range_z_roof_ext = range(wall_z1 - 1, wall_z1 + castle_width + 1)
range_x_roof_int = range_x_castle_ext
range_y_roof_int = range(floor_y + castle_height + 1, floor_y + castle_height + 3)
range_z_roof_int = range_z_castle_ext
# location of crenels and merlons on castle roof
crenel_y = floor_y + castle_height + 2
roof_x1 = castle_x_min - 1
roof_x2 = castle_x_min + castle_length
roof_z1 = wall_z1 - 1
roof_z2 = wall_z2 + 1

# BUILD
# clear any existing structure or ground
mc.build(range(castle_x_min - 1, castle_x_min + castle_length + 10), range(floor_y + 1, floor_y + 31), range(ref_z - 4, ref_z + 5), air)
# the base of the castle
mc.build(range_x_castle_ext, range_y_castle_ext, range_z_castle_ext, castle)
mc.build(range_x_castle_int, range_y_castle_int, range_z_castle_int, air)
# create a doorway
mc.build(castle_x_min, [floor_y + 1, floor_y + 2], ref_z, air)
# add windows on side walls
mc.build(range_x_window, range_y_window, (wall_z1, wall_z2), window_z)
# add windows on front wall
mc.build(castle_x_min, floor_y + 4, (ref_z - 1, ref_z, ref_z + 1), window_x)
# the roof of the castle
mc.build(range_x_roof_ext, range_y_roof_ext, range_z_roof_ext, castle)
mc.build(range_x_roof_int, range_y_roof_int, range_z_roof_int, air)
# build the ladder. Has to be against wall for player to climb it easily.
mc.build(castle_x_min + castle_length - 2, range(floor_y + 1, floor_y + castle_height + 1), ref_z, ladder)
# build crenels on roof
mc.build([roof_x1, roof_x2], crenel_y, range(wall_z1, wall_z1 + castle_width, 2), air)
mc.build(range(castle_x_min, castle_x_min + castle_length, 2), crenel_y, (roof_z1, roof_z2), air)
# build a door
mc.build(castle_x_min, floor_y + 1, ref_z, door)
# lay the red carpet
mc.build(range(path_x_min, castle_x_min + castle_length - 1), floor_y, ref_z, carpet)
# torches
mc.build(range(castle_x_min + 1, castle_x_min + castle_length - 1, 2), floor_y + 3, wall_z1 + 1, torch_n)
mc.build(range(castle_x_min + 1, castle_x_min + castle_length - 1, 2), floor_y + 3, wall_z2 - 1, torch_s)
mc.send_building()

###################################################################################
# Task: Flag

# LOCATION
pole_x = 122
pole_y = 15
flag_y = 22

# SIZE
flag_height = 13
flag_length = 21


# SHAPE
def rectangle_flag(global_x, global_y):
    local_x = global_x - pole_x
    local_y = global_y - flag_y
    if local_x < 0 or local_x >= flag_length:
        return False
    if local_y < 0 or local_y >= flag_height:
        return False
    return True


def top_triangle_flag(global_x, global_y):
    local_x = global_x - pole_x
    local_y = global_y - flag_y
    row_length = flag_length * local_y // flag_height + 1
    if local_x < 0 or local_x >= row_length:
        return False
    if local_y < 0 or local_y >= flag_height:
        return False
    return True


def half_ellipse_flag(global_x, global_y):
    local_x = global_x - pole_x
    local_y = global_y - flag_y
    if local_y < 0 or local_y >= flag_height:
        return False
    if local_x == 0:
        return True
    local_y -= flag_height // 2
    r2 = (local_x / flag_length) ** 2 + (2 * local_y / flag_height) ** 2
    return r2 <= 1.0


# BUILDING MATERIALS
air = "air"
pole = "default:fence_junglewood"
colours = ["wool:" + colour for colour in "white|grey|dark_grey|black|blue|cyan|green|dark_green|yellow|orange|brown|red|pink|magenta|violet".split("|")]

# ENGINEERING CALCULATIONS
num_colours = len(colours)
stripe_width = 2

mc.build(pole_x, range(pole_y, flag_y), ref_z, pole)
mc.build(range(pole_x, pole_x + 26), range(flag_y, flag_y + 26), range(ref_z - 4, ref_z + 5), air)
for x in range(pole_x, pole_x + flag_length):
    for y in range(flag_y, flag_y + flag_height):
        # pattern centred on centre of flag
        cx = pole_x + flag_length / 2
        cy = flag_y + flag_height / 2
        # pattern centred on front bottom corner
        # cx = pole_x
        # cy = flag_y

        # c = x // 2 % 15  # vertical stripes
        # c = y // 2 % 15  # horizontal stripes
        # c = (x+y)//2 % 15  # diagonal stripes
        # c = (x-y)//2 % 15  # other diagonal stripes
        # c = int(sqrt((x-cx)**2 + (y-cy)**2)) // stripe_width % num_colours  #  circles centred on cx, cy
        # c = int(max(abs(x-cx), abs(y-cy))) % len(colours)  # squares centred on cx, cy
        c = int(min(abs(x-cx), abs(y-cy))) % len(colours)  # cross centred on cx, cy
        colour = colours[c]
        if rectangle_flag(x, y):
            mc.build(x, y, ref_z, colour)
        else:
            mc.build(x, y, ref_z, "air")

mc.send_building()
