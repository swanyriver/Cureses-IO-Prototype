import random

SPAWN_MIN = 2
SPAWN_MAX = 15

class Character():
    def __init__(self, y, x):
        self.x = x
        self.y = y


class Speck():
    def __init__(self, ymax, xmax):

        self.ymax = ymax
        self.xmax = xmax

        self.xdelta = random.randint(-4,4)
        self.ydelta = random.randint(-4,4)

        if random.choice((True, False)):
            # put on side walls
            self.x = 0 if self.xdelta > 0 else xmax
            self.y = random.randint(0, ymax)
        else:
            self.y = 0 if self.ydelta > 0 else ymax
            self.x = random.randint(0, xmax)

        self.inbounds = True

    def move(self):
        self.x += self.xdelta
        self.y += self.ydelta
        self.inbounds = 0 <= self.x <= self.xmax and 0 <= self.y <= self.ymax


class Game():
    def __init__(self, height, width):
        self.character = Character(height // 2, width // 2)
        self.maxX = width

        # this is a hack for now, to solve a problem with curses difficulty writing a character in the very bottom right
        # http://stackoverflow.com/questions/36387625/curses-calling-addch-on-the-bottom-right-corner
        self.maxY = height - 1
        self.noise = []
        self.nextNoiseTick = 0

    def getCharPos(self):
        return self.character.y, self.character.x

    #this is a request from the controller, not an imitative, game model will determine if move is possible
    def moveCharecter(self, ydelta, xdelta):
        if 0 <= self.character.x + xdelta < self.maxX:
            self.character.x += xdelta
        if 0 <= self.character.y + ydelta < self.maxY:
            self.character.y += ydelta

    def tick(self):
        for speck in self.noise:
            speck.move()
        self.noise = [sp for sp in self.noise if sp.inbounds]

        if self.nextNoiseTick <= 0:
            self.nextNoiseTick = random.randint(SPAWN_MIN, SPAWN_MAX)
            self.noise.append(Speck(self.maxY-1, self.maxX-1))

        self.nextNoiseTick -= 1

    def getNoise(self):
        return [(sp.y, sp.x) for sp in self.noise]
