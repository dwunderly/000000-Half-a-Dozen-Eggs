import numpy as np

def sig(x):
    return 1./(1.+np.exp(-x))

def lrelu(x):
    if(x < 0):
        return 0.01*x
    return x

class NN:
    def __init__(self, shape, active = sig):
        self.mats = []
        for i in range(len(shape)-1):
            self.mats.append(np.random.rand(shape[i], shape[i+1]))
        self.active = active
        self.shape = shape

    def forward(self, inV):
        for mat in self.mats:
            inV = inV.dot(mat)
            inV = np.array(list(map(self.active, inV)))
        return inV
    
    def dup(self):
        copy = NN(self.shape, self.active)
        for i in range(len(self.mats)):
            copy.mats[i] = np.copy(self.mats[i])
        return copy

class Generation:
    def __init__(self, size, shape, action = sig):
        self.size = size
        self.generation = []
        self.action = action
        self.shape = shape
        self.generationT = [None] * size
        self.best = None

    def beginGeneration(self):
        if(self.best == None):
            for i in range(self.size):
                self.generation.append(NN(self.shape, self.action))
        else:
            for j in range(self.size):
                if(j == self.size-1):
                    self.generation[j] = self.best
                    continue
                c = self.best.dup()
                for i in range(len(c.shape)-1):
                    c.mats[i] += np.random.rand(c.shape[i],c.shape[i+1])
                self.generation[j] = c
            
    def step(self, state, index):
        f = self.generation[index].forward(np.array(state))
        i = np.argmax(f)
        return i
    
    def update(self, reward, index):
        self.generationT[index] = (reward, index)

    def endGeneration(self):
        self.generationT.sort()
        self.best = self.generation[self.generationT[-1][1]].dup()

if __name__ == "__main__":
    import Simulation
    g = Generation(20,(25,8))
    l = Simulation.Level(Simulation.l)
    for i in range(1000):
        g.beginGeneration()
        for j in range(20):
            r = None
            while r == None:
                r = l.Act(g.step(l.getVector(),j))
            g.update(r, j)
        g.endGeneration()
