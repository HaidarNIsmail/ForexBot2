import os
import pandas as pd
from stable_baselines3 import PPO
from src.forex_trading_env import ForexTradingEnv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up paths using environment variables
data_path = os.getenv("DATA_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/output/EURUSD_with_indicators.csv")
model_path = os.getenv("MODEL_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/models/ppo_forex_model.zip")

try:
    print("Loading data...")
    data = pd.read_csv(data_path)
    print("Data loaded successfully. Preview:")
    print(data.head())

    # Drop non-numeric columns if any
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    print("Dropped non-numeric columns. Columns now:")
    print(numeric_data.columns)

    # Ensure observation shape alignment
    if numeric_data.shape[1] < 24:
        print(f"Warning: Data has {numeric_data.shape[1]} features, padding to 24.")
        numeric_data = numeric_data.reindex(columns=range(24), fill_value=0)

    print("Initializing the ForexTrading environment...")
    env = ForexTradingEnv(data=numeric_data, window_size=10)
    print("Environment initialized successfully.")

    print("Loading the trained model...")
    model = PPO.load(model_path)
    print("Model loaded successfully.")

    print("Starting backtesting...")
    obs = env.reset()
    total_reward = 0

    while True:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        if done:
            print("Episode finished.")
            break

    print("Backtesting completed.")
    print(f"Total Reward: {total_reward}")

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")


























































