import pandas as pd
from src.indicators.indicators_setup import calculate_ema, calculate_rsi, calculate_macd

# Optimized parameters
SHORT_EMA = 12  # Optimized short EMA period
LONG_EMA = 26  # Optimized long EMA period
RSI_PERIOD = 13  # Optimized RSI period
MACD_SHORT = 12  # Optimized MACD short span
MACD_LONG = 28  # Optimized MACD long span
MACD_SIGNAL = 9  # Optimized MACD signal span


def backtest_strategy(data):
    """
    Backtest the strategy using the optimized parameters.
    """
    print("Starting backtest...")

    # Calculate indicators
    data['EMA_Short'] = calculate_ema(data['Close'], SHORT_EMA)
    data['EMA_Long'] = calculate_ema(data['Close'], LONG_EMA)
    data['RSI'] = calculate_rsi(data['Close'], RSI_PERIOD)
    data['MACD'], data['Signal_Line'] = calculate_macd(
        data['Close'], MACD_SHORT, MACD_LONG, MACD_SIGNAL
    )

    # Initialize trading signals and balance
    data['Position'] = 0  # 1 for buy, -1 for sell, 0 for neutral
    balance = 10000  # Initial balance
    position_size = 0
    print("Indicators calculated. Starting trade simulation...")

    for i in range(1, len(data)):
        if data['EMA_Short'][i] > data['EMA_Long'][i] and data['RSI'][i] < 30:
            if data['Position'][i - 1] <= 0:  # Check if no active buy position
                # Buy signal
                data.loc[i, 'Position'] = 1
                position_size = balance / data['Close'][i]
                print(f"Buy at {data['Close'][i]} on {data.index[i]}")
        elif data['EMA_Short'][i] < data['EMA_Long'][i] and data['RSI'][i] > 70:
            if data['Position'][i - 1] >= 0:  # Check if no active sell position
                # Sell signal
                data.loc[i, 'Position'] = -1
                balance = position_size * data['Close'][i]
                print(f"Sell at {data['Close'][i]} on {data.index[i]}")
                position_size = 0
        else:
            # Neutral signal
            data.loc[i, 'Position'] = data['Position'][i - 1]

    print("Backtest complete.")
    return balance, data


def main():
    """
    Main function to execute the backtest.
    """
    # Load cleaned data
    data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv"
    print(f"Loading data from {data_path}...")
    data = pd.read_csv(data_path)
    print(f"Data loaded successfully. Shape: {data.shape}")

    # Run backtest
    final_balance, data_with_signals = backtest_strategy(data)
    print(f"Final balance after backtest: ${final_balance:.2f}")

    # Save results
    result_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/backtest_results.csv"
    print(f"Saving backtest results to {result_path}...")
    data_with_signals.to_csv(result_path, index=False)
    print("Backtest results saved successfully.")


if __name__ == "__main__":
    main()


















