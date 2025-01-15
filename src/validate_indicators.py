import pandas as pd
import os
from src.indicators.indicators_setup import calculate_indicators
from ta.trend import ADXIndicator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for file paths
DATA_PATH = os.getenv('DATA_PATH', 'C:/Users/haida/PycharmProjects/ForexBot2/data/EURUSD.csv')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'C:/Users/haida/PycharmProjects/ForexBot2/output')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'EURUSD_with_indicators.csv')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def calculate_missing_indicators(df):
    """Calculate missing indicators and add them to the DataFrame."""
    print("Calculating missing indicators...")

    # ADX Calculation
    adx = ADXIndicator(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=14
    )
    df['adx'] = adx.adx()

    # Ichimoku Cloud Calculation
    high_9 = df['high'].rolling(window=9).max()
    low_9 = df['low'].rolling(window=9).min()
    high_26 = df['high'].rolling(window=26).max()
    low_26 = df['low'].rolling(window=26).min()
    high_52 = df['high'].rolling(window=52).max()
    low_52 = df['low'].rolling(window=52).min()

    df['ichimoku_leading_span_a'] = ((high_9 + low_9) / 2 + (high_26 + low_26) / 2) / 2
    df['ichimoku_leading_span_b'] = (high_52 + low_52) / 2

    print("Missing indicators calculated successfully.")


def main():
    try:
        # Load the data
        print("Loading data...")
        data = pd.read_csv(DATA_PATH)
        print(f"Data loaded successfully. Preview:\n{data.head()}")

        # Drop non-numeric columns if present
        non_numeric_cols = ['time']
        data.drop(columns=[col for col in non_numeric_cols if col in data.columns], inplace=True)
        print(f"Dropped non-numeric columns. Columns now:\n{data.columns}")

        # Calculate existing indicators
        print("Calculating existing indicators...")
        enriched_data = calculate_indicators(data)
        print(f"Existing indicators calculated. Preview:\n{enriched_data.head()}")

        # Calculate missing indicators
        calculate_missing_indicators(enriched_data)
        print(f"Indicators calculated. Preview:\n{enriched_data.head()}")

        # Save the enriched data
        print("Saving enriched data...")
        enriched_data.to_csv(OUTPUT_FILE, index=False)
        print(f"Enriched data saved successfully at {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()









