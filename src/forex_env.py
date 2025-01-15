import gym
from gym import spaces
import numpy as np

class ForexTradingEnv(gym.Env):
    def __init__(self, data, window_size):
        super(ForexTradingEnv, self).__init__()
        self.data = data
        self.window_size = window_size
        self.current_step = self.window_size

        # Define action space: 0 = Buy, 1 = Hold, 2 = Sell
        self.action_space = spaces.Discrete(3)
        # Observation space: (window_size, number of features in data)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.window_size, self.data.shape[1]), dtype=np.float64
        )

        self.trade_history = []

    def reset(self):
        self.current_step = self.window_size
        self.trade_history = []
        return self._get_observation()

    def step(self, action):
        # Ensure we don't exceed the data length
        if self.current_step >= len(self.data):
            return self._get_observation(), 0, True, {}

        self.current_step += 1
        done = self.current_step >= len(self.data)

        # Get previous and current close prices
        prev_price = self.data.iloc[self.current_step - 1]["close"]
        current_price = self.data.iloc[self.current_step]["close"]

        # Reward logic based on action (buy, hold, sell)
        if action == 0:  # Buy
            reward = current_price - prev_price  # Positive reward if price increases after buying
        elif action == 2:  # Sell
            reward = prev_price - current_price  # Positive reward if price decreases after selling
        else:  # Hold
            reward = 0  # No reward for holding, unless you have specific conditions

        # Store trade history (step, price, reward, action)
        self.trade_history.append((self.current_step, current_price, reward, action))

        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        # Get the last `window_size` steps of data
        start = max(0, self.current_step - self.window_size)
        obs = self.data.iloc[start:self.current_step].to_numpy()

        # If data is less than window size, pad with zeros
        if obs.shape[0] < self.window_size:
            padding = np.zeros((self.window_size - obs.shape[0], self.data.shape[1]))
            obs = np.vstack((padding, obs))

        return obs












































