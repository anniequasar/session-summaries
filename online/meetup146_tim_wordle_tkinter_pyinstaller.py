r"""MeetUp 146 - Beginners' Python and Machine Learning - 13 Jun 2022 - tkinter and wordle and pyinstaller

Youtube: https://youtu.be/q_TxhZxN-H0
Github:  https://github.com/timcu/session-summaries/raw/master/online/meetup146_tim_wordle_tkinter_pyinstaller.py
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/286518055/

Learning objectives
 - Cross platform tkinter
 - Creating a single file for distributing application

Reference:
    https://docs.python.org/3/library/tkinter.html
    https://docs.python.org/3/library/tk.html
    https://tkdocs.com/tutorial/
    https://pyinstaller.org/en/stable/index.html

@author D Tim Cummings

# Task 1 - install python 3 including tkinter on your computer
I have installed Python 3 from https://python.org
tkinter is included in the standard or anaconda python3 install on Mac and Windows

On debian based linux
sudo apt install python3-tk

On MacPorts python
sudo port install py310-tkinter

# Task 2 - Create and activate a virtual environment
# Set up project directory
mkdir bpaml146
cd bpaml146
# copy this file into project directory

# Create virtual environment
py -m venv venv-bpaml146                                # Windows
python3 -m venv venv-bpaml146                           # Mac or Linux
conda create --name venv-bpaml146 python=3.10           # Anaconda

# activate virtual environment
source venv-bpaml146/bin/activate               # Mac or Linux or Windows Bash
conda activate venv-bpaml146                    # Anaconda
venv-bpaml146\Scripts\activate.bat              # Windows command prompt
venv-bpaml146\Scripts\Activate.ps1              # Windows powershell

# powershell may need to have restrictions removed
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser

# Task 3 - import third party libraries into virtual environment
# Create a file requirements.txt
beautifulsoup4
lxml
pyinstaller

# install third party libraries
pip install -r requirements.txt

# Task 4 - fix cross-platform issues with our tkinter app setting background label colours on macOS
# Hints:
#   Theme aqua won't allow setting background colour on labels
#   Theme names listed in tkinter.ttk.Style().theme_names()
#   Get current theme name using tkinter.ttk.Style().theme_use()
#   Set current theme using tkinter.ttk.Style().theme_use(new_them_name)

# Task 5 - fix cross-platform issues with our tkinter app reading backspace and enter key on macOS
# Find alternative way of determining if backspace or enter key has been pressed.
# Hints:
#   Use dir(event) to find which attributes can be used
#   Log values of all attributes when a key has been pressed

# Task 6 - Fix cross platform issues with saving files for five letter guesses and answers
# macOS runs app in sandbox, different path each time. Can't write to cwd = /
# Hints:
#   https://pyinstaller.org/en/stable/runtime-information.html use sys._MEIPASS to find bundle_dir
#   https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
from pathlib import Path
bundle_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)
#
#
# Task 7 - use pyinstaller to create a single executable file for your platform
# pyinstaller --onefile --windowed meetup146_tim_wordle_tkinter_pyinstaller.py

"""
import json
import logging
import pathlib
import random
import re
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

import tkinter as tk
import tkinter.ttk as ttk

# uncomment following line to see debug logging
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# This code already provides first and last lines
root = tk.Tk()
# get link to style database
style = ttk.Style()


# Task 4 - fix cross-platform issues with our tkinter app setting background label colours on macOS
# Hints:
#   Theme aqua won't allow setting background colour on labels
#   Theme names listed in tkinter.ttk.Style().theme_names()
#   Get current theme name using tkinter.ttk.Style().theme_use()
#   Set current theme using tkinter.ttk.Style().theme_use(new_them_name)


def s4_theme():
    logger.debug(f"Available themes {style.theme_names()=}")
    logger.debug(f"Current theme {style.theme_use()=}")
    if style.theme_use() == 'aqua':
        if 'default' in style.theme_names():
            style.theme_use('default')
        else:
            for theme in style.theme_names():
                if theme != 'aqua':
                    style.theme_use(theme)
                    break
        logger.debug(f"New theme {style.theme_use()=}")


s4_theme()


def handle_keypress_for_letters_not_mac(event, dct_labels):
    """Event handler. Needs to change values of three global variables

    This function doesn't work on mac. Task 6 is to fix in handle_keypress_for_letters(event, dct_labels).
    This is a copy of handle_keypress_for_letters_not_mac(event, dct_labels) before you made changes
    """
    global current_guess, current_letter, lst_possible
    if len(event.char) < 1:
        # we can't use ord(event.char) if len(event.char) < 1
        return
    logger.debug(f"{event.char=}, {ord(event.char)=}, {current_guess=}, {current_letter=}")
    if ord(event.char) == 8:  # backspace key
        if current_letter > 0:
            current_letter -= 1
        # Reset all letters in case they are in error state (not a word)
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


# Task 5 - fix cross-platform issues with our tkinter app reading backspace and enter key on macOS
# Find alternative way of determining if backspace or enter key has been pressed.
# Hints:
#   Use dir(event) to find which attributes can be used
#   Log values of all attributes when a key has been pressed
#   Remove all uses of "ord(event.char)" and "event.char in '\r\n'" which don't work on mac


def handle_keypress_for_letters(event, dct_labels):
    """Event handler - Task 5 fix this function to work on mac

    For reference:
    before changes = handle_keypress_for_letters_not_mac
    sample solution = s5_handle_keypress_for_letters"""
    global current_guess, current_letter, lst_possible
    if len(event.char) < 1:
        # we can't use ord(event.char) if len(event.char) < 1
        return
    logger.debug(f"{event.char=}, {ord(event.char)=}, {current_guess=}, {current_letter=}")
    if ord(event.char) == 8:  # backspace key
        if current_letter > 0:
            current_letter -= 1
        # Reset all letters in case they are in error state (not a word)
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


def s5_handle_keypress_for_letters(event, dct_labels):
    """Solution 5 Event handler"""
    global current_guess, current_letter, lst_possible
    logger.debug(f"{current_guess=}, {current_letter=}")
    logger.debug(f"event public attributes and methods are {[a for a in dir(event) if not a.startswith('_')]}")
    logger.debug(f"{event.char=}, {event.keycode=}, {event.keysym=}, {event.keysym_num=}, {event.num=}")
    if event.keysym == 'BackSpace':  # backspace key
        if current_letter > 0:
            current_letter -= 1
        # Reset all letters in case they are in error state (not a word)
        for col in range(5):
            dct_labels[(current_guess, col)]['style'] = RESET
    if current_letter < 5 and current_guess < 6:
        lbl_current = dct_labels[(current_guess, current_letter)]
        if 'a' <= event.char <= 'z':
            lbl_current['text'] = event.char
            current_letter += 1
        elif event.keysym in ['BackSpace']:
            lbl_current['text'] = ''
    elif event.keysym in ['Return', 'KP_Enter']:
        # KP_Enter (keypad enter) key only available on posix os such as linux or mac
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


# Define constants (see meetup137)
URL = "https://nytimes.com/games/wordle/index.html"

# Task 6 - Fix cross platform issues with saving files for five letter guesses and answers
# macOS runs app in sandbox, different path each time. Can't write to cwd = /
# Hints:
#   https://pyinstaller.org/en/stable/runtime-information.html use sys._MEIPASS to find bundle_dir
# from pathlib import Path
# bundle_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)

bundle_dir = pathlib.Path(__file__).parent
logger.debug(f"{bundle_dir=}")
FIVE_LETTER_ANSWERS = bundle_dir / "five_letter_answers.txt"
FIVE_LETTER_GUESSES = bundle_dir / "five_letter_guesses.txt"
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
style.configure(ANSWER, borderwidth="0", relief=tk.NONE)
style.configure(CORRECT, background='green')
style.configure(MOVE, background='yellow')
style.configure(WRONG, background='white')
style.configure(RESET, background='light grey')


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
            lbl = ttk.Label(master=root, text='', style=RESET)
            if r == 6:
                lbl['style'] = ANSWER
            dct_labels[(r, c)] = lbl
            lbl.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

    def handle_keypress(event):
        """Nested function so dct_labels is in scope of this event handler"""
        handle_keypress_for_letters(event, dct_labels)

    root.bind("<Key>", handle_keypress)


if __name__ == "__main__":
    root.title("Wordle")
    create_letters()
    current_guess = 0
    current_letter = 0
    lst_valid_answers, lst_valid_guesses = fetch_word_lists()
    lst_all_valid_guesses = lst_valid_answers + lst_valid_guesses
    the_answer = random.choice(lst_valid_answers)
    dct_clue = {}  # easy mode
    lst_possible = lst_all_valid_guesses  # easy mode

    tk.mainloop()
