import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = os.getenv("BASE_DIR", "C:/Users/haida/PycharmProjects/ForexBot2")
INPUT_PATH = os.path.join(BASE_DIR, "output/EURUSD_with_indicators.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "output/EURUSD_cleaned.csv")

print("Loading enriched dataset...")
try:
    data = pd.read_csv(INPUT_PATH)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Failed to load dataset: {e}")
    exit()

# Display NaN Summary
print("NaN Summary:")
print(data.isna().sum())

# Display basic statistics
print("Basic Statistics:")
print(data.describe())

# Handle NaN Values
print("Handling NaN values...")
data.fillna(method='bfill', inplace=True)  # Backward fill
data.fillna(method='ffill', inplace=True)  # Forward fill (if necessary)

# Verify no remaining NaNs
print("NaN Summary After Cleanup:")
print(data.isna().sum())

# Save cleaned dataset
print("Saving cleaned dataset...")
try:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    data.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned dataset saved at {OUTPUT_PATH}")
except Exception as e:
    print(f"Failed to save cleaned dataset: {e}")

