import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Signal Generation Logic
def calculate_signals(df):
    """
    Generate Buy and Sell signals based on EMA crossovers and RSI thresholds.
    """
    # Define parameters
    ema_short, ema_long, rsi_threshold = 50, 200, 30

    # Calculate EMA
    df['EMA_50'] = df['Close'].ewm(span=ema_short, adjust=False).mean()
    df['EMA_200'] = df['Close'].ewm(span=ema_long, adjust=False).mean()

    # Generate Buy and Sell Signals
    df['Buy_Signal'] = (df['EMA_50'] > df['EMA_200']) & (df['RSI'] < rsi_threshold)
    df['Sell_Signal'] = (df['EMA_50'] < df['EMA_200']) & (df['RSI'] > 100 - rsi_threshold)

    # Replace NaN signals with False
    df['Buy_Signal'] = df['Buy_Signal'].fillna(False)
    df['Sell_Signal'] = df['Sell_Signal'].fillna(False)

    return df

# Add Stop Loss and Take Profit Levels
def calculate_levels(df, atr_multiplier=1.5):
    """
    Calculate Stop Loss and Take Profit levels based on ATR.
    """
    if 'ATR' not in df.columns:
        raise ValueError("ATR column is missing. Ensure ATR is calculated before calling this function.")

    df['Stop_Loss'] = df['Close'] - (atr_multiplier * df['ATR'])
    df['Take_Profit'] = df['Close'] + (atr_multiplier * df['ATR'])

    return df

# Integrate ML Model Predictions
def add_ml_predictions(df, ml_model_path):
    """
    Add predictions from the trained ML model to validate signals.
    """
    # Load ML model
    print("Loading ML model...")
    ml_model = joblib.load(ml_model_path)

    # Define features used in the model
    features = ['EMA_50', 'EMA_200', 'RSI', 'MACD', 'ADX', 'Stochastic_RSI']

    # Ensure all required features are present
    missing_features = [feature for feature in features if feature not in df.columns]
    if missing_features:
        raise ValueError(f"Missing features in dataset: {missing_features}")

    # Predict signals using the ML model
    print("Generating ML-based predictions...")
    df['ML_Prediction'] = ml_model.predict(df[features])

    # Combine ML Predictions with Rule-Based Signals
    df['Hybrid_Buy'] = df['Buy_Signal'] & (df['ML_Prediction'] == 1)
    df['Hybrid_Sell'] = df['Sell_Signal'] & (df['ML_Prediction'] == -1)

    return df

# Main Script
if __name__ == "__main__":
    # File paths
    data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators.csv"
    ml_model_path = "C:/Users/haida/PycharmProjects/ForexBot2/models/ml_model.pkl"
    output_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_hybrid_signals.csv"

    # Load dataset
    df = pd.read_csv(data_path, index_col="time", parse_dates=True)

    # Generate Rule-Based Signals
    df = calculate_signals(df)

    # Add Stop Loss and Take Profit Levels
    df = calculate_levels(df)

    # Add ML Predictions
    df = add_ml_predictions(df, ml_model_path)

    # Save Updated Dataset
    df.to_csv(output_path)
    print(f"Updated dataset with hybrid signals saved to: {output_path}")


















