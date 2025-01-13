import gym
from gym import spaces
import numpy as np
import pandas as pd

class ForexTradingEnv(gym.Env):
    def __init__(self, data, window_size=10):
        super(ForexTradingEnv, self).__init__()

        self.data = data
        self.window_size = window_size
        self.current_step = 0

        # Action space: Buy, Sell, or Hold (3 actions)
        self.action_space = spaces.Discrete(3)

        # Observation space: Price, volume, indicators for the window size
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(window_size, data.shape[1]), dtype=np.float32)

    def reset(self):
        self.current_step = self.window_size
        return self.data.iloc[self.current_step - self.window_size:self.current_step].values

    def step(self, action):
        current_price = self.data.iloc[self.current_step]['Close']
        self.current_step += 1

        # Action - Buy, Sell, or Hold
        if action == 0:  # Buy
            reward = self.data.iloc[self.current_step]['Close'] - current_price
        elif action == 1:  # Sell
            reward = current_price - self.data.iloc[self.current_step]['Close']
        else:  # Hold
            reward = 0

        done = self.current_step >= len(self.data) - 1
        next_state = self.data.iloc[self.current_step - self.window_size:self.current_step].values

        return next_state, reward, done, {}

    def render(self):
        pass  # Optionally print out the current state






