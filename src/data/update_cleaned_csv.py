import pandas as pd

# Path to the cleaned CSV file
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'

# Load the cleaned data
df = pd.read_csv(file_path)

# Add missing columns with default values
for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    if col not in df.columns:
        df[col] = 0.0  # Use default value

# Save the updated DataFrame
output_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'
df.to_csv(output_path, index=False)
print(f"Updated data with missing columns saved to: {output_path}")
