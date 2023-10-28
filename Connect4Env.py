import numpy as np
import gymnasium as gym
from gymnasium import spaces

from Connect4Board import Board, pretty_board
from stable_baselines3 import PPO, A2C, DQN

class Connect4(gym.Env):

    metadata = {"render_modes": ["console"]}

    def __init__(self, rows = 6, columns = 7, player2 = 'random', render_mode="console"):
        super(Connect4, self).__init__()

        self.render_mode = render_mode
        self.board = Board(rows, columns)
        self.invalid_action_counts = 0

        self.player2 = player2 if player2 in ['random', 'human'] else A2C.load(player2)

        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(columns)
        self.observation_space = gym.spaces.Box(low=0, high=2, 
                                            shape=(rows, columns), dtype=np.float32)

        # Get first move
        if self.board.current_player == 2:
            if self.player2 == 'random':
                self.board.update_board(np.random.choice(list(range(self.board.columns))))
            elif self.player2 == 'human':
                self.board.current_player=1
            else:
                self.board.update_board(int(self.player2.predict(self.board.board, deterministic=True)[0]))

    def reset(self, seed=None, options=None):
        """
        Important: the observation must be a numpy array
        :return: (np.array)
        """
        super().reset(seed=seed, options=options)

        # Reset the board
        self.board.reset_board()
        self.invalid_action_counts = 0

        if self.board.current_player == 2:
            if self.player2 == 'random':
                self.board.update_board(np.random.choice(list(range(self.board.columns))))
            elif self.player2 == 'human':
                self.board.current_player=1
            else:
                self.board.update_board(int(self.player2.predict(self.board.board, deterministic=True)[0]))

        return self.board.board, {}  # empty info dict


    def step(self, action):
        col = action

        # check for valid action
        if col > self.board.columns:
            raise ValueError(
                f"Received invalid action={action} which is not part of the action space"
            )

        # check if action is valid (column full?)
        if not self.board.valid_column(col):
            self.invalid_action_counts += 1
            if self.invalid_action_counts > 5:
                return (self.board.board, -10000, False, True, {'Winner' : 'None'})
            return (self.board.board, -10000, False, False, {'Winner' : 'None'})

        self.board.update_board(col)

        if self.board.winning_move():
            return (self.board.board, 1000, True, False, {'Winner' : 'Model'})

        if self.board.full_Board():
            return (self.board.board, -1, False, False, {'Winner' : 'None'})
        
        if self.player2 == 'human':
            print(f"Model Action: {action}")
            self.render()

        ##########################
        # Player 2

        valid_actions = [col for col, value in enumerate(self.board.board[self.board.rows-1,:]) if value == 0]

        # Random player
        if self.player2=='random':
            player2_action = np.random.choice(valid_actions)

        # Human player
        elif self.player2 == 'human':
            player2_action = int(input(f"Choose an action out of {valid_actions}: "))
            while not self.board.valid_column(player2_action):
                player2_action = int(input(f"Choose an action out of {valid_actions}: "))

        # Pretrained model
        else:
            player2_action = int(self.player2.predict(self.board.converted_board(), deterministic=True)[0])
            for i in range(100): # check if the model is able to get a valid column
                if self.board.valid_column(player2_action):
                    break
                else:
                    player2_action = int(self.player2.predict(self.board.converted_board(), deterministic=False)[0])
            if not self.board.valid_column(player2_action):
                #raise ValueError("Model performed too many invalid actions!")
                print("Warning: Model 2 performed too many invalid actions!")
                player2_action = np.random.choice(valid_actions)

        # Perform Action
        self.board.update_board(player2_action)

        if self.board.winning_move():
            return (self.board.board, -100, True, False, {'Winner' : str(self.player2)})

        if self.board.full_Board():
            return (self.board.board, -1, False, False, {'Winner' : 'None'})
        
        if self.player2 == 'human':
            print(f"Player Action: {player2_action}")
            self.render()
        ##########################


        terminated = False # Game goes on
        truncated = False  # we do not limit the number of steps here
        reward = -1 # Null reward everywhere except game was terminated before
        info = {} # Optionally we can pass additional info, we are not using that for now

        return (self.board.board, reward, terminated, truncated, info)

    def render(self):
        pretty_board(self.board.board)