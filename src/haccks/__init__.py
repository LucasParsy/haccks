from blessed import Terminal
import random
import string
import time
import threading
from typing import Callable

# Terminal object

# Initializing the list of characters


class Haccks():
    term = Terminal()  # lets keep this one easily accessible

    __primaryColor = ""
    __secondaryColor = ""

    __numChars = 0
    __speed = 1
    __alphabet = ""
    __customEndingMethod = None

    __thread = None
    __lock = threading.RLock()
    __reversedColorMethod = None
    __numValidated = 0
    __validatedChars: dict[int] = {}
    __paddH = 0
    __paddL = 0

    def __init__(self, numChars: int, alphabet: str = "", refreshDelay: float = 0.01, primaryColor: str = "green", secondaryColor: str = "normal", customEndingMethod: Callable[[Terminal], None] = None):
        """create a cool password decyphering fullscreen CLI animation

        Args:
            numChars (int): number of "cracking" characters to display
            alphabet (str, optional): use a custom alphabet for the shown possible chars. Enables the fullscreen wall of characters. Defaults to "".
            refreshDelay (float, optional): sleep time between each refresh of the effect. Defaults to 0.01.
            primaryColor (str, optional): color of the found characters. Check https://blessed.readthedocs.io/en/latest/colors.html for available colors. Defaults to "green".
            secondaryColor (str, optional): color of every other characters. Defaults to "normal".
            customEndingMethod (Callable[[Terminal], None], optional): change method called once all charaters are decoded. Term object allows you to print custom effects. Defaults to None.
        """
        self.__primaryColor = self.__checkColor(primaryColor)
        self.__secondaryColor = self.__checkColor(secondaryColor)

        self.__reversedColorMethod = getattr(
            self.term, primaryColor+"_reverse")
        self.__numChars = numChars
        self.__speed = refreshDelay
        self.__alphabet = alphabet
        self.__customEndingMethod = customEndingMethod
        for i in range(numChars):
            self.__validatedChars[i] = {1: '', 2: list(alphabet)}

        self.__thread = threading.Thread(target=self.__run).start()

    def __checkColor(self, colorName: str) -> str:
        color = getattr(self.term, colorName)
        if not color:
            raise ValueError(
                f"{colorName} is not a real color, please check https://blessed.readthedocs.io/en/latest/colors.html for available colors")
        return color

    def __update_padding(self):
        """resize awareness"""

        tempH = self.term.height // 2 - 2
        tempL = self.term.width // 2 - (self.__numChars * 2) // 2
        if tempH != self.__paddH or tempL != self.__paddL:
            print(self.term.clear)
        self.__paddH = tempH
        self.__paddL = tempL

    def __run(self):
        """auto runned method at class instanciation"""
        with self.term.cbreak(), self.term.hidden_cursor(), self.term.fullscreen():
            while True:
                with self.__lock:
                    self.__update_padding()
                    self.__effectGen()
                    # Debug Quit
                    if self.term.inkey(timeout=0.1) == 'q':
                        return

                    if self.__numValidated >= self.__numChars:
                        if self.__customEndingMethod:
                            self.__customEndingMethod(self.term)
                        else:
                            self.__showCompleted()
                        print(self.term.clear)
                        return
                time.sleep(self.__speed)

    def __showCompleted(self):
        time.sleep(2)
        print(self.term.clear)
        res = "".join([self.__validatedChars.get(i)[1]
                      for i in range(self.__numChars)])
        print(self.term.move_yx(self.__paddH, 0) +
              self.term.bold + self.term.center(res))

        message = " hacking complete ".upper()
        posHackComplete = self.term.move_yx(self.__paddH + 4, 0)
        coloredMessage = self.term.bold + \
            self.term.center(self.__reversedColorMethod(message))
        blankMessage = self.term.center(" " * len(message))

        for i in range(3):
            print(posHackComplete + blankMessage)
            time.sleep(0.6)  # blink
            print(posHackComplete + coloredMessage)
            time.sleep(0.6)
        time.sleep(10)

    def __effectGen(self):
        if self.__alphabet:
            self.__effectAlphabet()
        else:
            self.__effectSimple()

    def __effectSimple(self):
        # difficult to move back inside the "effectAlphabet" loop without making it even more convoluted
        randChars = [random.choice(
            string.ascii_letters + string.digits + string.punctuation) for _ in range(self.__numChars)]
        line = self.term.move_yx(
            self.__paddH, self.__paddL) + self.__secondaryColor + self.term.bold
        for i in range(self.__numChars):
            c = self.__validatedChars.get(i)[1]
            if c:
                line += self.__primaryColor + self.term.bold + \
                    c + ' ' + self.__secondaryColor + self.term.bold
            else:
                line += randChars[i] + ' '
        print(line)

    def __effectAlphabet(self):
        height = self.term.height

        for e in self.__validatedChars.values():
            random.shuffle(e[2])

        for h in range(0, height - 2):
            isEmptyLine = True
            line = self.term.move_yx(h, self.__paddL) + self.__secondaryColor

            if h == self.__paddH:
                line += self.term.bold
                isEmptyLine = False

            for i in range(self.__numChars):
                if (self.__validatedChars[i][1] and h != self.__paddH) or len(self.__validatedChars[i][2]) < (abs(h - self.__paddH) * 2 + 1):
                    line += "  "
                elif h == self.__paddH and self.__validatedChars[i][1]:
                    line += self.__primaryColor + self.term.bold + \
                        self.__validatedChars[i][1] + ' ' + \
                        self.__secondaryColor + self.term.bold
                else:
                    line += self.__validatedChars[i][2][h - self.__paddH] + " "
                    isEmptyLine = False

            print(line)

    def setCharacter(self, position: int, character: str):
        """set a character as "decoded", won't change and will appear in PrimaryColor

        Args:
            position (int): index of the character
            character (str): specific char to set
        """

        if position < 0 or position >= self.__numChars:
            return
        with self.__lock:
            self.__numValidated += 1
            self.__validatedChars[position][1] = character

    def removeCharsFromAlphabet(self, position: int, characters: str):
        """reduce possible alphabet for a character

        Args:
            position (int): index of the character
            characters (str): chars to remove from alphabet
        """

        if position < 0 or position >= self.__numChars or not self.__alphabet:
            return
        with self.__lock:
            self.__validatedChars[position][2] = [
                i for i in self.__validatedChars[position][2] if i not in list(characters)]

            alpha = self.__validatedChars[position][2]
            if len(alpha) <= 1:
                # todo: better "error handling" than this, people would not understand
                # I just hope that people won't just erase their complete alphabet by mistake.
                nc = "¿" if len(alpha) == 0 else alpha[0]
                self.setCharacter(position, nc)
