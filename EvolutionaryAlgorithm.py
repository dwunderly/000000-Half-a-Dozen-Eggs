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

class Generation:
    def __init__(self, size, inputs, outputs):
        self.size = size
        self.generation = []
        self.generationT = [None] * size
        self.best = None
        self.inputs = inputs
        self.outputs = outputs

    def beginGeneration():
        if(self.best == None):
            for i in range(self.size):
                self.generation.append(NN(self.inputs, self.outputs))
        else:
            for i in range(self.size):
                c = best.dup()
                c.mat += np.random.rand(c.inV, c.outV)
                generation[i] = c
            
    def step(self, state, index):
        f = self.generation[index].forward(np.array(state))
        i = np.argmax(f)
        return i
    
    def update(self, reward, index):
        self.generationT[index] = (reward, index)

    def endGeneration():
        self.generationT.sort()
        self.best = self.generation[self.generationT[-1][1]].dup()
        

generation = []
generationT = []
best = None

def initialize():
    global best
    

    for j in range(100):
        r = None
        while r == None:
            f = generation[j].forward(np.array(getState()))
            i = np.argmax(f)
            r = step(i)
        generationT.append((r, j))

    generationT.sort()
    best = generation[generationT[-1][1]].dup()

def getState():
    pass

def step(actIndex):
    pass

def newGeneration():
    global best
    for i in range(100):
        c = best.dup()
        c.mat += np.random.rand(c.inV, c.outV)
        generation[i] = c

    for j in range(100):
        r = None
        while r == None:
            f = generation[j].forward(np.array(getState()))
            i = np.argmax(f)
            r = step(i)
        generationT[j] = (r, j)

    generationT.sort()
    best = generation[generationT[-1][1]].dup()
    
