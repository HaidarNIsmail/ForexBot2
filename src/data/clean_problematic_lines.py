import pandas as pd

# File path
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD.csv'
cleaned_file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'

try:
    # Load the CSV, skipping problematic lines
    df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
    print("File loaded successfully with problematic lines skipped.")

    # Save the cleaned CSV
    df.to_csv(cleaned_file_path, index=False)
    print(f"Cleaned file saved to: {cleaned_file_path}")
except Exception as e:
    print(f"Error processing the CSV file: {e}")
