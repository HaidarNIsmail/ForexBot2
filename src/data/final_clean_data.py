import pandas as pd

# Load the cleaned data
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators_cleaned.csv'
df = pd.read_csv(file_path)

# Fill NaN values using backfill and forward-fill
df.fillna(method='bfill', inplace=True)
df.fillna(method='ffill', inplace=True)

# Save the final cleaned data
output_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators_final.csv'
df.to_csv(output_path, index=False)

print(f"Final cleaned data saved to: {output_path}")
