import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions import Categorical
import torchvision
import torchvision.transforms as transforms
import numpy as np

# Hyperparameters
agent_view = 5*5*3
agent_choices = 8
learning_rate = 0.001
gamma = 0.99
hidden_size = 128
dropout_prob = 0.3

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.state_space = agent_view # Input vector
        self.action_space = agent_choices # Number of choices
        
        # Neural Net architecture
        self.l1 = nn.Linear(self.state_space, hidden_size, bias=True)
        self.l2 = nn.Linear(hidden_size, hidden_size, bias=True)
        self.l3 = nn.Linear(hidden_size, self.action_space, bias=False)
        
        self.gamma = gamma
        
        # Episode policy and reward history
        self.policy_history = Variable(torch.Tensor())
        self.reward_episode = []
        # Overall reward and loss history
        self.reward_history = []
        self.loss_history = []
    
    def forward(self, x):
        model = torch.nn.Sequential(
            self.l1,
            nn.Dropout(p=dropout_prob),
            nn.SELU(),
            self.l2,
            nn.Dropout(p=dropout_prob),
            nn.SELU(),
            self.l3,
            nn.Softmax(dim=-1)
        )
        return model(x)

policy = Policy()
optimizer = optim.Adam(policy.parameters(), lr=learning_rate)

# Implement select_action here
def select_action(state):
    state = torch.from_numpy(state).type(torch.FloatTensor)
    choices = policy(Variable(state))
    c = Categorical(choices)
    
    action = c.sample()

        
    if policy.policy_history.nelement() == 0:
        policy.policy_history = torch.stack([c.log_prob(action)])
    else:
        policy.policy_history = torch.cat([policy.policy_history, torch.stack([c.log_prob(action)])])
    
    '''
    if policy.policy_history.size()[0] > 1:
        policy.policy_history = torch.cat([policy.policy_history, c.log_prob(action)])
    elif policy.policy_history.nelement() != 0:
        policy.policy_history = torch.stack([policy.policy_history, c.log_prob(action)])
    else:
        policy.policy_history = (c.log_prob(action))
    '''
    return action

# We apply Monte-Carlo Policy Gradient to improve out policy according
# to the equation
def update_policy():
    
    R = 0
    rewards = []

    # Discount future rewards back to the present using gamma
    for r in policy.reward_episode[::-1]:
        R = r + policy.gamma * R
        rewards.insert(0,R)

    # Scale rewards
    rewards = torch.FloatTensor(rewards)
    rewards = (rewards - rewards.mean()) / (rewards.std() + np.finfo(np.float64).eps)

    # Calculate loss
    loss = (torch.sum(torch.mul(policy.policy_history, Variable(rewards)).mul(-1), -1))

    # Update network weights
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    policy.loss_history.append(loss.data.item())
    
    #Save and intialize episode history counter
    policy.reward_history.append(np.sum(policy.reward_episode))
    policy.policy_history = Variable(torch.Tensor())
    policy.reward_episode = []

def rfunc0(x,steps,done):
    reward = 0
    if done:
        if(x <= 0):
            reward = 1000
        else:
            reward = -1000
    else:
        reward = 1/(x+2)
    #reward -= steps/4
    return reward


def rfunc1(x,steps,done):
    reward = 20 - (x*3)
    if done:
        if(x <= 0):
            reward += 40 - steps
        else:
            reward -= 40 + steps
    #reward -= steps/4
    return reward

def rfunc2(x,steps,done):
    return 1/(x+2)

def rfunc3(x, steps, done):
    return random.random()

def rfunc4(x, steps, done):
    return 5-x

GridDict = {0: (1.,0.,0.),
            1: (0.,1.,0.),
            2: (0.,0.,1.)}

class PolicyLearner:
    def __init__(self, rFunc):
        self.rFunc = rFunc

    def step(self, floorGrid):
        state = []
        for b in floorGrid:
            state += GridDict[b]
        return select_action(np.asarray(state))
    
    def update(self, x, step, done):
        reward = self.rFunc(x,steps,done)
        policy.reward_episode.append(reward)

    def learn(self):
        update_policy()

'''
def main(episodes):
    for episode in range(episodes):
        done = False     
        level.Reset()
        stps = []
        while not done:
            state = np.asarray(level.getVector())
            action = select_action(state)
            x,steps,done = level.Act(action.item())
            reward = rfunc0(x,steps,done)
            stps += [ActDictionary[action.item()]]
            policy.reward_episode.append(reward)
            if x <= 0:
                print("Reached the end!", end=" ")
            if done:
                break 
        update_policy()
        print("Episode Done!")
        print(stps)
'''
