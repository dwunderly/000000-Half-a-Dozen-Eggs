l = ["00011",
     "00011",
     "01011",
     "01111",
     "11011",
     "10000",
     "00100",
     "11011",
     "10111",
     "00X11"]

class Level:
    
    ViewWidth = 7
    ViewHeight = 7
    
    def __init__(self, stringArray):
        self.initialPos = None
        self.playerPos = None
        self.previousPos = None
        self.steps = 0
        self.map = []

        for y, string in enumerate(stringArray):
            self.map += [[]]
            for x, char in enumerate(string):
                if char == "0":
                    self.map[y] += [0]
                elif char == "1":
                    self.map[y] += [1]
                elif char == "X":
                    self.map[y] += [1]
                    self.playerPos = [x, y]
                    self.initialPos = (x, y)
                    self.previousPos = (x, y)
                else:
                    print("Error")

        if(self.playerPos == None):
            print("Error")

    def getBlock(self, X, Y):
        if(Y < 0 or Y >= len(self.map) or X < 0 or X >= len(self.map[Y])):
            return 0
        return self.map[Y][X]
    
    def getVector(self):
        ret = []
        for y in range(self.playerPos[1] - Level.ViewHeight//2,
                       self.playerPos[1] + Level.ViewHeight//2+1):
            for x in range(self.playerPos[0] - Level.ViewWidth//2,
                           self.playerPos[0] + Level.ViewWidth//2+1):
                ret += [self.getBlock(x, y)]
        return ret
    
    def moveUp(self):
        self.playerPos[1] -= 1
        
    def moveLeft(self):
        self.playerPos[0] -= 1

    def moveRight(self):
        self.playerPos[0] += 1

    def moveDown(self):
        self.playerPos[1] += 1

    def jumpUp(self):
        self.playerPos[1] -= 2

    def jumpLeft(self):
        self.playerPos[0] -= 2

    def jumpRight(self):
        self.playerPos[0] += 2

    def jumpDown(self):
        self.playerPos[1] += 2

    def Act(self, index):
        self.previousPos = tuple(self.playerPos)
        Level.Actions[index](self)
        self.steps += 1
        ret = None
        if(self.getBlock(self.playerPos[0], self.playerPos[1]) == 0 or self.steps >= 30):
            ret = (False, -self.previousPos[1], -self.steps)
            self.Reset()
        if(self.playerPos[1] == 0):
            ret = (True, -self.steps)
            self.Reset()
        return ret
    
    def Reset(self):
        self.playerPos = list(self.initialPos)
        self.steps = 0

    def __str__(self):
        s = ""
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if((x,y) == tuple(self.playerPos)):
                    s += "X"
                elif(char == 1):
                    s += "1"
                else:
                    s += "0"
            s += "\n"
        return s
        

    Actions = [moveUp,
               moveLeft,
               moveRight,
               moveDown,
               jumpUp,
               jumpLeft,
               jumpRight,
               jumpDown]
