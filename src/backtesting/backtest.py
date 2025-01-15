import pandas as pd
import torch
import numpy as np
from src.forex_env import ForexTradingEnv  # Import the environment
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv  # Correct import for DummyVecEnv
import matplotlib.pyplot as plt

# Paths
DATA_PATH = 'C:/Users/haida/PycharmProjects/ForexBot2/data/forex_data.csv'  # Adjust path if needed
OUTPUT_RESULTS = 'C:/Users/haida/PycharmProjects/ForexBot2/output/backtest_results.csv'
OUTPUT_EQUITY_CURVE = 'C:/Users/haida/PycharmProjects/ForexBot2/output/equity_curve.png'

# Load data
data = pd.read_csv(DATA_PATH)
window_size = 24  # Adjust based on your requirement

# Create the Forex environment
env = ForexTradingEnv(data, window_size)
env = DummyVecEnv([lambda: env])  # Stable-Baselines expects a vectorized environment

# Load the trained model
model = PPO.load("ppo_forex_model")

# Backtesting logic
total_reward = 0
equity_curve = []
state = env.reset()

for step in range(len(data) - window_size):  # Avoid IndexError
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
    action, _states = model.predict(state_tensor, deterministic=True)

    # Execute action
    state, reward, done, _ = env.step(action)

    total_reward += reward
    equity_curve.append(total_reward)

    if done:
        break

# Save backtest results
pd.DataFrame(equity_curve, columns=["Equity"]).to_csv(OUTPUT_RESULTS, index=False)

# Generate equity curve visualization
plt.plot(equity_curve)
plt.title("Equity Curve")
plt.xlabel("Time")
plt.ylabel("Equity")
plt.savefig(OUTPUT_EQUITY_CURVE)

print(f"Backtest results saved at {OUTPUT_RESULTS}")
print(f"Equity curve saved at {OUTPUT_EQUITY_CURVE}")



