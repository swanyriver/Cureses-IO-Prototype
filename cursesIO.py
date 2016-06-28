# Proof of concept test for curses based input and output on flip server

import curses

# Macros for curses magic number functions
import sys

ON = 1
OFF = 0

QUIT_CHAR = ord('q')
#QUIT_CHAR = 27 #escape key

SCREEN_REFRESH = .25 # 4-FPS

def startCurses():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(ON)
    screen.nodelay(ON)
    return screen


def exitCurses(screen):
    curses.nocbreak();
    screen.keypad(OFF);
    screen.nodelay(OFF)
    curses.echo()
    curses.endwin()


def respondToInput(in_char_num, gameState):
    pass

def refreshScreen(screen, gameState):
    pass

def main():
    myScreen = startCurses()

    while True:
        # primary input and output loop
        char_in = myScreen.getch()
        if char_in == QUIT_CHAR:
            break
        if char_in != curses.ERR:
            sys.stderr.write("input: %r %s %r\n"%(char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}", curses.keyname(char_in)))

        respondToInput(char_in, None)
        refreshScreen(myScreen, None)

    exitCurses(myScreen)


if __name__ == '__main__':
    main()
