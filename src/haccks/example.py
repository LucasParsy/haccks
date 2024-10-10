from src.haccks import Haccks

import time
import random
from blessed import Terminal
import string

def myCustomEnding(term: Terminal):
    paddH = term.height // 2 - 2

    print(term.clear)
    print(term.move_yx(paddH, 0) + term.chocolate1 +
          term.center("It’s now safe to turn off"))
    print(term.move_yx(paddH+1, 0) + term.chocolate1 +
          term.center("your computer"))
    time.sleep(5)


def basic():
    password = "T0psyKr33t!"

    h = Haccks(len(password))
    for i, c in enumerate(password):
        time.sleep(1)
        h.setCharacter(i, c)


def colorful():
    h = Haccks(24, refreshDelay=1,
                     primaryColor="purple", secondaryColor="fuchsia")
    h.setCharacter(0, 'A')
    h.setCharacter(23, 'Z')


def alpha():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&()*+<>?'
    e = Haccks(40, alphabet, refreshDelay=0.01,
                     primaryColor="yellow2", secondaryColor="aqua")


    # cool animation: guess one random potential character by millisecond 
    lal = [random.sample(list(alphabet), len(alphabet)) for _ in range(40)]
    while True:
        r = random.randint(0, len(lal)-1)
        if len(lal[r]) > 1:
            e.removeCharsFromAlphabet(r, lal[r].pop())
            time.sleep(0.001)

def custom():
    h = Haccks(12, customEndingMethod=myCustomEnding)

    # don't show this in example
    time.sleep(3)
    for i in range(12):
        h.setCharacter(i, 'Z')

def endingTitle(term):
    paddH = term.height // 2 - 2
    st = "Hacker Animation Cool Console Kryptographic Sequencer"


    time.sleep(0.1)
    print(term.clear)
    res = ""
    for c in st:
        res += term.greenyellow if c.isupper() else term.green
        res += c + ' '

    print(term.move_yx(paddH, 0) +
            term.bold + term.center(res))

    message = " hacking complete ".upper()
    posHackComplete = term.move_yx(paddH + 4, 0)
    coloredMessage = term.bold + \
        term.center(term.greenyellow_reverse(message))
    blankMessage = term.center(" " * len(message))

    for i in range(3):
        print(posHackComplete + blankMessage)
        time.sleep(0.6)  # blink
        print(posHackComplete + coloredMessage)
        time.sleep(0.6)
    time.sleep(10)


def title():
    st = "Hacker Animation Cool Console Kryptographic Sequencer"
    alphabet = string.ascii_letters + string.digits + ' '

    e = Haccks(len(st), alphabet, refreshDelay=0.01, customEndingMethod=endingTitle,
                     primaryColor="greenyellow", secondaryColor="green")

    lal = [random.sample(list(alphabet), len(alphabet)) for _ in range(len(st))]
    for i,c in enumerate(st):
        lal[i].remove(c)

    while True: # will hang forever
        r = random.randint(0, len(lal)-1)
        if len(lal[r]) > 0:
            e.removeCharsFromAlphabet(r, lal[r].pop())
            time.sleep(0.0005)



def main():
    print("""
1 : basic
2 : colorful
3 : alphabet
4 : custom ending
5 : everything together

which one do you want?
""")
    t = input("> ")
    if t == "1":
        basic()
    if t == "2":
        colorful()
    if t == "3":
        alpha()
    if t == "4":
        custom()
    if t == "5":
        title()
    else:
        print("I didn't understood :(")
main()
