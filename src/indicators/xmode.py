import pandas as pd
import matplotlib.pyplot as plt

# Signal Generation Logic
def calculate_signals(df):
    """
    Generate Buy and Sell signals based on EMA crossovers and RSI thresholds.
    """
    # Define parameters
    ema_short, ema_long, rsi_threshold = 5, 20, 30

    # Calculate EMA
    df['EMA_Short'] = df['Close'].ewm(span=ema_short, adjust=False).mean()
    df['EMA_Long'] = df['Close'].ewm(span=ema_long, adjust=False).mean()

    # Generate Buy and Sell Signals
    df['Buy_Signal'] = (df['EMA_Short'] > df['EMA_Long']) & (df['RSI'] < rsi_threshold)
    df['Sell_Signal'] = (df['EMA_Short'] < df['EMA_Long']) & (df['RSI'] > 100 - rsi_threshold)

    # Add Signal Persistence
    signal_persistence = 3
    df['Buy_Signal'] = df['Buy_Signal'].rolling(window=signal_persistence, min_periods=1).max().astype(bool)
    df['Sell_Signal'] = df['Sell_Signal'].rolling(window=signal_persistence, min_periods=1).max().astype(bool)

    # Debugging: Print Signal Counts
    print("Buy Signal Count:", df['Buy_Signal'].sum())
    print("Sell Signal Count:", df['Sell_Signal'].sum())

    return df

# Add Stop-Loss and Take-Profit Levels
def add_stop_loss_take_profit(df):
    """
    Add Stop-Loss and Take-Profit levels based on ATR.
    """
    atr_multiplier = 2.0
    df['Stop_Loss'] = df['Close'] - (df['ATR'] * atr_multiplier)
    df['Take_Profit'] = df['Close'] + (df['ATR'] * atr_multiplier)
    return df

# Visualization
def plot_signals_and_indicators(df):
    """
    Plot signals and key indicators for debugging.
    """
    # Plot EMA and Signals on Close Price
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Close Price', color='blue')
    plt.plot(df['EMA_Short'], label='EMA Short', color='green')
    plt.plot(df['EMA_Long'], label='EMA Long', color='red')
    plt.scatter(df.index[df['Buy_Signal']], df['Close'][df['Buy_Signal']], label='Buy Signal', marker='^', color='lime', alpha=0.8)
    plt.scatter(df.index[df['Sell_Signal']], df['Close'][df['Sell_Signal']], label='Sell Signal', marker='v', color='magenta', alpha=0.8)
    plt.title('Price with EMA Crossovers and Signals')
    plt.legend()
    plt.grid()
    plt.show()

    # Plot RSI
    plt.figure(figsize=(14, 4))
    plt.plot(df['RSI'], label='RSI', color='orange')
    plt.axhline(30, linestyle='--', color='red', label='Oversold (30)')
    plt.axhline(70, linestyle='--', color='green', label='Overbought (70)')
    plt.title('RSI Over Time')
    plt.legend()
    plt.grid()
    plt.show()

# Main Script
if __name__ == "__main__":
    # Load data
    data_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_indicators.csv"
    output_path = "C:/Users/haida/PycharmProjects/ForexBot2/data/data_with_signals.csv"
    df = pd.read_csv(data_path, index_col="time", parse_dates=True)

    # Generate Signals
    df = calculate_signals(df)

    # Add Stop-Loss and Take-Profit
    df = add_stop_loss_take_profit(df)

    # Debugging: Plot Signals and Indicators
    plot_signals_and_indicators(df)

    # Save Updated Data
    df.to_csv(output_path)
    print(f"Updated data with signals saved to: {output_path}")














