import pandas as pd
import numpy as np
import ta
from Config.config import Config


def trend_following_strategy(df, short_ema_period=5, long_ema_period=20):
    df = df.copy()

    df['Short_EMA'] = ta.trend.ema_indicator(df['Close'], window=short_ema_period, fillna=True)
    df['Long_EMA'] = ta.trend.ema_indicator(df['Close'], window=long_ema_period, fillna=True)

    # Initialize 'Signal' column
    df['Signal'] = 0.0

    # Generate buy/sell signals
    df.loc[df.index[short_ema_period:], 'Signal'] = np.where(
        df['Short_EMA'][short_ema_period:] > df['Long_EMA'][short_ema_period:], 1.0, -1.0
    )

    # Calculate Positions
    df['Positions'] = df['Signal'].diff()
    df['Positions'] = df['Positions'].replace({2.0: 1.0, -2.0: -1.0, 0.0: 0.0}).fillna(0.0)

    # Debugging: Print EMA and Signal relationships
    print(df[['Close', 'Short_EMA', 'Long_EMA', 'Signal', 'Positions']].tail(60))
    import matplotlib.pyplot as plt

    def plot_emas(df):
        plt.figure(figsize=(14, 7))
        plt.plot(df['Close'], label='Close Price', color='blue')
        plt.plot(df['Short_EMA'], label=f'Short EMA ({short_ema_period})', color='red')
        plt.plot(df['Long_EMA'], label=f'Long EMA ({long_ema_period})', color='green')
        plt.legend()
        plt.title('Close Price and EMAs')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

    # Call this function within trend_following_strategy before returning
    plot_emas(df)
    return df


if __name__ == "__main__":
    import os

    full_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'data_with_indicators.csv')

    try:
        data = pd.read_csv(full_data_path, index_col='time')
        df_trend = trend_following_strategy(data)
        print(df_trend[['Close', 'Short_EMA', 'Long_EMA', 'Signal', 'Positions']].tail(50))

    except FileNotFoundError:
        print(f"Could not find the data file. Please ensure that it exists. Path used: {full_data_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")