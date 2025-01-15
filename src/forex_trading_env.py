import gym
import numpy as np
from gym import spaces

class ForexTradingEnv(gym.Env):
    def __init__(self, data, window_size=10):
        super(ForexTradingEnv, self).__init__()
        self.data = data
        self.window_size = window_size
        self.current_step = 0

        # Observation space includes the new EMA indicators
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(self.window_size, len(self.data.columns)),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(3)  # Buy, Hold, Sell

    def reset(self):
        self.current_step = self.window_size
        return self._next_observation()

    def step(self, action):
        self.current_step += 1
        reward = 0  # Placeholder for reward logic
        done = self.current_step >= len(self.data) - 1
        obs = self._next_observation()
        return obs, reward, done, {}

    def _next_observation(self):
        return self.data.iloc[self.current_step - self.window_size:self.current_step].values























