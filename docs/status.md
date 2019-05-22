---
layout: default
title: Status
---

<iframe width="560" height="315" src="https://www.youtube.com/embed/cmZiq2iNe1g" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Project Summary:
The agent is will attempt to navigate towards a known goal in a 2D platforming environment. The agent will be “nearsighted” and take in a 5x5 grid of our immediate surroundings as its input. It will then try to predict the best course of action from the following set of actions: walk one space up, down, left, or right; or jump two spaces up, down, left, or right. For every action it takes it will get a reward based on whether it made it to the goal, its distance to the goal, and number of steps it has taken. 

Approach:
The A.I. currently trains with a genetic algorithm that uses evolutionary learning to run several neural networks against the maze. It then chooses the top x networks sorted on a reward function  for the next generation. The program sorts on the following parameters with descending priority: whether it reached the goal, its distance to the goal, and total number of steps it has taken for the current run. Then it performs mutations on each one to add randomness and to avoid falling into local minima. It repeats this cycle for a 1000 iterations so that even if it were to find a solution in that time, it would also potentially be able to look for more optimal solutions. 
In order to speed up training time and test the efficacy of our approach, we created a discrete simulation of the Minecraft world the agent will be operating in. In our simulation, the world is a 2D vector of 1s and 0s, and our simulation allows us to grab a vector that represents the 5x5 state that the agent sees. This simulation allows us to manually perform any action from our action set. It also updates the world based on what action we forced the agent to do. It will also allow us to manually reset the world but it also automatically resets after the agent “dies.” 

Evaluation:
<img src="Evaluation Graph.png"></img>


Remaining Goals and Challenges:
	Our prototype has some success in a discrete environment, but the final agent needs to be able to operate in a continuous environment. 

Continuous vs discrete (zombies and random event platforms)
Tripwires
Level generation
Using a policy learning function and comparing it against our evolutionary learning algorithm
Moving platforms 
MALMO IS A PEACE OF SHIT

Resources Used:
We used NumPy, PyTorch, Matplotlib, and Malmo documentation to help build our prototype. 


