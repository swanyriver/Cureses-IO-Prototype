# Proof of concept test for curses based input and output on flip server

import curses

# Macros for curses magic number functions
import sys

ON = 1
OFF = 0

#QUIT_CHAR = ord('q')
QUIT_CHAR = 27 #escape key

def startCurses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(ON)
    stdscr.nodelay(ON)
    return stdscr


def exitCurses(stdscr):
    curses.nocbreak();
    stdscr.keypad(OFF);
    stdscr.nodelay(OFF)
    curses.echo()
    curses.endwin()


def main():
    myScreen = startCurses()

    while True:
        # primary input and output loop
        char_in = myScreen.getch()
        if char_in == QUIT_CHAR:
            break
        if char_in != curses.ERR:
            sys.stderr.write("input: %r %s\n"%(char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}"))

    exitCurses(myScreen)


if __name__ == '__main__':
    main()
