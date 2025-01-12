import pandas as pd

# Path to the cleaned CSV
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'

# Load the CSV file
df = pd.read_csv(file_path)

# Drop the duplicate columns with zeros
columns_to_drop = ['Open', 'High', 'Low', 'Close', 'Volume']
df = df.drop(columns=columns_to_drop)

# Save the updated CSV file
output_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'
df.to_csv(output_path, index=False)

print(f"Cleaned file saved without duplicate columns to: {output_path}")
