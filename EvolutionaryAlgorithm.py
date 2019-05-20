import numpy as np
import Simulation

class NN:
    def __init__(self, inV, outV):
        self.inV = inV
        self.outV = outV
        self.mat = np.random.rand(inV, outV)

    def forward(self, inV):
        return inV.dot(self.mat)
    
    def dup(self):
        copy = NN(self.inV, self.outV)
        copy.mat = np.copy(self.mat)
        return copy

lev = Simulation.Level(Simulation.l)
generation = []
generationT = []
best = None

def initialize():
    global best
    for i in range(100):
        generation.append(NN(25,8))

    for j in range(100):
        r = None
        while r == None:
            f = generation[j].forward(np.array(lev.getVector()))
            i = np.argmax(f)
            r = lev.Act(i)
        generationT.append((r, j))

    generationT.sort()
    best = generation[generationT[-1][1]].dup()

def step():
    global best
    for i in range(100):
        c = best.dup()
        c.mat += np.random.rand(c.inV, c.outV)
        generation[i] = c

    for j in range(100):
        r = None
        while r == None:
            f = generation[j].forward(np.array(lev.getVector()))
            i = np.argmax(f)
            r = lev.Act(i)
        generationT[j] = (r, j)

    generationT.sort()
    best = generation[generationT[-1][1]].dup()
    
