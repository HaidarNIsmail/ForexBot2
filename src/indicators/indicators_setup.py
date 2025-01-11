import pandas as pd
import ta
from textblob import TextBlob


def analyze_sentiment(news_headlines):
    try:
        sentiments = [TextBlob(headline).sentiment.polarity for headline in news_headlines]
        return sentiments
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return None

def calculate_technical_indicators(df, news_headlines=None):

    # EMA
    df['EMA_50'] = ta.trend.ema_indicator(close=df['Close'], window=50)
    df['EMA_200'] = ta.trend.ema_indicator(close=df['Close'], window=200)

    # RSI
    df['RSI'] = ta.momentum.rsi(close=df['Close'], window=14)

    # MACD
    df['MACD'] = ta.trend.macd(close=df['Close'], window_slow=26, window_fast=12) # Removed window_sign
    df['MACD_Signal'] = ta.trend.macd_signal(close=df['Close'], window_slow=26, window_fast=12) # Removed window_sign
    df['MACD_Histogram'] = ta.trend.macd_diff(close=df['Close'], window_slow=26, window_fast=12) # Removed window_sign

    # Bollinger Bands
    bb_indicator = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_High'] = bb_indicator.bollinger_hband()
    df['BB_Low'] = bb_indicator.bollinger_lband()
    df['BB_Middle'] = bb_indicator.bollinger_mavg()

    # Average True Range (ATR)
    df['ATR'] = ta.volatility.average_true_range(high=df['High'], low=df['Low'], close=df['Close'], window=14)

    # Ichimoku Cloud (Corrected)
    ichimoku = ta.trend.IchimokuIndicator(high=df['High'], low=df['Low'])
    df['Ichimoku_Conversion'] = ichimoku.ichimoku_conversion_line()
    df['Ichimoku_Base'] = ichimoku.ichimoku_base_line()
    df['Ichimoku_A'] = ichimoku.ichimoku_a()
    df['Ichimoku_B'] = ichimoku.ichimoku_b()

    chikou_span_period = 26  # Standard period for Chikou Span
    df['Chikou_Span'] = df['Close'].shift(-chikou_span_period) # Manually calculate Chikou Span

    # Stochastic RSI
    df['Stochastic_RSI'] = ta.momentum.stochrsi(close=df['Close'])

    # ADX
    df['ADX'] = ta.trend.adx(high=df['High'], low=df['Low'], close=df['Close'])

    # Sentiment (Optional)
    if news_headlines is not None:
        sentiments = analyze_sentiment(news_headlines)
        if sentiments is not None:
            df['Sentiment'] = sentiments

    return df


# ... (Previous code for indicators setup from before)

if __name__ == "__main__":
    import os
    from Config.config import Config

    # Ensure that the `data` directory exists in your project. If not, create it.
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    full_data_path = os.path.join(os.path.dirname(__file__), '..', '..', Config.DATA_PATH) # Absolute path to EURUSD.csv
    output_file = os.path.join(output_dir, "data_with_indicators.csv") # Correct path, saves in forex_trading_bot/data

    try:
        df = pd.read_csv(full_data_path, index_col='time')
        df_with_indicators = calculate_technical_indicators(df.copy())
        df_with_indicators.to_csv(output_file)
        print(f"Data with technical indicators saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: Could not find the data file at: {full_data_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
