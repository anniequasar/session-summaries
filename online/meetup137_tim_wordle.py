#! /usr/bin/env python3
r"""MeetUp 137 - Beginners' Python and Machine Learning - 08 Mar 2022 - Wordle game

Learning objectives:
- how to write a wordle game in Python

Links:
- Colab:   https://colab.research.google.com/drive/1Kcm2XIUqEkY2g3-rUjFQZMPKuYx9ggSU
- Youtube: https://youtu.be/Llld1CeTutU
- Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/284430965
- Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings
"""

# Find what version of Python Google Colab is running
import sys
print(f"{sys.version=}")

# Check out the wordle game https://nytimes.com/games/wordle

# Challenge 1 - given an answer and a guess display which letters are in the right place
the_answer = "brace"
the_guess = "realm"

print(f"\nSolution 1 - letters in the right place answer={the_answer}, guess={the_guess}")
for i, answer_letter in enumerate(the_answer):
    print(i, the_guess[i], end=' ')
    if the_guess[i] == answer_letter:
        print("is the correct letter in the correct place")
    else:
        print("is not the correct letter for this place")
print()

# Challenge 2 - find which letters are correct but are in the wrong place. Assume no doubles

print(f"Solution 2 - using a function with local variables so as not to be confused with global variables "
      f"answer={the_answer}, guess={the_guess}")


def show_clues_no_doubles(answer, guess):
    for idx, local_letter in enumerate(guess):
        print(idx, local_letter, end=' ')
        if local_letter == answer[idx]:
            print("is the correct letter in the correct place")
        elif local_letter in answer:
            print("is the correct letter in the wrong place")
        else:
            print("is not the correct letter for this place")


show_clues_no_doubles(the_answer, the_guess)
print()

# How well does our solution cope with double letters
the_guess = "lulls"
the_answer = "sully"
print(f"How does solution 2 cope with double letters answer={the_answer}, guess={the_guess}")
show_clues_no_doubles(the_answer, the_guess)

# Doesn't work because first l in lulls is a wrong letter because all the ls have aready been guessed
# We also need to abbreviate our terminology 
# CORRECT = correct letter in the correct place
# MOVE = correct letter in the wrong place
# WRONG = incorrect letter

# Write a function show_clues which works for doubles
# Hint: Find all the CORRECTs first. Then evaluate for MOVEs


def show_clues(answer, guess):
    # convert str to list
    lst_answer = list(answer)
    # store all clues in list initialising them to empty str
    lst_clue = [''] * len(answer)
    for idx, local_letter in enumerate(guess):
        # First pass is to look for exact matches
        if local_letter == answer[idx]:
            lst_clue[idx] = 'CORRECT'
            # This was an exact match so remove from answer, so it doesn't trigger in second pass
            lst_answer[idx] = None
    for idx, local_letter in enumerate(guess):
        # Now we only need to look at letters which weren't exact matches in the first pass
        if lst_clue[idx] == '':
            if local_letter in lst_answer:
                lst_clue[idx] = 'MOVE'
                # This was a partial match so still remove from answer, so it doesn't trigger twice in second pass
                lst_answer.remove(local_letter)
            else:
                lst_clue[idx] = 'WRONG'
    for idx, local_letter in enumerate(guess):
        print(idx, local_letter, lst_clue[idx])


print(f"\nA better solution for double letters answer={the_answer}, guess={the_guess}")
show_clues(the_answer, the_guess)

# Challenge 3: Create a function clues() which returns list of clues
# Use constants for the three result strs
CORRECT = 'CORRECT'
MOVE = 'MOVE'
WRONG = 'WRONG'

print(f"\nSolution 3 = function returning clues. answer={the_answer}, guess={the_guess}")


def clues(answer, guess):
    # convert str to list
    lst_answer = list(answer)
    # store all clues in list initialising them to empty str
    lst_clue = [''] * len(answer)
    for idx, local_letter in enumerate(guess):
        # First pass is to look for exact matches
        if local_letter == answer[idx]:
            lst_clue[idx] = CORRECT
            # This was an exact match so remove from answer, so it doesn't trigger in second pass
            lst_answer[idx] = None
    for idx, local_letter in enumerate(guess):
        # Now we only need to look at letters which weren't exact matches in the first pass
        if lst_clue[idx] == '':
            if local_letter in lst_answer:
                lst_clue[idx] = MOVE
                # This was a partial match so still remove from answer, so it doesn't trigger twice in second pass
                lst_answer.remove(local_letter)
            else:
                lst_clue[idx] = WRONG
    return lst_clue


the_clues = clues(the_answer, the_guess)
for i, letter in enumerate(the_guess):
    print(i, letter, the_clues[i])
print()

# Challenge 4: Use the following terminal colour codes to display the matching letters in colour and bold
# When finished with a colour need to reset it back to normal text. 
CORRECT = '\033[1m\033[92m'
MOVE = '\033[1m\033[35m'
WRONG = ''
RESET = '\033[0m'
the_answer = 'gives'
the_guess = 'guess'
# \033 is the esc character in octal. Here it is in decimal, hexadecimal, octal
print(f"chr(27) '\\x1b'  '\\033'")
print(repr(chr(27)), repr('\x1b'), repr('\033'), sep='  ')

print(f"\nSolution 4: colour clues answer={the_answer}, guess={the_guess}")


def colour_clues(answer, guess):
    lst = []
    for local_letter, clue in zip(guess, clues(answer, guess)):
        lst.append(f"{clue}{local_letter}{RESET}")
    return "".join(lst)


print(colour_clues(the_answer, the_guess))

# Challenge 5: Use the input(prompt) function to read a guess from the user and display result

print(f"\nSolution 5: read guess from stdin answer={the_answer}, guess={the_guess}")
the_guess = input("Your guess: ")
print(f"            {colour_clues(the_answer, the_guess)}")

# Challenge 6: Keep reading user input until they guess the answer

print(f"\nSolution 6: keep reading user input until guess the answer answer={the_answer}, guess={the_guess}")
num = 0
the_guess = None
while num < 6 and the_guess != the_answer:
    num += 1
    the_guess = input(f"Your guess {num}: ")
    print(f"              {colour_clues(the_answer, the_guess)}")

# Next month's challenge - restrict guesses to actual five-letter words rather than a random selection of letters
# Uses a feature of Python 3.8, walrus operator.

"""# Installing Python
Next week's session will be running Python on your computer so let's look at how to install it. 

- Python from https://python.org - includes standard libraries and IDLE
- Anaconda from https://anaconda.com - includes Python and data science libraries and Spyder

Other Integrated Development Environments (IDEs)

- PyCharm Community Edition - free from https://jetbrains.com/pycharm
- Visual Studio Code - free from https://code.visualstudio.com/
"""