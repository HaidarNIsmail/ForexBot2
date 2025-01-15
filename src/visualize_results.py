import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths
output_path = os.getenv("OUTPUT_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/output")
backtest_results_path = os.path.join(output_path, "backtest_results.csv")

# Load backtest data
try:
    print("Loading backtest results...")
    results = pd.read_csv(backtest_results_path)
    print("Results loaded successfully. Preview:")
    print(results.head())

    # Equity Curve
    results['Cumulative Reward'] = results['Reward'].cumsum()

    plt.figure(figsize=(12, 6))
    plt.plot(results['Time'], results['Cumulative Reward'], label="Equity Curve", color='blue')
    plt.title("Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Reward")
    plt.legend()
    plt.grid()
    plt.show()

    # Trade Analysis
    trades = results[results['Trade'] == 1]  # Filter trade rows
    plt.figure(figsize=(12, 6))
    plt.plot(results['Time'], results['Price'], label="Price", color='gray')
    plt.scatter(trades['Time'], trades['Price'], label="Trade Entry/Exit", color='red', marker='x')
    plt.title("Trade Analysis")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()

    # Performance Metrics
    win_trades = trades[trades['Reward'] > 0]
    loss_trades = trades[trades['Reward'] <= 0]

    win_rate = len(win_trades) / len(trades) * 100 if len(trades) > 0 else 0
    avg_return = trades['Reward'].mean() if len(trades) > 0 else 0
    max_drawdown = results['Cumulative Reward'].min()
    sharpe_ratio = results['Reward'].mean() / results['Reward'].std() if results['Reward'].std() != 0 else 0

    print("\nPerformance Metrics:")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Return per Trade: {avg_return:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

except FileNotFoundError:
    print(f"Error: Backtest results file not found at {backtest_results_path}")
except Exception as e:
    print(f"Unexpected error: {e}")
