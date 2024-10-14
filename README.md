
![haccks animated logo](https://raw.githubusercontent.com/LucasParsy/haccks/refs/heads/master/gifs/title.gif)

# Hacker Animation Cool Console Kryptographic Sequencer (haccks)


#### Description 
a digital rain code password decrypting effect library for Python, useful to visually represent character by-character secrets retrieval attacks. For [example a binary search in a blind database injection](https://www.youtube.com/watch?v=za_9hrq-ZuA).

inspired by the "cryptographic sequencer" [from the Batman Arkham video games series](https://www.ign.com/wikis/batman-arkham-city/Cryptographic_Sequencer) and the phone number tracking effect 
[from the Matrix movie intro](https://youtu.be/GVYTd4dH0Uc?si=XRgM3BwYB5OejB3v&t=11)

#### Usage

##### basic example
```python
from haccks import Haccks

password = "T0psyKr33t!"

h = Haccks(len(password))

# guess 1 character by second
for i, c in enumerate(password):
    h.setCharacter(i, c)
    time.sleep(1)
```
![basic example](https://raw.githubusercontent.com/LucasParsy/haccks/refs/heads/master/gifs/basic.gif)

##### change colors and framerate
```python
from haccks import Haccks

h = Haccks(24, refreshDelay=1,
                    primaryColor="purple", secondaryColor="fuchsia")
h.setCharacter(0, 'A')
h.setCharacter(23, 'Z')
```
![custom colors example](https://raw.githubusercontent.com/LucasParsy/haccks/refs/heads/master/gifs/colorful.gif)

##### set a custom alphabet
```python
from haccks import Haccks

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
```
![custom colors example](https://raw.githubusercontent.com/LucasParsy/haccks/refs/heads/master/gifs/alpha.gif)

##### call a custom method at the animation end

```python
from haccks import Haccks

from blessed import Terminal

def myCustomEnding(term: Terminal):
    paddH = term.height // 2 - 2

    print(term.clear)
    print(term.move_yx(paddH, 0) + term.chocolate1 +
          term.center("It’s now safe to turn off"))
    print(term.move_yx(paddH+1, 0) + term.chocolate1 +
          term.center("your computer"))
    time.sleep(5)

h = Haccks(12, customEndingMethod=myCustomEnding)
...
```
![custom colors example](https://raw.githubusercontent.com/LucasParsy/haccks/refs/heads/master/gifs/custom_end.gif)

#### installation

it's on [pypi](https://pypi.org/project/haccks/) , so simple as 

```python
pip install haccks
```

#### Documentation

Please tell me if it's not clear <br>(it makes sense in my mind, but that's because i'm a genius :P)

```python

# constructor of effect. immediatly displays fullscreen on terminal.
# ex: you know you have a 7 chars long secret to guess that can only be hexadecimal chars:
#   Haccks(7, '0123456789abcdef')

h = Haccks(
    numChars: int,               # number of "cracking" characters to display
    alphabet: str = "",          # possible chars shown.
    refreshDelay: float = 0.01,  # sleep time between each refresh of the effect

    # check blessed.readthedocs.io/en/latest/colors.html for available colors
    primaryColor: str = "green",    # color of the found characters 
    secondaryColor: str = "normal", # color of all other characters

    customEndingMethod: Callable[[blessed.Terminal], None] = None # custom method called at end
)

# set a character as "decoded", won't change and will appear in PrimaryColor
# ex: you found with a certitude that the second char of your secret is 'c': 
#     h.setCharacter(1, 'c')

h.setCharacter(
    position: int   # index of the character
    character: str: # char to set
)

# remove possible characters from the alphabet of an index
# ex: you know that the third char of your secret cannot be 'Z': 
#     h.removeCharsFromAlphabet(2, 'Z')

h.removeCharsFromAlphabet(
    position: int,  # index of the character
    characters: str # chars to exclude from alphabet
)
```



#### features and todos

##### Done

- [x] some errors and automatic managements
    - removing alphabet characters will validate a character if there is only 1 char left.
    - if all characters are validated the ending is displayed
- [x] blazingly fast (printing characters one by one? *nobody* would try that...)
- [x] multiplatform (thanks to the [blessed](https://pypi.org/project/blessed/) library)

- [x] customisable (colors, custom ending)
- [x] stoppable (type `q` to quit)
- [x] window resize aware

##### TODO
- [ ] more customization?
    - non-fullscreen mode?
    - multiple secrets guesses?
- [ ] use `multiprocessing` instead of `threading` ? (very small performance gain)
- [ ] more? (pull requests are open)
