import pandas as pd
import matplotlib.pyplot as plt

# Backtesting Function
def backtest_strategy(df, initial_balance=10000):
    """
    Perform a backtest using Buy/Sell signals and Stop Loss/Take Profit levels.
    """
    balance = initial_balance
    position_size = 0
    df['Equity'] = balance

    for index, row in df.iterrows():
        # Open Buy Position
        if row['Hybrid_Buy'] and position_size == 0:
            entry_price = row['Close']
            stop_loss = row['Stop_Loss']
            take_profit = row['Take_Profit']
            position_size = balance / entry_price
            print(f"Opened Buy at {index}: Entry = {entry_price}")

        # Open Sell Position
        elif row['Hybrid_Sell'] and position_size == 0:
            entry_price = row['Close']
            stop_loss = row['Take_Profit']
            take_profit = row['Stop_Loss']
            position_size = balance / entry_price
            print(f"Opened Sell at {index}: Entry = {entry_price}")

        # Close Position
        if position_size > 0:
            if row['Close'] <= stop_loss or row['Close'] >= take_profit:
                exit_price = row['Close']
                balance += position_size * (exit_price - entry_price)
                print(f"Closed Position at {index}: Exit = {exit_price}, Balance = {balance}")
                position_size = 0

        # Update Equity
        df.at[index, 'Equity'] = balance + (position_size * row['Close'] if position_size > 0 else 0)

    return df

# Main Script
data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_hybrid_signals.csv"
df = pd.read_csv(data_path, index_col="time", parse_dates=True)

# Backtest the strategy
df = backtest_strategy(df)

# Plot Equity Curve
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Equity'], label="Equity Curve")
plt.title("Strategy Backtest")
plt.legend()
plt.grid()
plt.show()

# Save Results
output_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/backtest_results.csv"
df.to_csv(output_path)
print(f"Backtest results saved to: {output_path}")

















