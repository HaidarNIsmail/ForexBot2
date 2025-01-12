import pandas as pd

# Path to the CSV file
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators.csv'

# Load the CSV file
df = pd.read_csv(file_path)

# Interpolate missing values
columns_to_interpolate = [
    'EMA_50', 'EMA_200', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram',
    'BB_High', 'BB_Low', 'BB_Middle', 'ATR', 'Ichimoku_Conversion',
    'Ichimoku_Base', 'Ichimoku_A', 'Ichimoku_B', 'Chikou_Span',
    'Stochastic_RSI', 'ADX'
]

for col in columns_to_interpolate:
    df[col] = df[col].replace(0, pd.NA).interpolate(method='linear')

# Save the cleaned data
output_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators_cleaned.csv'
df.to_csv(output_path, index=False)

print(f"Cleaned data saved to: {output_path}")

