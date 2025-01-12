import pandas as pd
import ta
from textblob import TextBlob
from src.indicators.maw import calculate_maw
from src.indicators.rtd import calculate_rtd
from src.indicators.xmode import xmode_strategy  # Ensure this is correctly imported
import os
from Config.config import Config

def analyze_sentiment(news_headlines):
    try:
        sentiments = [TextBlob(headline).sentiment.polarity for headline in news_headlines]
        return sentiments
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return None

def calculate_technical_indicators(df, news_headlines=None):
    try:
        print("Starting indicator calculations...")

        # Check if required columns exist
        required_columns = {'Open', 'High', 'Low', 'Close', 'Volume'}
        missing_columns = required_columns.difference(df.columns)
        if missing_columns:
            raise KeyError(f"Missing columns in DataFrame: {', '.join(missing_columns)}")

        # EMA Calculation
        print("Calculating EMAs...")
        df['EMA_50'] = ta.trend.ema_indicator(close=df['Close'], window=50)
        df['EMA_200'] = ta.trend.ema_indicator(close=df['Close'], window=200)

        # RSI
        print("Calculating RSI...")
        df['RSI'] = ta.momentum.rsi(close=df['Close'], window=14)

        # MACD
        print("Calculating MACD...")
        df['MACD'] = ta.trend.macd(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
        df['MACD_Signal'] = ta.trend.macd_signal(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
        df['MACD_Histogram'] = ta.trend.macd_diff(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)

        # Bollinger Bands
        print("Calculating Bollinger Bands...")
        bb_indicator = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
        df['BB_High'] = bb_indicator.bollinger_hband()
        df['BB_Low'] = bb_indicator.bollinger_lband()
        df['BB_Middle'] = bb_indicator.bollinger_mavg()

        # Average True Range (ATR)
        print("Calculating ATR...")
        df['ATR'] = ta.volatility.average_true_range(high=df['High'], low=df['Low'], close=df['Close'], window=14)

        # Ichimoku Cloud
        print("Calculating Ichimoku Cloud...")
        ichimoku = ta.trend.IchimokuIndicator(high=df['High'], low=df['Low'])
        df['Ichimoku_Conversion'] = ichimoku.ichimoku_conversion_line()
        df['Ichimoku_Base'] = ichimoku.ichimoku_base_line()
        df['Ichimoku_A'] = ichimoku.ichimoku_a()
        df['Ichimoku_B'] = ichimoku.ichimoku_b()
        df['Chikou_Span'] = df['Close'].shift(-26)

        # Stochastic RSI
        print("Calculating Stochastic RSI...")
        df['Stochastic_RSI'] = ta.momentum.stochrsi(close=df['Close'])

        # ADX
        print("Calculating ADX...")
        df['ADX'] = ta.trend.adx(high=df['High'], low=df['Low'], close=df['Close'])

        # Calculate MAW, RTD, and X-Mode
        print("Calculating MAW...")
        df = calculate_maw(df)
        print("Calculating RTD...")
        df = calculate_rtd(df)
        print("Calculating X-Mode...")
        df = xmode_strategy(df)

        # Sentiment (using TextBlob, if applicable)
        if news_headlines is not None:
            print("Analyzing sentiment...")
            sentiments = analyze_sentiment(news_headlines)
            if sentiments is not None:
                df['Sentiment'] = sentiments

    except KeyError as e:
        print(f"KeyError: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during technical indicator calculation: {e}")
        return None

    # Drop any rows with NaN values resulting from indicator calculations
    df.dropna(inplace=True)

    return df

if __name__ == "__main__":
    # Load data
    full_data_path = os.path.join(os.path.dirname(__file__), '..', '..', Config.DATA_PATH)

    try:
        df = pd.read_csv(full_data_path, index_col='time')

        # Ensure the index is a DatetimeIndex
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
            print("Converted 'time' column to DatetimeIndex.")

        print("Calculating technical indicators...")
        df_with_indicators = calculate_technical_indicators(df.copy())

        if df_with_indicators is not None:
            df_with_indicators.to_csv("data/data_with_indicators.csv")
            print(f"Data with technical indicators saved to data/data_with_indicators.csv")
        else:
            print("Error during indicator calculations.")

    except FileNotFoundError:
        print(f"Error: Could not find the data file at: {full_data_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
