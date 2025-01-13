import pandas as pd


def calculate_ema(column, span):
    """
    Calculate the Exponential Moving Average (EMA) for a given column.

    Args:
        column (pd.Series): The data column to calculate EMA for (e.g., Close prices).
        span (int): The span for the EMA calculation.

    Returns:
        pd.Series: The calculated EMA values.
    """
    return column.ewm(span=span, adjust=False).mean()


def calculate_rsi(column, period=14):
    """
    Calculate the Relative Strength Index (RSI).

    Args:
        column (pd.Series): The data column to calculate RSI for (e.g., Close prices).
        period (int): The period for the RSI calculation.

    Returns:
        pd.Series: The calculated RSI values.
    """
    delta = column.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(column, fast=12, slow=26, signal=9):
    """
    Calculate the Moving Average Convergence Divergence (MACD).

    Args:
        column (pd.Series): The data column to calculate MACD for (e.g., Close prices).
        fast (int): The span for the fast EMA.
        slow (int): The span for the slow EMA.
        signal (int): The span for the signal line.

    Returns:
        tuple: MACD line and Signal line as pd.Series.
    """
    ema_fast = column.ewm(span=fast, adjust=False).mean()
    ema_slow = column.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line




