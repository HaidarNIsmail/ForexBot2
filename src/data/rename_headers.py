import pandas as pd

# Path to the CSV file
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'

# Load the CSV file
df = pd.read_csv(file_path)

# Rename headers to match the requirements
df.rename(columns={
    'time': 'time',          # Keep 'time' as is
    'open': 'Open',          # Rename 'open' to 'Open'
    'high': 'High',          # Rename 'high' to 'High'
    'low': 'Low',            # Rename 'low' to 'Low'
    'close': 'Close',        # Rename 'close' to 'Close'
    'tick_volume': 'Volume', # Rename 'tick_volume' to 'Volume'
    'spread': 'Spread',      # Keep 'spread' as is
    'real_volume': 'RealVolume'  # Rename 'real_volume' to 'RealVolume'
}, inplace=True)

# Save the updated file
output_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'
df.to_csv(output_path, index=False)

print(f"Headers renamed successfully and file saved to: {output_path}")

