import numpy as np
from stable_baselines3 import PPO, A2C, DQN


class RandomPlayer():

    def __init__(self):
        self.name = 'Random Player'

    def predict(self, valid_actions):
        return np.random.choice(valid_actions)


class HumanPlayer():

    def __init__(self):
        self.name = 'Human Player'

    def predict(self, valid_actions):
        action = int(input(f"Choose an action out of {valid_actions}: "))
        while action not in valid_actions:
            action = int(input(f"Choose an action out of {valid_actions}: "))
        return action


class TrainedModel():

    def __init__(self, model_path):
        pass



