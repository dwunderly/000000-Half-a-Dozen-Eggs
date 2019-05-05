---
layout: default
title: Proposal
---

## Summary of the Project
The agent is going to attempt to navigate a 3D platforming environment towards a known goal. The agent will have information on its immediate surroundings, and its distance to the goal. The agent will have a limited pool of actions which it can perform, such as strafe one block, walk one block forward, or jump two blocks forward.

## AI/ML Algorithms
The agent will be trained using reinforcement learning. The AI turns the state (the immediate 5x5 surrounding blocks) and represent this as a vector. This vector is transformed by a weight matrix into a smaller vector representing which action the agent should perform. If the action reduces the distance to the goal, the weights are increased representing "rewarding" this behaviour. If the action increases the distance or causes the agent to fall the weights are decreased. 

## Evaluation Plan
A score will be derived based on distance to the goal and time taken to get there.

## Prototype Goals
The first prototype will aim to navigate simple flat bridges with some holes. The agent will only be able to perceive the immediate 5x5 surroundings. And the agent will only be able to perform the following moves: walk 1 left/right/forward/backward, jump 2 forward.

## Future Goals
As the prototype is clearly very simple, a number of goals for the future have been created. Goals include changing the number of moves available to offer more degrees of freedom, increasing the field of vision, and creating more advanced and sparser environments. If the project is still too simple, we aim to transition to solving 3d platforming puzzles.
