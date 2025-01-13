import pandas as pd
from src.indicators.indicators_setup import calculate_ema, calculate_rsi, calculate_macd, calculate_atr, calculate_bollinger_bands

# Example: Load the data (adjust the path as needed)
data = pd.read_csv('C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv')

# Calculate indicators
data['EMA_Short'] = calculate_ema(data, span=12)
data['EMA_Long'] = calculate_ema(data, span=50)
data['RSI'] = calculate_rsi(data)
data['MACD'], data['MACD_Signal'] = calculate_macd(data)
data['ATR'] = calculate_atr(data)
data['BB_Upper'], data['BB_Lower'] = calculate_bollinger_bands(data)

# Check the columns after adding indicators
print("Columns in dataset:", data.columns)

# Example strategy using the indicators
def strategy_logic(data):
    # Example conditions based on indicators
    data['Signal'] = 0  # Default no position
    data.loc[(data['EMA_Short'] > data['EMA_Long']) & (data['RSI'] < 30), 'Signal'] = 1  # Buy Signal
    data.loc[(data['EMA_Short'] < data['EMA_Long']) & (data['RSI'] > 70), 'Signal'] = -1  # Sell Signal
    return data

# Applying the strategy
data_with_signals = strategy_logic(data)

# Displaying the final dataset with signals
print(data_with_signals.tail())





