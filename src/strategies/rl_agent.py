import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import pandas as pd
import numpy as np

# Custom Trading Environment
class TradingEnv(gym.Env):
    def __init__(self, df):
        super(TradingEnv, self).__init__()
        self.df = df
        self.current_step = 0
        self.action_space = gym.spaces.Discrete(3)  # Buy, Sell, Hold
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(df.columns),), dtype=np.float32)

    def reset(self, seed=None, options=None):
        """
        Reset the environment to the initial state.
        """
        super().reset(seed=seed)
        self.current_step = 0
        return self._next_observation(), {}

    def step(self, action):
        reward = 0
        terminated = False
        truncated = False

        # Ensure we don't access out-of-bounds indices
        if self.current_step == 0:
            self.current_step += 1
            return self._next_observation(), reward, terminated, truncated, {}

        # Reward logic: Profit/Loss based on action
        if action == 1:  # Buy
            reward = max(0, self.df.iloc[self.current_step]['Close'] - self.df.iloc[self.current_step - 1]['Close'])
        elif action == 2:  # Sell
            reward = max(0, self.df.iloc[self.current_step - 1]['Close'] - self.df.iloc[self.current_step]['Close'])

        self.current_step += 1
        if self.current_step >= len(self.df) - 1:
            terminated = True

        return self._next_observation(), reward, terminated, truncated, {}

    def _next_observation(self):
        """
        Get the next observation from the data and normalize it.
        """
        obs = self.df.iloc[self.current_step].values
        obs = (obs - np.min(obs)) / (np.max(obs) - np.min(obs) + 1e-8)  # Normalize
        return obs

# Load data
data_path = "../../data/data_with_indicators.csv"
df = pd.read_csv(data_path)

# Columns to inspect and clean
columns_to_clean = [
    'Close', 'EMA_50', 'EMA_200', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram',
    'BB_High', 'BB_Low', 'BB_Middle', 'Ichimoku_Conversion', 'Ichimoku_Base',
    'Ichimoku_A', 'Chikou_Span', 'Stochastic_RSI'
]

# Clean data: Handle NaN values
df[columns_to_clean] = df[columns_to_clean].fillna(method='ffill').fillna(method='bfill')  # Forward and backward fill

# Ensure no NaN values remain
if df[columns_to_clean].isnull().values.any():
    raise ValueError("Dataset still contains NaN values after cleaning.")

# Select relevant columns for RL environment
df = df[['Close', 'EMA_50', 'EMA_200', 'RSI', 'MACD', 'ADX', 'Stochastic_RSI']]

# Create RL environment
env = DummyVecEnv([lambda: TradingEnv(df)])

# Train PPO agent
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save RL agent
model.save("../../models/rl_agent.zip")
print("RL agent saved to: ../../models/rl_agent.zip")











