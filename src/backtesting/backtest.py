import gym
import pandas as pd
from stable_baselines3 import PPO
from src.forex_trading_env import ForexTradingEnv  # Adjusted path to 'src'

# Load the cleaned data
data = pd.read_csv("C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv")  # Updated path

# Create the trading environment
env = ForexTradingEnv(data)

# Load the pre-trained model
model = PPO.load("C:/Users/haida/PycharmProjects/ForexBot2/src/ppo_forex_model.zip")  # Updated path for the model


# Backtesting the strategy
def backtest_strategy(data):
    trade_rewards = []  # Store the rewards for each trade
    position = None  # No position at the start
    balance = 10000  # Initial balance

    # Remove the 'time' column if it exists
    if 'time' in data.columns:
        data = data.drop(columns=['time'])

    for i in range(len(data) - 10):  # Assuming a window size of 10 for the environment
        current_data = data.iloc[i:i + 10]  # Get the window of data
        action, _ = model.predict(current_data.values)  # Get action from the model (Buy, Sell, Hold)

        # Implement the trading logic
        if action == 0 and position is None:  # Buy signal
            position = current_data['Close'].iloc[-1]
            balance -= position  # Buying the asset
        elif action == 1 and position is not None:  # Sell signal
            balance += current_data['Close'].iloc[-1]  # Selling the asset
            position = None  # Exit position

        # Record the trade reward (this is a placeholder; you can calculate more specific rewards)
        trade_rewards.append(balance)

    final_balance = balance if position is None else balance + current_data['Close'].iloc[
        -1]  # Closing the position if still open
    return final_balance, trade_rewards



# Run the backtest
final_balance, trade_rewards = backtest_strategy(data)

# Print results
print(f"Final balance after backtest: {final_balance}")




























