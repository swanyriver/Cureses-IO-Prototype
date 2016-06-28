class Character():
    def __init__(self, y, x):
        self.x = x
        self.y = y


class Game():
    def __init__(self, height, width):
        self.character = Character(height // 2, width // 2)
        self.maxX = width
        self.maxY = height

    def getCharPos(self):
        return self.character.y, self.character.x

    #this is a request from the controller, not an imitative, game model will determine if move is possible
    def moveCharecter(self, ydelta, xdelta):
        if 0 <= self.character.x + xdelta <= self.maxX:
            self.character.x += xdelta
        if 0 <= self.character.y + ydelta <= self.maxY:
            self.character.y += ydelta
