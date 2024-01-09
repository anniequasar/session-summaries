r"""MeetUp 144 - Beginners' Python and Machine Learning - 31 May 2022 - tkinter and wordle

Youtube: https://youtu.be/EZnSHYC_eG4
Github:  https://github.com/timcu/bpaml-sessions/raw/master/online/meetup144_tim_wordle_tkinter.py
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/285475011/

Learning objectives
 - Graphical User Interface
 - tkinter styles
 - tkinter event handling

Reference:
    https://docs.python.org/3/library/tkinter.html
    https://docs.python.org/3/library/tk.html
    https://tkdocs.com/tutorial/
    https://realpython.com/python-gui-tkinter/

@author D Tim Cummings

Requires Python 3 installed on your computer
tkinter is included in the standard or anaconda python3 install on Mac and Windows

On debian based linux
sudo apt install python3-tk

On MacPorts python
sudo port install py39-tkinter

# Create virtual environment
py -m venv bpaml144 --system-site-packages             # Windows
python3 -m venv bpaml144 --system-site-packages        # Mac or Linux
conda create --name venv-bpaml144 python=3.9           # Anaconda

# activate virtual environment
source bpaml144/bin/activate                    # Mac or Linux or Windows Bash
conda activate venv-bpaml144                    # Anaconda
bpaml144\Scripts\activate.bat                   # Windows command prompt
bpaml144\Scripts\Activate.ps1                   # Windows powershell
"""
import json
import logging
import random
import re
import tkinter.font
from urllib.request import urlopen
from bs4 import BeautifulSoup

import tkinter as tk
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)

# Remember from meetup083 the minimal tkinter program
#   window = tk.Tk()
#   lbl_heading = tk.Label(text="My first GUI app")
#   lbl_heading.grid()
#   tk.mainloop()

# This code already provides first and last lines
root = tk.Tk()

# Task 1: Create a simple tkinter program using themed label widget from tkinter.ttk not classic label from tkinter
# Use function as best practice to avoid polluting global namespace with global variables (classes even better)


# Solution 1:
def s1_ttk_label():
    top = tk.Toplevel(root)
    lbl = ttk.Label(master=top, text="Meetup 145 - Wordle", font="Courier 30 bold italic")
    lbl.grid()


# Enable next line to test solution 1
# s1_ttk_label()

# Themed widgets should use styles rather than direct formatting. The default style for labels is called TLabel
# First get link to style database
style = ttk.Style()


def ttk_label_using_style():
    """Changes default style of label so all labels use the same style"""
    top = tk.Toplevel(root)
    top.geometry("+700+100")  # width x height + top left x + top left y of window excluding title bar
    lbl1 = ttk.Label(master=top, text="Themed label using default style")
    lbl1.grid()
    lbl2 = ttk.Label(master=top, text="Second label also using default style")
    lbl2.grid()
    # Confirm the default style name
    logger.warning(f"Default style name for {type(lbl1)} is {lbl1.winfo_class()}")
    logger.warning(f"{tkinter.font.names()=}")
    for font_name in tkinter.font.names():
        logger.warning(f"{font_name} uses font family {tk.font.nametofont(font_name)['family']}")
    # Use the same family as TkFixedFont but give it a font size of 30pt (+ve for pt, -ve for px)
    # Font can be specified using tuple eg ("courier", 15, "bold", "italic") or str "courier 15 bold italic"
    style.configure(lbl1.winfo_class(), font=(tk.font.nametofont('TkFixedFont')['family'], 20))


# ttk_label_using_style()
# Changing style 'TLabel' changes default style for all labels
# Creating a style 'Error.TLabel' will start with the default style and make a change


def ttk_label_using_sub_style():
    """Changes default style of label so all labels use the same style"""
    top = tk.Toplevel(root)
    top.geometry("+700+400")  # width x height + top left x + top left y of window excluding title bar
    lbl1 = ttk.Label(master=top, text="Themed label using default style")
    lbl1.grid()
    lbl2 = ttk.Label(master=top, text="Second label also using style Error.TLabel")
    lbl2.grid()
    style.configure("Error.TLabel", foreground="red")
    lbl2['style'] = "Error.TLabel"


# Run following line with and without running ttk_label_with_style()
# ttk_label_using_sub_style()

# Define constants (see meetup137)
URL = "https://nytimes.com/games/wordle/index.html"
FIVE_LETTER_ANSWERS = "five_letter_answers.txt"
FIVE_LETTER_GUESSES = "five_letter_guesses.txt"
# These constants from meetup137 will have different values which will be explained later
CORRECT = f'Correct.Letter.TLabel'
MOVE = f'Move.Letter.TLabel'
WRONG = f'Wrong.Letter.TLabel'
RESET = f'Reset.Letter.TLabel'

LETTER = f'Letter.TLabel'
ERROR = f'Error.Letter.TLabel'
ANSWER = f'Answer.Letter.TLabel'
style.configure(LETTER, font="sans-serif 30", anchor="center", borderwidth="2", relief=tk.GROOVE)
style.configure(ERROR, foreground="red")
style.configure(ANSWER, borderwidth="0")
style.configure(CORRECT, background='green')
style.configure(MOVE, background='yellow')
style.configure(WRONG, background='white')
style.configure(RESET, background='light grey')

# Task 2: Draw a window with a label with a grooved border, red sans-serif text 30pt


# Solution 2: Introducing padx, pady, sticky, grid_columnconfigure
def s2_red_bordered_label():
    top = tk.Toplevel(root)
    top.geometry("+700+700")  # width x height + top left x + top left y of window excluding title bar
    lbl1 = ttk.Label(master=top, text="Solution")
    lbl1.grid(row=0, column=0, padx=5, pady=5)
    lbl1['style'] = ERROR
    lbl2 = ttk.Label(master=top, text="2")
    lbl2.grid(row=0, column=1, padx=5, pady=5)
    lbl2['style'] = ERROR
    lbl3 = ttk.Label(master=top, text="Sticky")
    lbl3.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
    lbl3['style'] = ERROR
    # make columns 1 and 2 stretch as window stretches
    top.grid_columnconfigure(1, weight=1)
    top.grid_columnconfigure(2, weight=1)


# s2_red_bordered_label()

# Task 3: Make a grid fo 7 rows by 5 columns of labels which all stretch to be equally spaced


# Solution 3: Introducing minsize
def s3_grid_7x5():
    top = tk.Toplevel(root)
    top.geometry("+100+400")  # width x height + top left x + top left y of window excluding title bar
    for r in range(7):
        for c in range(5):
            lbl = ttk.Label(master=top, text=f"{r}{c}")
            lbl.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            lbl['style'] = LETTER
            top.grid_columnconfigure(c, weight=1, minsize=75)
        top.grid_rowconfigure(r, weight=1, minsize=75)


# s3_grid_7x5()

# Task 4: Using what you learnt in meetup083, root.bind "<Key>" to a method which logs event.char


# Solution 4
def s4_handle_keypress(event):
    # modifier keys return zero length str so check len first
    if len(event.char) > 0:
        logger.warning(f"{event.char} {ord(event.char)}")


# root.bind("<Key>", s4_handle_keypress)

# Task 5: Create labels again from task 3 but incorporate event handler to change text one label at a time on keypress


# Solution 5:
def s5_keypress_change_labels():
    top = tk.Toplevel(root)
    top.geometry("+700+400")  # width x height + top left x + top left y of window excluding title bar
    lst_labels = []
    for r in range(7):
        for c in range(5):
            lbl = ttk.Label(master=top, text=f"{r}{c}")
            lbl.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            lbl['style'] = LETTER
            lst_labels.append(lbl)
            top.grid_columnconfigure(c, weight=1, minsize=75)
        top.grid_rowconfigure(r, weight=1, minsize=75)
    idx = 0

    def handle_keypress_for_lst_labels(event):
        nonlocal idx
        if 'a' <= event.char <= 'z':
            lst_labels[idx]['text'] = event.char
            idx = (idx + 1) % len(lst_labels)
            logger.warning(f"{event.char} {idx} {ord(event.char)}")

    root.bind("<Key>", handle_keypress_for_lst_labels)


# s5_keypress_change_labels()

# Now we can incorporate the functions to fetch word lists and calculate clues from meetup142 and meetup137
# Task 6 is to understand how create_letters() and handle_keypress() work together


def fetch_word_lists():
    """From meetup142 fetch word lists from javascript of real wordle game and cache locally"""
    try:
        with open(FIVE_LETTER_ANSWERS) as f:
            lst_answers = [w.strip() for w in f]
        logger.info("read answers from file")
        with open(FIVE_LETTER_GUESSES) as f:
            lst_guesses = [w.strip() for w in f]
        logger.info("read guesses from file")
    except FileNotFoundError:
        logger.info(f"fetch answers and guesses from web {URL}")
        with urlopen(URL) as page:
            soup = BeautifulSoup(page, features="lxml")
        script = soup.find("script", src=True, defer=False)
        url_js = URL[:URL.rfind("/") + 1] + script["src"]
        with urlopen(url_js) as js_response:
            str_js = js_response.read().decode(js_response.headers.get_content_charset())
        ptn = re.compile(r"""(\[[a-z,"'\s]{5000,}])""")
        lst_match = ptn.findall(str_js)
        lst_answers = sorted(json.loads(lst_match[0]))
        with open(FIVE_LETTER_ANSWERS, "w") as file_answers:
            for w in lst_answers:
                file_answers.write(w + "\n")
        lst_guesses = sorted(json.loads(lst_match[1]))
        with open(FIVE_LETTER_GUESSES, "w") as file_guesses:
            for w in lst_guesses:
                file_guesses.write(w + "\n")
    return lst_answers, lst_guesses


def clues(answer, guess):
    """From meetup137 return clues for current guess for given answer finding exact and partial matches"""
    # convert str to list of letters
    lst_answer = list(answer)
    # store all clues in list initialising them to empty str
    lst_clue = [''] * len(answer)
    for i, letter in enumerate(guess):
        # First pass is to look for exact matches
        if letter == answer[i]:
            lst_clue[i] = CORRECT
            # This was an exact match so remove from answer, so it doesn't trigger in second pass
            lst_answer[i] = None
    for i, letter in enumerate(guess):
        # Now we only need to look at letters which weren't exact matches in the first pass
        if lst_clue[i] == '':
            if letter in lst_answer:
                lst_clue[i] = MOVE
                # This was a partial match so still remove from answer, so it doesn't trigger twice in second pass
                lst_answer.remove(letter)
            else:
                lst_clue[i] = WRONG
    return lst_clue


def find_possible(dct_clue_per_guess, lst_possible_prev):
    """From meetup142 - for easy mode - find limited possibilities given all clues so far"""
    possible = lst_possible_prev
    for guess, lst_clue in dct_clue_per_guess.items():
        possible = [word for word in lst_possible_prev if clues(word, guess) == lst_clue]
    return possible


def create_letters():
    """Add a 7 x 5 grid to window with squares for letters to by typed in and row at bottom to display answer"""
    dct_labels = {}
    for r in range(7):
        # Make frames auto-expand as window is stretched vertically
        root.grid_rowconfigure(r, weight=1, minsize=75)
        for c in range(5):
            if r == 0:
                # Make labels auto-expand as window is stretched horizontally
                root.grid_columnconfigure(c, weight=1, minsize=75)
            lbl = ttk.Label(master=root, text='', style=LETTER)
            if r == 6:
                lbl['style'] = ANSWER
            dct_labels[(r, c)] = lbl
            lbl.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

    def handle_keypress(event):
        """Nested function so dct_labels is in scope of this event handler"""
        handle_keypress_for_letters(event, dct_labels)

    root.bind("<Key>", handle_keypress)


def handle_keypress_for_letters(event, dct_labels):
    """Event handler. Needs to change values of three global variables"""
    global current_guess, current_letter, lst_possible
    if len(event.char) < 1:
        return
    logger.debug(f"{event.char=}, {ord(event.char)=}, {current_guess=}, {current_letter=}")
    if ord(event.char) == 8:  # backspace key
        if current_letter > 0:
            current_letter -= 1
        for col in range(5):
            dct_labels[(current_guess, col)]['style'] = RESET
    if current_letter < 5 and current_guess < 6:
        lbl_current = dct_labels[(current_guess, current_letter)]
        if 'a' <= event.char <= 'z':
            lbl_current['text'] = event.char
            current_letter += 1
        elif ord(event.char) == 8:
            lbl_current['text'] = ''
    elif event.char in '\r\n':
        if current_guess < 6:
            the_guess = "".join([dct_labels[(current_guess, col)]['text'] for col in range(5)])
            if the_guess not in lst_all_valid_guesses:
                logger.error(f"Not a word {the_guess}")
                for col in range(5):
                    dct_labels[(current_guess, col)]['style'] = ERROR
            else:
                dct_clue[the_guess] = clues(the_answer, the_guess)
                for col, clue in enumerate(dct_clue[the_guess]):
                    lbl_letter = dct_labels[(current_guess, col)]
                    lbl_letter['style'] = clue
                    # lbl_letter.master['background'] = clue
                lst_possible = find_possible(dct_clue, lst_possible)
                logger.warning(f"{lst_possible[:50]}")
                current_letter = 0
                current_guess += 1
                if the_guess == the_answer or current_guess == 6:
                    current_guess = 6
                    for col, letter in enumerate(the_answer):
                        dct_labels[(6, col)]['text'] = letter


if __name__ == "__main__":
    root.title("Wordle")
    # create_letters()
    current_guess = 0
    current_letter = 0
    lst_valid_answers, lst_valid_guesses = fetch_word_lists()
    lst_all_valid_guesses = lst_valid_answers + lst_valid_guesses
    the_answer = random.choice(lst_valid_answers)
    dct_clue = {}  # easy mode
    lst_possible = lst_all_valid_guesses  # easy mode

    tk.mainloop()
