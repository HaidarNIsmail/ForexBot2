import pandas as pd


# Example function to generate signals (you may adjust this based on your strategy)
def generate_signals(data):
    # Example: Create a signal column based on the Close price and EMA50
    data['Signal'] = (data['Close'] > data['EMA_50']).astype(int)  # Buy signal when Close > EMA_50
    return data


def backtest_strategy(data):
    # Add signal generation logic
    data = generate_signals(data)

    # Initialize variables for backtest
    balance = 10000  # Initial balance (you can adjust this)
    position = None  # No open position at the beginning
    entry_price = 0
    position_size = 1000  # Size of each trade (adjust as needed)

    for idx, row in data.iterrows():
        if row['Signal'] == 1 and position is None:  # Buy signal
            position = 'Long'
            entry_price = row['Close']
            print(f"Buying at {entry_price} on {row['time']}")
        elif row['Signal'] == 0 and position == 'Long':  # Sell signal for a Long position
            balance += (row['Close'] - entry_price) * position_size
            position = None
            print(f"Selling at {row['Close']} on {row['time']}")

    # Final balance after the backtest
    return balance


# Load data (you need to ensure the path is correct)
data = pd.read_csv('C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv')

# Show the columns in the dataset
print("Columns in dataset:", data.columns)

# Backtest the strategy
final_balance = backtest_strategy(data)

# Print the final balance after the backtest
print(f"Final balance after backtest: {final_balance}")





















