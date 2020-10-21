#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 083 - Beginners' Python and Machine Learning - 27 Sep 2020 - tkinter and keyring

Learning objectives
 - Graphical User Interface
 - storing passwords

Reference:
https://docs.python.org/3/library/tkinter.html
https://realpython.com/python-gui-tkinter/
https://pypi.org/project/keyring/

@author D Tim Cummings

Requires Python 3 installed on your computer
tkinter is included in the standard or anaconda python3 install on Mac and Windows

On debian based linux
sudo apt install python3-tk

On MacPorts python
sudo port install py39-tkinter

Task 1. Create new virtual environment. I find I need to inherit global site packages (sometimes)
python3 -m venv venv --system-site-packages

# Create virtual environment
python -m venv venv --system-site-packages         # Windows
python3 -m venv venv --system-site-packages        # Mac or Linux
conda create --name venv-bpaml-tkinter python=3.9  # Anaconda

# activate virtual environment
source venv/bin/activate                    # Mac or Linux or Windows Bash
conda activate venv-bpaml-tkinter           # Anaconda
venv\Scripts\activate.bat                   # Windows command prompt
venv\Scripts\Activate.ps1                   # Windows powershell

# install keyring when virtual environment active
pip install keyring
"""
import datetime
import getpass
import keyring
import logging
import tkinter as tk

# Task 2. Create a window. Add a label with some text and run the event loop

window = tk.Tk()
lbl_heading = tk.Label(text="My first GUI app")
lbl_heading.grid()
# There is also a line tk.mainloop() at the very bottom of this file to run the event loop and display window

# Task 3. Change text to be "Switchboard" using lbl_heading.config(text=s)


# Solution 3: Also format the text to be left justified using Label(justify=tk.LEFT).

# lbl_heading['text'] = "Switchboard"  # Alternative way of changing title
#
#
# # Add a button to show help on tkinter grid
# def click_help_grid():
#     top = tk.Toplevel(window)
#     top.title("help(grid)")
#     lbl_help = tk.Label(master=top, text=tk.Label.grid.__doc__, justify=tk.LEFT)
#     lbl_help.grid()  # grid lays elements out in a grid. default is single column many rows
#
#
# # remember to omit parentheses when passing function as an argument
# btn_help_grid = tk.Button(text="help(grid)", command=click_help_grid)
# btn_help_grid.grid()
#
#
# # Task 4: Add another button to see help on bind
# def click_help_bind():
#     top = tk.Toplevel(window)
#     top.title("help(bind)")
#     lbl_help = tk.Label(master=top, text=tk.Label.bind.__doc__, justify=tk.LEFT)
#     lbl_help.grid()
#
#
# btn_help_bind = tk.Button(text="help(bind)", command=click_help_bind)
# btn_help_bind.grid()
#
#
# # Solution 4: Making the solution generic, adding a button in new window, using pack rather than grid
# def click_help_by_name(name):
#     top = tk.Toplevel(window)
#     top.title(f"help({name})")
#     lbl_help = tk.Label(master=top, text=getattr(tk.Label, name).__doc__, justify=tk.LEFT, font=("Andale Mono", 14))
#     lbl_help.pack()  # pack is an alternative geometry manager to grid. Can pack from one side in a column or row
#     btn_close = tk.Button(master=top, text="close", command=top.destroy)
#     btn_close.pack()
#
#
# def add_button_for_help(name):
#     btn_help = dict()
#     # use lambda to define a function on one line. Our one line function (no args) calls another function with one arg.
#     btn_help[name] = tk.Button(text=f"help({name})", command=lambda: click_help_by_name(name))
#     btn_help[name].grid()
#
#
# add_button_for_help("pack")
# add_button_for_help("config")
#
# # Task 5: Add a button which creates a window showing the current time
#
#
# def click_time_now():
#     top = tk.Toplevel(window)
#     lbl_time = tk.Label(master=top, text=datetime.datetime.now().strftime("%H:%M:%S"), font=("Courier", 60))
#     lbl_time.pack()
#
#
# btn_time_now = tk.Button(text="Time now", command=click_time_now)
# btn_time_now.grid(row=1, column=1)
#
#
# # Solution 5: Time which updates
# def click_time_clock():
#     fmt = "%H:%M:%S [%f]"
#
#     def update_time_clock():
#         # this function has to be a sub function of click_time_clock so lbl_time variable is in scope
#         now = datetime.datetime.now()
#         lbl_time['text'] = now.strftime(fmt)
#         iv_countdown.set(max(iv_countdown.get() - 1, 0))
#         # every time update_time_clock is called it tells event loop when it wants to run the next time using after()
#         lbl_time.after(1000 - now.microsecond // 1000, update_time_clock)
#
#     top = tk.Toplevel(window)
#     top.title("Clock")
#     lbl_time = tk.Label(master=top, text="start me", font=("Courier", 60))
#     lbl_time.pack()
#     # How to add an editable number field. How to use pack() to layout horizontally
#     frm = tk.Frame(top)
#     lbl_countdown = tk.Label(frm, text="Countdown")
#     lbl_countdown.pack(side=tk.LEFT)
#     iv_countdown = tk.IntVar(value=10)
#     ent_countdown = tk.Entry(frm, textvariable=iv_countdown)
#     ent_countdown.pack(side=tk.LEFT)
#     frm.pack()
#     # Start the clock
#     update_time_clock()
#
#
# btn_time_clock = tk.Button(text="Time clock", command=click_time_clock)
# btn_time_clock.grid(row=2, column=1, sticky="e")
#
# # Following is required for task 6
# sv_service_name = tk.StringVar(value="bpaml-tkinter-demo")
# # Task 6: Create a window which accepts a string (into tk.StringVar sv_service_name) with a label "Service name"
#
#
# def click_service_name():
#     top = tk.Toplevel()
#     lbl_service_name = tk.Label(top, text="Service name")
#     lbl_service_name.pack(side=tk.LEFT)
#     ent_service_name = tk.Entry(top, textvariable=sv_service_name)
#     ent_service_name.pack(side=tk.LEFT)
#
#
# btn_service_name = tk.Button(text="Service name", command=click_service_name)
# btn_service_name.grid(row=3, column=1)
#
#
# # Solution 6: Collecting service name, username and password
#
# sv_username = tk.StringVar(value=getpass.getuser())
# sv_password = tk.StringVar()
#
#
# def menu_authentication():
#
#     def click_save_password():
#         keyring.set_password(sv_service_name.get(), username=sv_username.get(), password=sv_password.get())
#         # Following line uses Python 3.8 f-strings. Remove "=" signs for Python 3.7
#         logging.warning(f"{sv_username.get()=} {sv_password.get()=} {keyring.get_password(sv_service_name.get(), sv_username.get())=}")
#         sv_password.set("")
#         top.destroy()
#
#     top = tk.Toplevel(window)
#     top.title("Authenticate")
#     top.geometry("+50+300")  # width x height + top left x + top left y of window excluding title bar
#     frm = tk.LabelFrame(master=top, text='Enter credentials')
#     frm.pack()
#
#     tk.Label(master=frm, text="Service name").grid(row=0, column=0)
#     tk.Label(master=frm, text="Username").grid(row=1, column=0)
#     tk.Label(master=frm, text="Password").grid(row=2, column=0)
#     tk.Entry(master=frm, textvariable=sv_service_name).grid(row=0, column=1)
#     tk.Entry(master=frm, textvariable=sv_username).grid(row=1, column=1)
#     tk.Entry(master=frm, textvariable=sv_password, show="•").grid(row=2, column=1)
#     tk.Button(master=frm, text="Save password", command=click_save_password).grid(row=3, column=1, sticky="e")
#
#
# # Use menu rather than button
# menu_bar = tk.Menu(window)
# edit_menu = tk.Menu(menu_bar, tearoff=0)
# edit_menu.add_command(label="Authentication", command=menu_authentication)
# menu_bar.add_cascade(label="Edit", menu=edit_menu)
# window.config(menu=menu_bar)
#
#
# # Task 7: Add a menu item which prints password from keyring
# def menu_print_password():
#     print(f"{keyring.get_password(sv_service_name.get(), sv_username.get())=}")
#
#
# edit_menu.add_command(label="Print password", command=menu_print_password)
#
#
# # Solution 7: Also add keyboard shortcut for menu
# def menu_log_password(event=None):
#     # Normally you would never log a password at any level. This is for demo purposes only
#     logging.warning(f"{keyring.get_password(sv_service_name.get(), sv_username.get())=} {sv_service_name.get()=} {sv_username.get()=}")
#
#
# edit_menu.add_command(label="Log password", command=menu_log_password, underline=0, accelerator="Ctrl-l")
# window.bind_all("<Control-l>", menu_log_password)
#
# # Task 8: Create a window with a canvas and draw based on mouse down events
#
#
# # Solution 8:
# def click_btn_draw():
#     start = {"x": 0, "y": 0}
#
#     def mouse_down(event):
#         start['x'], start['y'] = event.x, event.y
#
#     def mouse_motion(event):
#         canvas.create_line((start['x'], start['y'], event.x, event.y))
#         start['x'], start['y'] = event.x, event.y
#
#     top = tk.Toplevel(bg='gray')
#     top.geometry("680x520")
#
#     canvas = tk.Canvas(top, width=640, height=480)
#     canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#     canvas.bind("<Button-1>", mouse_down)
#     canvas.bind("<B1-Motion>", mouse_motion)
#
#
# btn_draw = tk.Button(text="Drawing", command=click_btn_draw)
# btn_draw.grid(row=4, column=1, sticky="e")
#
tk.mainloop()
