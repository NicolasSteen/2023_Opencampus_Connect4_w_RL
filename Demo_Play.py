from Connect4Env import Connect4
from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.env_util import make_vec_env
import time
from Connect4Board import pretty_board

# Instantiate the env
vec_env = make_vec_env(Connect4, n_envs=1, env_kwargs={'player2':'human'})
#model_name = 'A2C_naive_stochastic_model.zip'
model_name = 'my_model.zip'

obs = vec_env.reset()
model = A2C.load(model_name)
while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)

    print("")
    if done: # Note that the VecEnv resets automatically when a done signal is encountered
        print(f"{info[0]['Winner']} wins!!!")
        pretty_board(info[0]['terminal_observation'])
        print("###############################\n")
        print("########## GAME OVER ##########\n")
        print("###############################\n")
        break
    time.sleep(1.2)