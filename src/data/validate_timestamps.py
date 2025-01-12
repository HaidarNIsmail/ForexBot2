import pandas as pd

# Path to the final cleaned file
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators_final.csv'

# Load the CSV
df = pd.read_csv(file_path)

# Convert 'time' column to datetime format and set it as the index
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

# Save the updated DataFrame
output_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators_final_with_index.csv'
df.to_csv(output_path)

print(f"Validated and updated file saved to: {output_path}")
