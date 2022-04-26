#! /usr/bin/env python3
r"""MeetUp 142 - Beginners' Python and Machine Learning - 12 Apr 2022 - Wordle game with word list

Learning objectives:
- how to scrape data from website and store in local file
- incorporate word list in wordle game from MeetUp 137

Links:
- Colab:   https://colab.research.google.com/drive/1kyJQDgQwzEUFIcj58Uvbm_OUCtsLg8Gb
- Youtube: https://youtu.be/arpGk_K5f_U
- Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/285029634/
- Github:  https://github.com/anniequasar/session-summaries/tree/master/online

- Meetup 074: https://colab.research.google.com/drive/1El9hOgXGbhwkOnBpv0WrFnSEBZxfTt4B (regular expressions)
- Meetup 133: https://colab.research.google.com/drive/1omqD-sGNnu9vq-PieZgTvNAEa1Kj6m7M (web scraping)
- Meetup 137: https://colab.research.google.com/drive/1Kcm2XIUqEkY2g3-rUjFQZMPKuYx9ggSU (wordle part 1)

@author D Tim Cummings
"""
# Import required libraries BeautifulSoup, urlopen, re, json
import json
import random
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Challenge 1 - Go to source code of wordle game and find javascript code containing the list of words
url = "https://nytimes.com/games/wordle/index.html"

# Solution 1 - script tag loading source from file
# <script src="main.3d28ac0c.js"></script>

# Challenge 2 - Install Beautifulsoup4 and lxml to be able to scrape web page for this script
# Hint - see Meetup 133

# Solution 2 - following are to be typed on command line without preceding #
# python3 -m venv bpaml142  # Create virtual environment
# source bpaml/bin/activate  # activate virtual environment (mac or linux)
# bpaml\Scripts\Activate  # activate virtual environment (windows)
# pip list  # use to check libraries are installed
# pip install beautifulsoup4 lxml  # Use to install if they are missing.

# Load the wordle game https://nytimes.com/games/wordle/index.html into a soup
with urlopen(url) as page:
    soup = BeautifulSoup(page, features="lxml")

# Find all the script tags
lst_script = soup.find_all("script")
for s in lst_script:
    print(s)

# Compare these scripts to Chrome devtools (F12)
# Apparently more scripts are added dynamically

# Challenge 3 - Use the find method to find a script tag with src attribute but no defer attribute
# hint kwargs to scan attributes "attribute name" = [True | False] for existence of attribute

# Solution 3
print("\nSolution 3")
script = soup.find("script", src=True, defer=False)
js_file = script["src"]
print(js_file)

# Challenge 4 - Construct an url for javascript file
# hint: rfind finds rightmost substring of string

# Solution 4
print("\nSolution 4")
idx_slash = url.rfind("/")
print(f"{url[:idx_slash+1]=}")
url_js = url[:idx_slash+1] + js_file
print(f"{url_js=}")

# urlopen can read the javascript file and the charset of the file
# using 'with' automatically closes resources when finished with them
with urlopen(url_js) as js_response:
    bytes_js = js_response.read()
    print(bytes_js[:80], "...")
    print(type(bytes_js))
    print(js_response.headers.get_content_charset())

# Challenge 5 - Convert the javascript into a str

# Solution 5
print("\nSolution 5")
str_js = bytes_js.decode(js_response.headers.get_content_charset())
print(f"{str_js[:80]=} ...")
print()

# Find word list within javascript code
# In javascript word list will be in a javascript array eg ["abode", "brake", "cater"] or ['abode', 'brake', 'cater']
# There will be more than 1000 words in the list
# We can use regular expressions to find them. Test your regex in https://regex101.com
ptn = re.compile(r"""(\[[a-z,"'\s]{5000,}])""")
lst_match = ptn.findall(str_js)
for m in lst_match:
    # don't want to give away any wordle answers for a particular day or show which answers have already been used so
    # sort them (after converting them to python list)
    lst = sorted(json.loads(m))
    print(len(lst), lst[:20], "...")

# save possible answers in file
FIVE_LETTER_ANSWERS = "five_letter_answers.txt"
lst_answers = sorted(json.loads(lst_match[0]))
with open(FIVE_LETTER_ANSWERS, "w") as file_answers:
    for w in lst_answers:
        file_answers.write(w + "\n")

# reading possible answers from file
with open(FIVE_LETTER_ANSWERS) as f:
    # readlines() reads each line including newline characters
    lst_raw = f.readlines()
print(len(lst_raw), lst_raw[:10])
lst_answers = [w.strip() for w in lst_raw]
print(len(lst_answers), lst_answers[:10])

# Challenge 6 - Save valid guesses to a file and read them back

# Solution 6 - Checking if file exists and fetching if it doesn't
print("\nSolution 6")
FIVE_LETTER_GUESSES = "five_letter_guesses.txt"
try:
    with open(FIVE_LETTER_GUESSES) as f:
        lst_guesses = [w.strip() for w in f]  # as convenience can iterate over file object one line at a time
    print("read guesses from file")
except FileNotFoundError:
    print("fetch guesses from web")
    with urlopen(url) as page:
        soup = BeautifulSoup(page, features="lxml")
    script = soup.find("script", src=True, defer=False)
    url_js = url[:url.rfind("/")+1] + script["src"]
    with urlopen(url_js) as js_response:
        str_js = js_response.read().decode(js_response.headers.get_content_charset())
    ptn = re.compile(r"""(\[[a-z,"'\s]{5000,}])""")
    lst_match = ptn.findall(str_js)
    lst_guesses = sorted(json.loads(lst_match[1]))
    with open(FIVE_LETTER_GUESSES, "w") as file_guesses:
        for w in lst_guesses:
            file_guesses.write(w + "\n")

# Last month's code can be consolidated
the_answer = "brace"
# Use the following terminal colour codes to display the matching letters in colour and bold
# When finished with a colour need to reset it back to normal text.
CORRECT = '\033[1m\033[92m'
MOVE = '\033[1m\033[35m'
WRONG = ''
RESET = '\033[0m'


def clues(answer, guess):
    # convert str to list
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


def colour_clues(answer, guess):
    lst_clue = []
    for letter, clue in zip(guess, clues(answer, guess)):
        lst_clue.append(f"{clue}{letter}{RESET}")
    return "".join(lst_clue)


num = 0
the_guess = None
while num < 6 and the_guess != the_answer:
    num += 1
    the_guess = input(f"Your guess {num}: ")
    print(f"              {colour_clues(the_answer, the_guess)}")

# Challenge 7 - Modify last month's code to choose a word from answers and check validity from valid guesses

# Solution 7
print("\nSolution 7")
lst_all_valid_guesses = lst_answers + lst_guesses


def find_possible(dct_clue_per_guess, lst_possible_prev):
    # for easy mode
    possible = lst_possible_prev
    for guess, lst_clue in dct_clue_per_guess.items():
        possible = [word for word in lst_possible_prev if clues(word, guess) == lst_clue]
    return possible


num = 0
the_answer = random.choice(lst_answers)
the_guess = None
dct_clue = {}  # easy mode
lst_possible = lst_all_valid_guesses  # easy mode
while num < 6 and the_guess != the_answer:
    num += 1
    the_guess = input(f"Your guess {num} : ")
    while the_guess not in lst_all_valid_guesses:
        print("Not a word")
        the_guess = input(f"Your guess {num} : ")
    print(f"               {colour_clues(the_answer, the_guess)}", end='')
    # easy mode
    dct_clue[the_guess] = clues(the_answer, the_guess)
    lst_possible = find_possible(dct_clue, lst_possible)
    print(f"       {len(lst_possible)} {lst_possible[:30]}")

print(f"Correct answer {the_answer}")
