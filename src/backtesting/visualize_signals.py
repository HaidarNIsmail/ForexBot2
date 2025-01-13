import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BACKTEST_RESULTS_PATH = os.getenv("BACKTEST_RESULTS_PATH", "data/backtest_results.csv")


# Load backtest results
def load_results(file_path):
    try:
        return pd.read_csv(file_path, parse_dates=["Timestamp"])
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


# Plot price and signals
def plot_signals(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df["Timestamp"], df["Close"], label="Price", color="blue", alpha=0.7)
    buy_signals = df[df["Signal"] == "Buy"]
    sell_signals = df[df["Signal"] == "Sell"]

    plt.scatter(buy_signals["Timestamp"], buy_signals["Close"], color="green", label="Buy Signal", marker="^", alpha=1)
    plt.scatter(sell_signals["Timestamp"], sell_signals["Close"], color="red", label="Sell Signal", marker="v", alpha=1)

    plt.title("Price Chart with Buy and Sell Signals")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


# Plot equity curve
def plot_equity_curve(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df["Timestamp"], df["Equity"], label="Equity Curve", color="purple", alpha=0.8)
    plt.title("Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


# Summary of performance
def print_summary(df):
    total_trades = len(df[df["Signal"].notnull()])
    buy_trades = len(df[df["Signal"] == "Buy"])
    sell_trades = len(df[df["Signal"] == "Sell"])
    final_equity = df["Equity"].iloc[-1]
    initial_equity = df["Equity"].iloc[0]
    profit = final_equity - initial_equity
    profit_pct = (profit / initial_equity) * 100

    print(f"Total Trades: {total_trades}")
    print(f"Buy Trades: {buy_trades}")
    print(f"Sell Trades: {sell_trades}")
    print(f"Final Equity: {final_equity:.2f}")
    print(f"Net Profit: {profit:.2f} ({profit_pct:.2f}%)")


# Main function
if __name__ == "__main__":
    print("Loading backtest results...")
    results = load_results(BACKTEST_RESULTS_PATH)
    if results is not None:
        print("Plotting signals...")
        plot_signals(results)
        print("Plotting equity curve...")
        plot_equity_curve(results)
        print("Summary of performance:")
        print_summary(results)
