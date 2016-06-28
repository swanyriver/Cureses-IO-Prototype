# Proof of concept test for curses based input and output on flip server

import curses
import sys
import time

# Macros for curses magic number functions
ON = 1
OFF = 0

SCREEN_REFRESH = .25 # 4-FPS

# sadly there is no Enum class or pattern in python 2.x so this class will need to be used with extreme caution
class ACTIONS():
    up = 1
    down = 2
    left = 3
    right = 4
    quit = 5

# # TODO map inputs to action enums
# #inputEnum = ["up","down","left","right"]
#
# control_key_scheme = {
#     "up": curses.KEY_UP,
#     "down": curses.KEY_DOWN,
#     "left": curses.KEY_LEFT,
#     "right": curses.KEY_RIGHT,
#     "quit": 27 #escape key
# }
#
# ascii_key_scheme = {
#     "up": ord('w'),
#     "down": ord('s'),
#     "left": ord('a'),
#     "right": ord('d'),
#     "quit": ord('q')
# }

# int to int, mapping keyboard key to action enum
control_scheme = {
    curses.KEY_UP:ACTIONS.up,
    ord('w'):ACTIONS.up,
    curses.KEY_DOWN:ACTIONS.down,
    ord('s'):ACTIONS.down,
    curses.KEY_LEFT:ACTIONS.left,
    ord('a'):ACTIONS.left,
    curses.KEY_RIGHT:ACTIONS.right,
    ord('d'):ACTIONS.right,
    27:ACTIONS.quit, #escape key
    ord('q'):ACTIONS.quit
}

directional_change = {
    ACTIONS.left:(-1,0),
    ACTIONS.right:(1,0),
    ACTIONS.up:(0,-1),
    ACTIONS.down:(0,1)
}


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
    action = control_scheme.get(in_char_num)
    if action:
        positionDelta = directional_change.get(action, (0, 0))
        sys.stderr.write("Respond to input" + str(positionDelta) + "\n")


def refreshScreen(screen, gameState):
    sys.stderr.write("Refreshing screen\n")


#input is captured constantly but screen refreshes on interval
# no-sleep version of process loop
def constantInputReadLoop(screen, game):
    lastRefresh = time.time()
    while True:
        # primary input and output loop
        char_in = screen.getch()
        if control_scheme.get(char_in) == ACTIONS.quit:
            break
        if char_in != curses.ERR:
            sys.stderr.write("input: %r %s %r\n" %
                             (char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}",
                              curses.keyname(char_in)))

        respondToInput(char_in, None)
        if time.time() - lastRefresh > SCREEN_REFRESH:
            lastRefresh = time.time()
            refreshScreen(myScreen, None)


# input is processed and screen is refreshed each 'tick'
def sleepLoop(screen, game):
    while True:
        time.sleep(SCREEN_REFRESH)
        char_in = screen.getch()
        if control_scheme.get(char_in) == ACTIONS.quit:
            break
        if char_in != curses.ERR:
            sys.stderr.write("input: %r %s %r\n" %
                             (char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}",
                              curses.keyname(char_in)))
        respondToInput(char_in, game)
        refreshScreen(myScreen, game)


# use halfdelay input method,  breaks for input but only for specified time in tenths of a second
# performs similarly to no-sleep loop, has the advantage of halting for input after all other computation is complete
def halfdelayLoop(screen, game):
    sys.stderr.write("HalfDelay loop initiated")
    curses.nocbreak()
    refreshinTenths = int(SCREEN_REFRESH // .1)
    sys.stderr.write("Screen Refresh Rate: %d tenths of a second\n"%refreshinTenths)
    curses.halfdelay(refreshinTenths)
    while True:
        char_in = screen.getch()
        if control_scheme.get(char_in) == ACTIONS.quit:
            break
        if char_in != curses.ERR:
            sys.stderr.write("input: %r %s %r\n" %
                             (char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}",
                              curses.keyname(char_in)))
        respondToInput(char_in, game)
        refreshScreen(myScreen, game)


if __name__ == '__main__':
    myScreen = startCurses()

    #myScreen.getmaxyx()

    #constantInputReadLoop(myScreen, None)
    #sleepLoop(myScreen, None)
    halfdelayLoop(myScreen, None)
    exitCurses(myScreen)