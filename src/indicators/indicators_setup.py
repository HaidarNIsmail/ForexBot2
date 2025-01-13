import pandas as pd

# EMA Calculation
def calculate_ema(data, span=14, column='Close'):
    return data[column].ewm(span=span, adjust=False).mean()

# RSI Calculation
def calculate_rsi(data, period=14, column='Close'):
    delta = data[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# MACD Calculation
def calculate_macd(data, fast=12, slow=26, signal=9, column='Close'):
    ema_fast = calculate_ema(data, span=fast, column=column)
    ema_slow = calculate_ema(data, span=slow, column=column)
    macd = ema_fast - ema_slow
    signal_line = calculate_ema(data, span=signal, column='MACD')
    return macd, signal_line

# ATR Calculation (added)
def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift(1))
    low_close = abs(data['Low'] - data['Close'].shift(1))
    tr = pd.concat([high_low, high_close, low_close], axis=1)
    tr = tr.max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

# Bollinger Bands Calculation
def calculate_bollinger_bands(data, window=20, column='Close'):
    rolling_mean = data[column].rolling(window=window).mean()
    rolling_std = data[column].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * 2)
    lower_band = rolling_mean - (rolling_std * 2)
    return upper_band, lower_band





