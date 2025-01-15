import torch
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from src.forex_env import ForexTradingEnv  # Import the environment

# Check if CUDA (GPU) is available and set the device accordingly
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load your dataset
data_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/forex_data.csv'  # Adjust the path if needed
data = pd.read_csv(data_path)

window_size = 24  # Adjust the window size as per your requirement

# Create the Forex environment
env = ForexTradingEnv(data, window_size)
env = DummyVecEnv([lambda: env])  # Stable-Baselines expects a vectorized environment

# Initialize the PPO model with the device (GPU or CPU)
model = PPO("MlpPolicy", env, verbose=1, device=device)

# Train the model
model.learn(total_timesteps=100000)

# Save the trained model
model.save("ppo_forex_model")

print("Model trained and saved successfully.")





