# Proof of concept test for curses based input and output on flip server

import curses
import sys
import time
from gameModel import Game

# Macros for curses magic number functions
ON = 1
OFF = 0

SCREEN_REFRESH = .25 # 4-FPS
SCREEN_REFRESH = .05

# sadly there is no Enum class or pattern in python 2.x so this class will need to be used with extreme caution
class ACTIONS():
    up = 1
    down = 2
    left = 3
    right = 4
    quit = 5

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
    ACTIONS.left:(0,-1),
    ACTIONS.right:(0,1),
    ACTIONS.up:(-1,0),
    ACTIONS.down:(1,0)
}


def log(str):
    sys.stderr.write(str)


def startCurses():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(ON)
    screen.nodelay(ON)
    curses.curs_set(OFF)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    return screen


def exitCurses(screen):
    curses.nocbreak();
    screen.keypad(OFF);
    screen.nodelay(OFF)
    curses.curs_set(ON)
    curses.echo()
    curses.endwin()


def respondToInput(in_char_num, gameState):
    action = control_scheme.get(in_char_num)
    if action:
        positionDelta = directional_change.get(action, (0, 0))
        log("Respond to input" + str(positionDelta) + "\n")

        gameState.moveCharecter(*positionDelta)
        log("character at: %s\n"%(str(gameState.getCharPos())))


def refreshScreen(screen, gameState):
    #log("Refreshing screen\n")
    screen.erase()
    gameState.tick()

    #TODO attempting to addch at the same position caused exception, set up try/catch or a predraw canvas array to handle overlap
    alreadyDrawn = set()

    y, x = gameState.getCharPos()
    #screen.addch(y, x, ord('@'), curses.color_pair(1))
    for line in gameState.getCharacterDrawing():
        screen.addstr(y, x, line, curses.color_pair(1))
        y += 1
    alreadyDrawn.add((y,x))

    #draw noise
    #log("screen tick,  noise: " + str(gameState.getNoise()) + "\n")
    for speck in gameState.getNoise():
        if speck in alreadyDrawn: continue
        y,x = speck
        #log("speck y:%d, x:%d  alreadydrawn:%s\n"%(y,x, str(alreadyDrawn)))
        screen.addch(y, x, ord('#'), curses.color_pair(2))
        alreadyDrawn.add(speck)




#input is captured constantly but screen refreshes on interval
# no-sleep version of process loop
# todo continuous input appears to increases frame rate, rectify?  suprising because refreshScreen should not be called on every processed input
def constantInputReadLoop(screen, game):
    log("constant input loop initiated\n")
    lastRefresh = time.time()
    while True:
        # primary input and output loop
        char_in = screen.getch()
        if control_scheme.get(char_in) == ACTIONS.quit:
            break
        if char_in != curses.ERR:
            log("input: %r %s %r\n" %
                             (char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}",
                              curses.keyname(char_in)))

        respondToInput(char_in, game)
        if time.time() - lastRefresh > SCREEN_REFRESH:
            lastRefresh = time.time()
            refreshScreen(myScreen, game)


# input is processed and screen is refreshed each 'tick'
#   if key inputs are not made to be one-press-one-action then there is a batching effect that leads to a delay between
#   lifting key and movement stopping
def sleepLoop(screen, game):
    log("SleepLoop initiated\n")
    while True:
        time.sleep(SCREEN_REFRESH)
        char_in = screen.getch()
        if control_scheme.get(char_in) == ACTIONS.quit:
            break
        if char_in != curses.ERR:
            log("input: %r %s %r\n" %
                             (char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}",
                              curses.keyname(char_in)))
        respondToInput(char_in, game)
        refreshScreen(myScreen, game)


# use halfdelay input method,  breaks for input but only for specified time in tenths of a second
# performs similarly to no-sleep loop, has the advantage of halting for input after all other computation is complete
# limited to 10FPS  # very noticeable frame stuttering
def halfdelayLoop(screen, game):
    log("HalfDelay loop initiated\n")
    curses.nocbreak()
    refreshinTenths = int(SCREEN_REFRESH // .1) if SCREEN_REFRESH >= .1 else 1
    log("Screen Refresh Rate: %d tenths of a second\n"%refreshinTenths)
    curses.halfdelay(refreshinTenths)
    while True:
        char_in = screen.getch()
        if control_scheme.get(char_in) == ACTIONS.quit:
            break
        if char_in != curses.ERR:
            log("input: %r %s %r\n" %
                             (char_in, chr(char_in) if 0 <= char_in < 256 else "{Non Ascii}",
                              curses.keyname(char_in)))
        respondToInput(char_in, game)
        refreshScreen(myScreen, game)


if __name__ == '__main__':
    myScreen = startCurses()

    myGame = Game(*myScreen.getmaxyx())

    if len(sys.argv) > 1 and str.isdigit(sys.argv[1]):
        selectedLoop = int(sys.argv[1])
    else:
        selectedLoop = None

    if selectedLoop == 1:
        constantInputReadLoop(myScreen, myGame)
    elif selectedLoop == 2:
        sleepLoop(myScreen, myGame)
    elif selectedLoop == 3:
        halfdelayLoop(myScreen, myGame)
    else:
        constantInputReadLoop(myScreen, myGame)

    exitCurses(myScreen)
