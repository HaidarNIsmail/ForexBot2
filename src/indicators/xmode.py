import pandas as pd
import numpy as np

def calculate_signals(df):
    # Example signal logic
    df['Buy_Signal'] = (df['EMA_50'] > df['EMA_200']) & (df['RSI'] < 30)
    df['Sell_Signal'] = (df['EMA_50'] < df['EMA_200']) & (df['RSI'] > 70)

    # Add persistence for signals
    signal_persistence = 3
    df['Buy_Signal'] = df['Buy_Signal'].rolling(window=signal_persistence, min_periods=1).max()
    df['Sell_Signal'] = df['Sell_Signal'].rolling(window=signal_persistence, min_periods=1).max()

    return df

if __name__ == "__main__":
    data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators.csv"
    output_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_signals.csv"

    df = pd.read_csv(data_path, index_col='time', parse_dates=True)
    df = calculate_signals(df)

    df.to_csv(output_path)
    print(f"Updated data with signals saved to: {output_path}")










