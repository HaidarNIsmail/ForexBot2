import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load data
data_path = "../../data/data_with_indicators.csv"
df = pd.read_csv(data_path)

# Ensure required columns are present
required_columns = [
    'EMA_50', 'EMA_200', 'RSI', 'MACD', 'ADX', 'Stochastic_RSI', 'Buy_Signal', 'Sell_Signal'
]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

# Create target variable
df['Target'] = 0  # Default: No signal
df.loc[df['Buy_Signal'] == True, 'Target'] = 1  # Buy signal
df.loc[df['Sell_Signal'] == True, 'Target'] = -1  # Sell signal

# Select features and target
features = ['EMA_50', 'EMA_200', 'RSI', 'MACD', 'ADX', 'Stochastic_RSI']
X = df[features]
y = df['Target']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the trained model
output_path = "../../models/ml_model.pkl"
joblib.dump(model, output_path)
print(f"ML model saved to: {output_path}")





