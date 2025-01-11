import pandas as pd
import os
from Config.config import Config

def clean_data(df):
    # Rename columns for convenience
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'tick_volume': 'Volume',
        'real_volume': 'Real_Volume'
    }, inplace=True)

    # Convert relevant columns to numeric
    for col in ['Open', 'High', 'Low', 'Close', 'Volume', 'Real_Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert index to DateTimeIndex
    df.index = pd.to_datetime(df.index)

    # Remove rows with zero volume (optional)
    df = df[df['Volume'] != 0]

    # Drop any rows with missing values
    df.dropna(inplace=True)

    return df

if __name__ == "__main__":
    try:
        # Build the full/absolute path to the CSV file
        full_data_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            Config.DATA_PATH
        )

        # Read the raw CSV data
        df = pd.read_csv(full_data_path, index_col='time')

        # Clean the data
        cleaned_df = clean_data(df)

        # Save the cleaned data back to CSV
        cleaned_df.to_csv(full_data_path, index=True)
        print(f"Cleaned data saved to: {full_data_path}")

    except FileNotFoundError:
        print(f"Error. Could not find the data file at: {full_data_path}")
    except Exception as e:
        print(f"An unexpected error occurred during data cleaning: {e}")
