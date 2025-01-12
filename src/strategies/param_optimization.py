import pandas as pd
from itertools import product

# Load data
data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators.csv"
df = pd.read_csv(data_path, index_col="time", parse_dates=True)

# Optimization Function
def optimize_parameters(df, ema_short_values, ema_long_values, rsi_values):
    best_params = None
    best_return = float('-inf')

    for ema_short, ema_long, rsi_threshold in product(ema_short_values, ema_long_values, rsi_values):
        # Generate Signals
        df['EMA_Short'] = df['Close'].ewm(span=ema_short).mean()
        df['EMA_Long'] = df['Close'].ewm(span=ema_long).mean()
        df['RSI'] = (df['Close'] - df['Close'].shift(1)).cumsum()  # Simplified RSI for testing

        df['Buy_Signal'] = (df['EMA_Short'] > df['EMA_Long']) & (df['RSI'] < rsi_threshold)
        df['Sell_Signal'] = (df['EMA_Short'] < df['EMA_Long']) & (df['RSI'] > 100 - rsi_threshold)

        # Backtest Strategy
        df['Equity'] = 10000  # Reset balance
        for index, row in df.iterrows():
            if row['Buy_Signal']:
                df.at[index, 'Equity'] += 10  # Simplified trading logic
            elif row['Sell_Signal']:
                df.at[index, 'Equity'] -= 10

        # Calculate Return
        total_return = df['Equity'].iloc[-1]
        if total_return > best_return:
            best_return = total_return
            best_params = (ema_short, ema_long, rsi_threshold)

    print(f"Best Parameters: EMA Short = {best_params[0]}, EMA Long = {best_params[1]}, RSI Threshold = {best_params[2]}")
    return best_params

# Define Parameter Ranges
ema_short_values = range(5, 20, 5)
ema_long_values = range(20, 50, 10)
rsi_values = range(30, 50, 10)

# Run Optimization
optimize_parameters(df, ema_short_values, ema_long_values, rsi_values)

