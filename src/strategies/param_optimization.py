import pandas as pd
import numpy as np
from scipy.optimize import minimize
from src.indicators.indicators_setup import calculate_ema, calculate_rsi, calculate_macd

def objective_function(params, *args):
    """
    Objective function to minimize for parameter optimization.
    """
    data = args[0]
    short_ema, long_ema, rsi_period, macd_short, macd_long, macd_signal = params

    # Calculate EMA
    data['EMA_Short'] = calculate_ema(data, 'Close', span=int(short_ema))
    data['EMA_Long'] = calculate_ema(data, 'Close', span=int(long_ema))

    # Calculate RSI
    data['RSI'] = calculate_rsi(data, 'Close', period=int(rsi_period))

    # Calculate MACD
    data['MACD'], data['Signal_Line'] = calculate_macd(
        data, 'Close', short_span=int(macd_short), long_span=int(macd_long), signal_span=int(macd_signal)
    )

    # Example trading strategy
    data['Signal'] = np.where((data['Close'] > data['EMA_Short']) &
                              (data['RSI'] > 50) &
                              (data['MACD'] > data['Signal_Line']), 1, -1)

    # Simulate returns
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Close'].pct_change()

    # Calculate negative Sharpe ratio as the objective
    mean_return = data['Strategy_Return'].mean()
    std_return = data['Strategy_Return'].std()
    if std_return == 0:
        return np.inf  # Avoid division by zero
    sharpe_ratio = mean_return / std_return
    return -sharpe_ratio

def optimize_parameters(data, initial_params):
    """
    Optimizes trading strategy parameters.
    """
    result = minimize(
        objective_function,
        initial_params,
        args=(data,),
        method='Nelder-Mead'
    )
    return result

if __name__ == "__main__":
    print("Loading data from C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv...")
    data = pd.read_csv("C:/Users/haida/PycharmProjects/ForexBot2/data/cleaned_data.csv")
    print("Data loaded successfully.")

    # Initial parameters for optimization
    initial_params = [12, 26, 14, 12, 26, 9]  # Short EMA, Long EMA, RSI period, MACD parameters

    print("Optimizing parameters...")
    result = optimize_parameters(data, initial_params)

    print("Optimization complete.")
    print("Optimized parameters:", result.x)
    print("Optimization success:", result.success)
    print("Optimization message:", result.message)








