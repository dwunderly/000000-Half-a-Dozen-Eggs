l = ["1111111",
     "0000001",
     "0111111",
     "0001000",
     "0111111",
     "0100001",
     "111X111"]

class Level:
    
    ViewWidth = 5
    ViewHeight = 5
    
    def __init__(self, stringArray):
        self.initialPos = None
        self.playerPos = None
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
        for y in range(self.playerPos[1] - Level.ViewHeight//2-1,
                       self.playerPos[1] + Level.ViewHeight//2):
            for x in range(self.playerPos[0] - Level.ViewWidth//2-1,
                           self.playerPos[0] + Level.ViewWidth//2):
                print(x,y)
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
        Level.Actions[index](self)
        if(self.getBlock(self.playerPos[0],self.playerPos[1]) == 0):
            self.Reset()
            return -100
        return 1
            

    def Reset(self):
        self.playerPos = list(self.initialPos)

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
