import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_strategy(df, initial_balance=10000):
    balance = initial_balance
    equity_curve = []
    position = 0  # 1 for long, -1 for short, 0 for no position

    for idx, row in df.iterrows():
        if row['Buy_Signal']:
            position = 1
            entry_price = row['Close']

        elif row['Sell_Signal']:
            position = -1
            entry_price = row['Close']

        # Stop Loss and Take Profit
        if position == 1 and row['Low'] < row['Stop_Loss']:
            balance += (row['Stop_Loss'] - entry_price) * position
            position = 0

        elif position == -1 and row['High'] > row['Take_Profit']:
            balance += (entry_price - row['Take_Profit']) * abs(position)
            position = 0

        # Update equity curve
        equity_curve.append(balance)

    df['Strategy_Equity'] = equity_curve
    return df

if __name__ == "__main__":
    data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_signals.csv"
    output_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/backtest_results.csv"

    df = pd.read_csv(data_path, index_col='time', parse_dates=True)

    # Ensure required columns are present
    required_columns = ['Stop_Loss', 'Take_Profit', 'Buy_Signal', 'Sell_Signal']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Backtest strategy
    df = backtest_strategy(df)

    # Calculate performance metrics
    df['Strategy_Returns'] = df['Strategy_Equity'].pct_change().fillna(0)
    total_return = (df['Strategy_Equity'].iloc[-1] - df['Strategy_Equity'].iloc[0]) / df['Strategy_Equity'].iloc[0] * 100
    sharpe_ratio = df['Strategy_Returns'].mean() / df['Strategy_Returns'].std() * np.sqrt(252)
    max_drawdown = ((df['Strategy_Equity'].cummax() - df['Strategy_Equity']) / df['Strategy_Equity'].cummax()).max() * 100

    print(f"Total Return: {total_return:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2f}%")

    # Save results
    df.to_csv(output_path)
    print(f"Backtest results saved to: {output_path}")

    # Plot equity curve
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Strategy_Equity'], label='Strategy Equity Curve')
    plt.title('Strategy Backtest')
    plt.legend()
    plt.show()














