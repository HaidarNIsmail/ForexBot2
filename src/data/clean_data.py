import pandas as pd
from sklearn.impute import SimpleImputer

# Input and output file paths
input_file = 'C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators_final_with_index.csv'
output_file = 'C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv'

def clean_data():
    print("Reading the data...")
    try:
        # Load the data
        df = pd.read_csv(input_file, index_col=0)
        print(f"Data loaded successfully. Shape: {df.shape}")

        # Impute missing values
        print("Handling missing values...")
        imputer = SimpleImputer(strategy='mean')
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
        print("Missing values imputed.")

        # Optional: Drop rows with extreme outliers (if needed)
        # Define outlier thresholds
        # threshold = 3
        # df = df[(df - df.mean()).abs() / df.std() < threshold]

        # Save cleaned data
        print(f"Saving cleaned data to {output_file}...")
        df.to_csv(output_file)
        print("Cleaned data saved successfully.")

    except Exception as e:
        print(f"Error during data cleaning: {e}")

if __name__ == '__main__':
    clean_data()


