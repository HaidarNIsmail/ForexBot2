import pandas as pd
import os
import matplotlib.pyplot as plt
from src.strategies.xmode import xmode_strategy

def backtest_strategy(df, initial_capital=10000.0):
    # basic backtest
    df = df.copy()

    # 'Positions' is from the xmode_strategy
    df['Market_Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Market_Returns'] * df['Positions'].shift(1)
    df['Strategy_Returns'].fillna(0, inplace=True)

    df['Cumulative_Returns'] = (1 + df['Strategy_Returns']).cumprod() * initial_capital
    df['Total'] = df['Cumulative_Returns']

    # performance metrics
    total_return = (df['Total'].iloc[-1] - initial_capital)/initial_capital * 100
    sharpe_ratio = (df['Strategy_Returns'].mean() / df['Strategy_Returns'].std() * (252**0.5)
                    if df['Strategy_Returns'].std() != 0 else 0)
    dd_series = (df['Total'].cummax() - df['Total']) / df['Total'].cummax()
    max_drawdown = dd_series.max() * 100

    print(f"Total Return: {total_return:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2f}%")

    # Plot results
    plt.figure(figsize=(12,6))
    plt.plot(df['Total'], label='X-Mode Strategy Value')
    # buy & hold
    plt.plot(df['Close'] * initial_capital / df['Close'].iloc[0], label='Buy & Hold')
    plt.title('Backtest - X Mode Strategy')
    plt.legend()
    plt.show()

    return df

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), '..','..','data','data_with_indicators.csv')

    try:
        data = pd.read_csv(data_path, index_col='time')
        # 1) Run the xmode logic
        from src.strategies.xmode import xmode_strategy
        df_xmode = xmode_strategy(data)

        # 2) Backtest
        results = backtest_strategy(df_xmode)

    except FileNotFoundError:
        print(f"Data file not found at {data_path}")
    except Exception as e:
        print("Error in backtest:", e)