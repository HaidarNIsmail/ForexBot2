import gym
from stable_baselines3 import PPO
from forex_trading_env import ForexTradingEnv  # Ensure the correct import path for your environment
import pandas as pd

# Load data
data = pd.read_csv('C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv')

# Create the environment
env = ForexTradingEnv(data)

# Initialize PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_forex_model")

print("Model training completed and saved!")



