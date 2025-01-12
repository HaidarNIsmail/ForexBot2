import pandas as pd

# Load the CSV file
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD.csv'
df = pd.read_csv(file_path)

# Standardize column names
df.rename(columns={
    'time': 'Date',          # Adjust if needed
    'price_open': 'Open',
    'price_high': 'High',
    'price_low': 'Low',
    'price_close': 'Close',
    'volume': 'Volume'
}, inplace=True)

# Ensure required columns are present
required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise KeyError(f"Missing columns in DataFrame: {missing_columns}")

# Save the corrected data
df.to_csv(file_path, index=False)
