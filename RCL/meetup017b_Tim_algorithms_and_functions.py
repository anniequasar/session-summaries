"""
MeetUp 017b - Beginners Python Support Sessions 25-Jun-2019

Learning objectives:
    Algorithms and functions including recursive functions

@author D Tim Cummings

Challenge 2: Develop an algorithm to calculate what coins and notes are required to give
someone the correct change.
Smallest coin is 5c so always round up.
Put algorithm in a function so it can be called from different places in program
Make algorithm generic enough that it can take different selections of coins/notes and still work
Test for $0.45, $17.93

Advanced Challenge 3: You are programming an ATM which delivers $20 and $50 notes.
Can your "change" algorithm be used to
deliver the correct combination of notes. If not, what changes are required.
Test for $110

Super Advanced Challenge 4: Will your ATM work for an obscure currency which only
has $23, $25, and $29 notes
Test for $77. Test for $78

"""

total_change_cents = 1793
last_digit = total_change_cents % 10
extra_change = 0
if 0 < last_digit < 5:
    extra_change = 5 - last_digit
elif last_digit > 5:
    extra_change = 10 - last_digit
remaining_change = total_change_cents + extra_change


if remaining_change >= 2000:
    num_twenty_dollar = remaining_change // 2000
    remaining_change = remaining_change % 2000
    print("{} twenty dollar notes leaving {} cents".format(num_twenty_dollar, remaining_change))

if remaining_change >= 1000:
    num_ten_dollar = remaining_change // 1000
    remaining_change %= 1000
    print("{} ten dollar notes leaving {} cents".format(num_ten_dollar, remaining_change))

if remaining_change >= 500:
    num_five_dollar = remaining_change // 500
    remaining_change %= 500
    print("{} five dollar notes leaving {} cents".format(num_five_dollar, remaining_change))

if remaining_change >= 200:
    num_two_dollar = remaining_change // 200
    remaining_change %= 200
    print("{} two dollar coins leaving {} cents".format(num_two_dollar, remaining_change))

if remaining_change >= 100:
    num_one_dollar = remaining_change // 100
    remaining_change %= 100
    print("{} one dollar coins leaving {} cents".format(num_one_dollar, remaining_change))

if remaining_change >= 50:
    num_fifty_cent = remaining_change // 50
    remaining_change %= 50
    print("{} fifty cent coins leaving {} cents".format(num_fifty_cent, remaining_change))

if remaining_change >= 20:
    num_twenty_cent = remaining_change // 20
    remaining_change = remaining_change % 20
    print("{} twenty cent coins leaving {} cents".format(num_twenty_cent, remaining_change))

if remaining_change >= 10:
    num_ten_cent = remaining_change // 10
    remaining_change %= 10
    print("{} ten cent coins leaving {} cents".format(num_ten_cent, remaining_change))

if remaining_change >= 5:
    num_five_cent = remaining_change // 5
    remaining_change %= 5
    print("{} five cent coins leaving {} cents".format(num_five_cent, remaining_change))


def calc_remaining_change(remaining_change, denomination):
    num_coin = 0
    if remaining_change >= denomination:
        num_coin = remaining_change // denomination
        remaining_change %= denomination
        print("{} x {} cents leaving {} cents".format(num_coin, denomination, remaining_change))
    return remaining_change, num_coin


remaining_change = (total_change_cents + 4) // 5 * 5  # round up to nearest 5c
remaining_change, count = calc_remaining_change(remaining_change, 2000)
remaining_change, count = calc_remaining_change(remaining_change, 1000)
remaining_change, count = calc_remaining_change(remaining_change, 500)
remaining_change, count = calc_remaining_change(remaining_change, 200)
remaining_change, count = calc_remaining_change(remaining_change, 100)
remaining_change, count = calc_remaining_change(remaining_change, 50)
remaining_change, count = calc_remaining_change(remaining_change, 20)
remaining_change, count = calc_remaining_change(remaining_change, 10)
remaining_change, count = calc_remaining_change(remaining_change, 5)








