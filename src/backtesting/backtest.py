import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from dotenv import load_dotenv

# Add the src directory to PYTHONPATH
sys.path.append("C:/Users/haida/PycharmProjects/ForexBot2/src")

# Import the ForexTradingEnv after ensuring PYTHONPATH is set
from forex_env import ForexTradingEnv

# Load environment variables from .env file
load_dotenv()

# Set up paths using environment variables
data_path = os.getenv("DATA_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/output/EURUSD_with_indicators.csv")
model_path = os.getenv("MODEL_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/models/ppo_forex_model.zip")
output_path = os.getenv("OUTPUT_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/output")

try:
    print("Loading data...")
    data = pd.read_csv(data_path)
    print("Data loaded successfully. Preview:")
    print(data.head())

    # Drop non-numeric columns if any
    data = data.select_dtypes(include=['float64', 'int64'])
    print("Dropped non-numeric columns. Columns now:")
    print(data.columns)

    # Handle NaN values
    print("Handling NaN values...")
    data.fillna(method='ffill', inplace=True)  # Forward-fill NaNs
    data.fillna(method='bfill', inplace=True)  # Backward-fill if necessary

    # Padding data to match the expected observation shape
    required_features = 24
    current_features = data.shape[1]
    if current_features < required_features:
        padding = required_features - current_features
        for i in range(padding):
            data[f'padding_{i+1}'] = 0
        print(f"Data padded to {required_features} features.")

    print("Initializing the ForexTrading environment...")
    env = ForexTradingEnv(data=data, window_size=10)
    print("Environment initialized successfully.")

    print("Loading the trained model...")
    model = PPO.load(model_path)
    print("Model loaded successfully.")

    print("Starting backtesting...")
    obs = env.reset()
    total_reward = 0
    trade_count = 0
    rewards = []
    equity_curve = []

    while True:
        try:
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            rewards.append(reward)
            equity_curve.append(total_reward)
            trade_count += 1
            if done:
                print("Episode finished.")
                break
        except IndexError as e:
            print(f"IndexError during backtesting: {e}")
            break

    # Calculate performance metrics
    sharpe_ratio = (np.mean(rewards) / np.std(rewards)) * np.sqrt(len(rewards)) if len(rewards) > 1 else 0
    max_drawdown = np.max(np.maximum.accumulate(rewards) - rewards) if rewards else 0
    win_rate = (sum(1 for r in rewards if r > 0) / len(rewards)) * 100 if rewards else 0

    print("Performance Metrics:")
    print(f"Total Reward: {total_reward}")
    print(f"Sharpe Ratio: {sharpe_ratio}")
    print(f"Max Drawdown: {max_drawdown}")
    print(f"Win Rate: {win_rate}%")

    # Save backtest results
    print("Saving backtest results...")
    if hasattr(env, 'trade_history') and env.trade_history:
        results = pd.DataFrame(env.trade_history, columns=["Time", "Price", "Reward", "Trade"])
        results_path = os.path.join(output_path, "backtest_results.csv")
        results.to_csv(results_path, index=False)
        print(f"Backtest results saved at {results_path}")
    else:
        print("No trade history available to save.")

    # Visualization
    print("Generating visualization...")
    plt.figure(figsize=(10, 6))
    plt.plot(equity_curve, label='Equity Curve')
    plt.xlabel('Trade Count')
    plt.ylabel('Total Reward')
    plt.title('Equity Curve')
    plt.legend()
    equity_curve_path = os.path.join(output_path, "equity_curve.png")
    plt.savefig(equity_curve_path)
    print(f"Equity curve saved at {equity_curve_path}")
    plt.show()

    print("Backtesting completed.")

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")



















































































