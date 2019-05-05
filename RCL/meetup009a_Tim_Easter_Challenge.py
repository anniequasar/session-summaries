'''
MeetUp 009a - Beginners Python Support Sessions 1-May-2019

Learning objectives:
    Computational thinking
    Python: def, for, if, integer arithmetic, "{}".format


@author D Tim Cummings

Challenge is to calculate date of easter for every year since 1583

Ref: https://en.wikipedia.org/wiki/Computus

Check years 1981 2019 2049

'''

def easter_gauss(year):
    a = year % 19
    b = year % 4
    c = year % 7
    k = year // 100
    p = (13 + 8 * k) // 25
    q = k // 4
    M = (15 - p + k - q) % 30
    N = (4 + k - q) % 7
    d = (19 * a + M) % 30
    e = (2 * b + 4 * c + 6 * d + N) % 7
    day = d + e + 22
    if day < 32:
        month = "March"
    else:
        month = "April"
        day -= 31
    if d == 29 and e == 6:
        print("Year={}, d={}, e={}".format(year, d, e))
        day = 19
    if d == 28 and e == 6 and (11 * M + 11) % 30 < 19:
        print("Year={}, d={}, e={}, (11M + 11)%30={}".format(year, d, e, (11 * M + 11) % 30))
        day = 18
    return year, month, day


def easter_ian_taylor(year):
    a = year % 19
    b = year >> 2
    c = b // 25 + 1
    d = (c * 3) >> 2
    e = ((a * 19) - ((c * 8 + 5) // 25) + d + 15) % 30
    e += (29578 - a - e * 32) >> 10
    e -= ((year % 7) + b - d + e + 2) % 7
    d = e >> 5
    day = e - d * 31
    month = d + 3
    return year, month, day


for y in range(1583, 2500):
    eg = easter_gauss(y)
    ei = easter_ian_taylor(y)
    if eg[2] != ei[2]:
        print(eg, ei)
    print("Year {0:>4d}  Easter {1[2]:>2d} {1[1]:<4s}".format(y, eg))
