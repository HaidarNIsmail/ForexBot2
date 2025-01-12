import pandas as pd

# File path to your CSV
file_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD.csv'

# Step 1: Try loading the file with error handling
try:
    # Use engine='python' for more flexible parsing
    df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
    print("Data loaded successfully with problematic lines skipped.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    df = None

# Step 2: Validate the data structure if loading succeeded
if df is not None:
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
    else:
        print("All required columns are present.")

    # Step 3: Save the cleaned file (if needed)
    output_path = 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD_cleaned.csv'
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")
else:
    print("Could not load the data. Check the file for formatting issues.")

