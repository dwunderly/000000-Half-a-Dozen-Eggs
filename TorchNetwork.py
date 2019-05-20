import torch
from torch.autograd import Variable
import Simulation

lev = Simulation.Level(Simulation.l)

dtype = torch.FloatTensor
N,D_in,H,D_out = 1, 25, 100, 8

w1 = Variable(torch.randn(D_in, H).type(dtype),requires_grad=True)
w2 = Variable(torch.randn(H, D_out).type(dtype), requires_grad=True)
firstTime = True

learning_rate = 1

def go():
    x = torch.tensor(lev.getVector()).view([1,D_in]).type(dtype)
    y_pred = x.mm(w1).sigmoid().mm(w2).sigmoid().softmax(1)
    values, indices = y_pred.max(1)
    
    rew = lev.Act(indices.item())
    if(rew > 0):
        y = [0] * D_out
        y[indices.item()] = 1.
        y = torch.tensor(y)
    else:
        y = [1] * D_out
        y[indices.item()] = 0.
        y = torch.tensor(y)
    
    loss = (y_pred - y).pow(2).sum()

    global firstTime
    if(not firstTime):
        w1.grad.data.zero_()
        w2.grad.data.zero_()
    else:
        firstTime = True
    
    loss.backward()
    w1.data -= learning_rate * w1.grad.data * abs(rew)
    w2.data -= learning_rate * w2.grad.data * abs(rew)
    print(rew)
    
    
    
    
    
    
