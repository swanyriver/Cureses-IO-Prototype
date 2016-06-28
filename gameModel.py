class Character():
    def __init__(self, y, x):
        self.x = x
        self.y = y


class Game():
    def __init__(self, height, width):
        self.character = Character(height // 2, width // 2)
        self.maxX = width

        # this is a hack for now, to solve a problem with curses difficulty writing a character in the very bottom right
        # http://stackoverflow.com/questions/36387625/curses-calling-addch-on-the-bottom-right-corner
        self.maxY = height - 1

    def getCharPos(self):
        return self.character.y, self.character.x

    #this is a request from the controller, not an imitative, game model will determine if move is possible
    def moveCharecter(self, ydelta, xdelta):
        if 0 <= self.character.x + xdelta < self.maxX:
            self.character.x += xdelta
        if 0 <= self.character.y + ydelta < self.maxY:
            self.character.y += ydelta
