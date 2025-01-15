import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from forex_trading_env import ForexTradingEnv
from indicator_setup import calculate_indicators

# Load data
data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD.csv"
data = pd.read_csv(data_path)

# Add indicators
data = calculate_indicators(data)

# Drop non-numeric columns for training
data = data.select_dtypes(include=['float64', 'int64'])

# Create environment
env = DummyVecEnv([lambda: ForexTradingEnv(data, window_size=10)])

# Initialize model
model = PPO("MlpPolicy", env, verbose=1)

# Train model
model.learn(total_timesteps=500_000)

# Save model
model.save("C:/Users/haida/PycharmProjects/ForexBot2/models/ppo_forex_model")





























