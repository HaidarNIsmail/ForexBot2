import pandas as pd
import numpy as np
from stable_baselines3 import PPO
from forex_trading_env import ForexTradingEnv
from mt5_integration import fetch_data
import MetaTrader5 as mt5

# Initialize MetaTrader5 connection
if not mt5.initialize():
    print("MetaTrader 5 initialization failed.")
    mt5.shutdown()
    raise SystemExit

# Fetch data
try:
    data = fetch_data('EURUSD', timeframe=mt5.TIMEFRAME_M1, n_bars=1000)
    print("Data fetched successfully. Columns:", data.columns)
except Exception as e:
    print(f"Error fetching data: {e}")
    mt5.shutdown()
    raise

# Shutdown MetaTrader5
mt5.shutdown()

# Preprocess data
if not isinstance(data, pd.DataFrame):
    data = pd.DataFrame(data)

# Drop the time column (timestamps) since it's non-numeric
if 'time' in data.columns:
    data = data.drop(columns=['time'])

# Ensure all data is numeric
data = data.select_dtypes(include=['float', 'int'])

# Debugging step: Verify column names
print("Processed data columns:", data.columns)

# Initialize the environment
env = ForexTradingEnv(data, window_size=10)

# Load the trained model
model = PPO.load("ppo_forex_model")

# Evaluate the model
obs = env.reset()
total_reward = 0
n_steps = 1000  # Set the number of steps for evaluation

for step in range(n_steps):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    total_reward += reward
    if done:
        print(f"Episode finished after {step + 1} steps.")
        break

print("Total reward after evaluation:", total_reward)

