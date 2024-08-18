

#https://sparkbyexamples.com/python/print-colored-text-to-the-terminal-in-python/#:~:text=ANSI%20Escape%20Sequences%20to%20Add%20Color%20to%20Terminal%20Output&text=The%20escape%20sequence%20for%20setting,followed%20by%20the%20letter%20m%20.
'''
30 – Black
31 – Red
32 – Green
33 – Yellow
34 – Blue
35 – Magenta
36 – Cyan
37 – White
'''


print("\033[31mRed text\033[0m")
print("\033[32mGreen text\033[0m")
print("\033[1mBold text\033[0m")
print("\033[4mUnderlined text\033[0m")


# Import termcolor module
from termcolor import colored as tc
 
# termcolor example
print(tc("Red text on white background %i"%3, "red", "on_white"))
print(tc("Green bold text", "green", attrs=["bold"]))
print(tc("Yellow underlined text", "yellow", attrs=["underline"]))