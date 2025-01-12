import pandas as pd
import matplotlib.pyplot as plt

# Backtesting Function
def backtest_strategy(df, initial_balance=10000):
    balance = initial_balance
    position_size = 0
    df['Equity'] = balance

    for index, row in df.iterrows():
        if row['Buy_Signal'] and position_size == 0:
            entry_price = row['Close']
            stop_loss = row['Stop_Loss']
            take_profit = row['Take_Profit']
            position_size = balance / entry_price
            print(f"Opened Buy at {index}: Entry = {entry_price}")

        elif row['Sell_Signal'] and position_size > 0:
            exit_price = row['Close']
            balance += position_size * (exit_price - entry_price)
            position_size = 0
            print(f"Closed Position at {index}: Exit = {exit_price}")

        df.at[index, 'Equity'] = balance + (position_size * row['Close'] if position_size > 0 else 0)

    return df

# Run Backtest
df = pd.read_csv("C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_signals.csv", index_col="time", parse_dates=True)
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
















