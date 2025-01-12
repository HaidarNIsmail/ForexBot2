import pandas as pd
import numpy as np
import math

def calculate_maw(df, source='Close', ss_period=444, maw_period=1111, ema_period=11):
    """
    Calculates the Moving Average Wave (MAW) indicator.

    Args:
        df (pd.DataFrame): DataFrame containing price data.
        source (str): Column name for the source data (default: 'Close').
        ss_period (int): Period for Super Smoother.
        maw_period (int): Period for MAW calculation.
        ema_period (int): Period for EMA smoothing.

    Returns:
        pd.DataFrame: DataFrame with added 'MAW' column.
    """
    df = df.copy()
    SQRT2xPI = np.sqrt(8.0) * np.arcsin(1.0)  # Constant
    alpha = SQRT2xPI / ss_period
    beta = np.exp(-alpha)
    gamma = -beta * beta
    delta = 2.0 * beta * math.cos(alpha)

    # Initialize 'super_smooth' with NaN
    df['super_smooth'] = np.nan

    # Calculate 'super_smooth' using recursive formula
    for i in range(2, len(df)):
        series_sum = df[source].iloc[i] + df[source].iloc[i - 1]
        prev1 = df['super_smooth'].iloc[i - 1] if i - 1 >= 0 else 0.0
        prev2 = df['super_smooth'].iloc[i - 2] if i - 2 >= 0 else 0.0
        df.at[i, 'super_smooth'] = (1.0 - delta - gamma) * (series_sum) * 0.5 + \
                                    delta * prev1 + \
                                    gamma * prev2

    # Calculate slope
    df['slope'] = (df['super_smooth'].shift(maw_period) - df['super_smooth']) / maw_period

    # Calculate E
    df['E'] = 0.0
    for i in range(maw_period, len(df)):
        e_sum = 0.0
        for j in range(1, maw_period + 1):
            if i - j >= 0:
                e_sum += df['super_smooth'].iloc[i] + j * df['slope'].iloc[i] - df['super_smooth'].iloc[i - j]
        df.at[i, 'E'] = e_sum / maw_period

    # Calculate EMA
    zeta = 2.0 / (ema_period + 1.0)
    df['EMA'] = df['E'].ewm(span=ema_period, adjust=False).mean()

    # Calculate raw_output
    df['raw_output'] = df.apply(lambda row: row['E'] / math.sqrt(row['EMA']) if row['EMA'] != 0 else 0.0, axis=1)

    # Calculate scaled_output
    df['max_maw'] = df['raw_output'].rolling(window=maw_period).max()
    df['min_maw'] = df['raw_output'].rolling(window=maw_period).min()
    df['scaled_output'] = 200 * (df['raw_output'] - df['min_maw']) / (df['max_maw'] - df['min_maw']) - 100
    df['scaled_output'] = df['scaled_output'].fillna(0)  # Handle NaN

    # Assign to 'MAW' column
    df['MAW'] = df['scaled_output']

    # Clean up intermediate columns
    df.drop(['super_smooth', 'slope', 'E', 'EMA', 'raw_output', 'max_maw', 'min_maw', 'scaled_output'], axis=1, inplace=True)

    return df