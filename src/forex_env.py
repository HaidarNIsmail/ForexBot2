import gym
from gym import spaces
import numpy as np

class ForexTradingEnv(gym.Env):
    def __init__(self, data, window_size):
        super(ForexTradingEnv, self).__init__()
        self.data = data
        self.window_size = window_size
        self.current_step = self.window_size

        # Update observation space to match padded data shape
        self.action_space = spaces.Discrete(3)  # Buy, Hold, Sell
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.window_size, self.data.shape[1]), dtype=np.float64
        )

        self.trade_history = []

    def reset(self):
        self.current_step = self.window_size
        self.trade_history = []
        return self._get_observation()

    def step(self, action):
        if self.current_step >= len(self.data):
            return self._get_observation(), 0, True, {}

        self.current_step += 1
        done = self.current_step >= len(self.data)

        if action == 0:  # Buy
            reward = self.data.iloc[self.current_step]["close"] - self.data.iloc[self.current_step - 1]["close"]
        elif action == 2:  # Sell
            reward = self.data.iloc[self.current_step - 1]["close"] - self.data.iloc[self.current_step]["close"]
        else:  # Hold
            reward = 0

        self.trade_history.append((self.current_step, self.data.iloc[self.current_step]["close"], reward, action))
        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        start = max(0, self.current_step - self.window_size)
        obs = self.data.iloc[start:self.current_step].to_numpy()

        if obs.shape[0] < self.window_size:
            padding = np.zeros((self.window_size - obs.shape[0], self.data.shape[1]))
            obs = np.vstack((padding, obs))

        return obs



































