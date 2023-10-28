# 2023_Opencampus_Connect4_w_RL

Course Project for the Reinforcement Learning Course at Opencampus Kiel 2023

This repository contains my project code for the opencampus.sh course "Reinforcement Learning". In this project I trained an RL-agent to learn a strategy for the game "Connect4". Essential libraries for RL-agents and Interaction with the environment in this project are **stable_baselines3** and **gymnasium**.

## Connect 4

Connect Four is a two-player strategy game played on a 6x7 grid. The objective of the game is to be the first player to form a line of four of your colored discs in a row, column, or diagonal on the grid.

### Rules

1. Game Setup:

   - The game board consists of a 6x7 grid, which can hold a maximum of 42 discs (6 rows and 7 columns).
   - Usually colored discs are used to play the game. For this implementation the characters 'X' and 'O' represent the discs of the player

2. Taking Turns:

   - Players take turns placing one of their discs into one of the seven columns.
   - The disc will fall to the lowest available empty space in the chosen column.
   - Players cannot place discs outside the grid or into a column that is already full.

3. Winning the Game:

   - The objective is to connect four of your discs in a row, either horizontally, vertically, or diagonally.
   - When a player successfully connects at least four of their discs in a row, the game ends.

4. Blocking Your Opponent:

   - Part of the strategy involves blocking your opponent from forming a winning line of four discs.

5. Draws:
   - If all 42 spaces on the board are filled, and no player has achieved a winning combination, the game is a draw or a tie.

## Relevance for Reinforcement Learning

Connect Four is a simple yet engaging game that involves both strategy and tactical thinking. Connect4 is a suitable example for training a Reinforcement Learning (RL) algorithm due to its clear objectives, finite state and action spaces, binary rewards, strategic depth, and incremental learning opportunities. It's easy to visualize and offers educational value for understanding RL concepts and algorithms.

## Modules

1. Connect4Board: This module contains the relevant code for a Board class to play Connect4. Initialization of the Board, as well as functions for updating its state and checking for a winner are implemented here.

2. Connect4Env: This module contains the Environment code for training an RL-agent. The initialization of the environment, as well as the logic behind step() and reset() are defined here. This includes the settings of different rewards given to the agent for performing certain actions.

## Further files

1. model_train.ipynb: A Jupyter notebook to train an RL-agent (PPO, A2O or DQN) to play Connect4. The trained model can be saved and used for a game against a human player.

2. Demo_play.py: Executing this file with a python interpreter allows you to conduct a demo-game against a trained RL-agent (\_requires an already trained model).

3. Player2.py **Work in Progress** This module is supposed to define a class for a second player, which can either be a _random_ player, a _human_ player or an already _trained model_.

## Notes

As of now, a random player is used to train the RL-agent. This causes the agent to learn a very simple winning strategy, which is to always drop its disc into the same column. This appears to be a good and plausible strategy for the agent, as it leads to a fast win of the game against a random player. The random player will only rarely block the agents column.

While effective against a random player this strategy is clearly limited. It lacks adaptability and strategic depth. To improve the RL-agent's performance and make it more competitive, a new training strategy must be developed.

One solution would be to implement a smarter computer player, that is able to block horizontal moves of the agent.

Another solution could be to let the agent play against himself (i.e. trained versions of the agent). One approach could be to iteratively train a new agent for a certain numer of steps, saving the model and then letting the agent continue training against the saved state of the model/agent. In the longterm, this may help the agent to learn and develop more sophisticated tactics, enhancing its overall gameplay.

## Issues

- DOES MODEL UNDERSTAND WHO HE IS PLAYING?!?
  --> check if the agent is able to infer which disc belongs to him, which is essential for him to make strategic meaningful moves!
