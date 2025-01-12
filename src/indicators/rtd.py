# src/indicators/rtd.py

import pandas as pd
import numpy as np
import math

def get_mesa(df, src_in, fast, slow):
    """
    Calculate MESA Moving Average (MAMA and FAMA).

    Args:
        df (pd.DataFrame): DataFrame containing price data.
        src_in (str): Source column name (e.g., 'Close').
        fast (float): Fast limit parameter.
        slow (float): Slow limit parameter.

    Returns:
        tuple: (MAMA, FAMA) as pd.Series
    """
    price = df[src_in]
    MAMA = pd.Series(np.nan, index=df.index)
    FAMA = pd.Series(np.nan, index=df.index)

    PI = 3.14159

    # Initialize variables
    Smooth = pd.Series(np.nan, index=df.index)
    Detrender = pd.Series(np.nan, index=df.index)
    I1 = pd.Series(np.nan, index=df.index)
    Q1 = pd.Series(np.nan, index=df.index)
    jI = pd.Series(np.nan, index=df.index)
    jQ = pd.Series(np.nan, index=df.index)
    I2 = pd.Series(np.nan, index=df.index)
    Q2 = pd.Series(np.nan, index=df.index)
    Re = pd.Series(np.nan, index=df.index)
    Im = pd.Series(np.nan, index=df.index)
    Period = pd.Series(np.nan, index=df.index)
    SmoothPeriod = pd.Series(np.nan, index=df.index)
    Phase = pd.Series(np.nan, index=df.index)

    for i in range(6, len(df)):
        # Calculate Smooth
        Smooth.iloc[i] = (4 * price.iloc[i] + 3 * price.iloc[i - 1] + 2 * price.iloc[i - 2] + price.iloc[i - 3]) / 10

        # Calculate Detrender
        Detrender.iloc[i] = (0.0962 * Smooth.iloc[i] + 0.5769 * Smooth.iloc[i - 2] - 0.5769 * Smooth.iloc[i - 4] - 0.0962 * Smooth.iloc[i - 6]) * (0.075 * Period.iloc[i - 1] + 0.54)

        # Calculate Q1
        Q1.iloc[i] = (0.0962 * Detrender.iloc[i] + 0.5769 * Detrender.iloc[i - 2] - 0.5769 * Detrender.iloc[i - 4] - 0.0962 * Detrender.iloc[i - 6]) * (0.075 * Period.iloc[i - 1] + 0.54)

        # Calculate I1
        I1.iloc[i] = Detrender.iloc[i - 3]

        # Calculate jI and jQ
        jI.iloc[i] = (0.0962 * I1.iloc[i] + 0.5769 * I1.iloc[i - 2] - 0.5769 * I1.iloc[i - 4] - 0.0962 * I1.iloc[i - 6]) * (0.075 * Period.iloc[i - 1] + 0.54)
        jQ.iloc[i] = (0.0962 * Q1.iloc[i] + 0.5769 * Q1.iloc[i - 2] - 0.5769 * Q1.iloc[i - 4] - 0.0962 * Q1.iloc[i - 6]) * (0.075 * Period.iloc[i - 1] + 0.54)

        # Calculate I2 and Q2
        I2.iloc[i] = I1.iloc[i] - jQ.iloc[i]
        Q2.iloc[i] = Q1.iloc[i] + jI.iloc[i]

        # Smooth I2 and Q2
        I2.iloc[i] = 0.2 * I2.iloc[i] + 0.8 * I2.iloc[i - 1]
        Q2.iloc[i] = 0.2 * Q2.iloc[i] + 0.8 * Q2.iloc[i - 1]

        # Calculate Re and Im
        Re.iloc[i] = I2.iloc[i] * I2.iloc[i - 1] + Q2.iloc[i] * Q2.iloc[i - 1]
        Im.iloc[i] = I2.iloc[i] * Q2.iloc[i - 1] - Q2.iloc[i] * I2.iloc[i - 1]

        # Smooth Re and Im
        Re.iloc[i] = 0.2 * Re.iloc[i] + 0.8 * Re.iloc[i - 1]
        Im.iloc[i] = 0.2 * Im.iloc[i] + 0.8 * Im.iloc[i - 1]

        # Calculate Period
        if Im.iloc[i] != 0 and Re.iloc[i] != 0:
            period_calc = 2 * PI / math.atan(Im.iloc[i] / Re.iloc[i])
        else:
            period_calc = Period.iloc[i - 1] if i - 1 >= 0 else 0

        # Constraints on Period
        period_calc = max(min(period_calc, 1.5 * Period.iloc[i - 1]), 0.67 * Period.iloc[i - 1]) if i - 1 >= 0 else period_calc
        period_calc = max(min(period_calc, 50), 6)
        Period.iloc[i] = 0.2 * period_calc + 0.8 * (Period.iloc[i - 1] if i - 1 >= 0 else 0)

        # Smooth Period
        SmoothPeriod.iloc[i] = 0.33 * Period.iloc[i] + 0.67 * (SmoothPeriod.iloc[i - 1] if i - 1 >= 0 else 0)

        # Calculate Phase
        if I1.iloc[i] != 0:
            Phase.iloc[i] = math.atan(Q1.iloc[i] / I1.iloc[i]) * 180 / PI
        else:
            Phase.iloc[i] = Phase.iloc[i - 1] if i - 1 >= 0 else 0

        # Calculate DeltaPhase
        DeltaPhase = Phase.iloc[i - 1] - Phase.iloc[i] if i - 1 >= 0 else 0
        DeltaPhase = max(DeltaPhase, 1)

        # Calculate alpha
        alpha = fast / DeltaPhase
        alpha = max(min(alpha, fast), slow)

        # Update MAMA and FAMA
        MAMA_prev = MAMA.iloc[i - 1] if i - 1 >= 0 else price.iloc[i]
        MAMA.iloc[i] = alpha * price.iloc[i] + (1 - alpha) * MAMA_prev
        FAMA_prev = FAMA.iloc[i - 1] if i - 1 >= 0 else MAMA.iloc[i]
        FAMA.iloc[i] = 0.5 * alpha * MAMA.iloc[i] + (1 - 0.5 * alpha) * FAMA_prev

    return MAMA, FAMA

def calculate_rtd(df, fast=0.11, slow=0.06):
    """
    Calculates RTD (Realtime Trend Detection) using MESA.

    Args:
        df (pd.DataFrame): DataFrame containing price data.
        fast (float): Fast limit parameter.
        slow (float): Slow limit parameter.

    Returns:
        pd.DataFrame: DataFrame with added 'M_cur', 'F_cur', 'M_1', 'F_1', 'M_1x', 'F_1x' columns.
    """
    df = df.copy()

    # Current timeframe MESA
    M_cur, F_cur = get_mesa(df, src_in='Close', fast=fast, slow=slow)
    df['M_cur'] = M_cur
    df['F_cur'] = F_cur

    # Higher timeframe scaling factors (assuming '240' is higher timeframe, e.g., 4-hour)
    scale = 240 / 15  # Example scaling, adjust based on your timeframes
    scalex = 1440 / 15  # Example scaling for extra higher timeframe (e.g., daily)

    # Higher timeframe MESA
    M_1, F_1 = get_mesa(df, src_in='Close', fast=fast * scale, slow=slow * scale)
    df['M_1'] = M_1
    df['F_1'] = F_1

    # Extra higher timeframe MESA
    M_1x, F_1x = get_mesa(df, src_in='Close', fast=fast * scalex, slow=slow * scalex)
    df['M_1x'] = M_1x
    df['F_1x'] = F_1x

    # Determine trade action based on MESA comparisons
    df['tradeAction'] = np.where(df['M_1'] > df['M_1x'],
                                 "Realtime Trend Detection: Market in uptrend. LONGS ONLY.",
                                 "Realtime Trend Detection: Market in downtrend. SHORTS ONLY.")

    # Generate Signals
    df['RTD_Signal'] = np.where(df['M_1'] > df['M_1x'], 1, -1)

    return df

# src/indicators/rtd.py

if __name__ == "__main__":
    # Sample test
    import pandas as pd

    # Load sample data
    df_test = pd.read_csv('data/data_with_indicators.csv', parse_dates=['Date'])
    df_test = df_test.set_index('Date')

    # Calculate RTD
    df_test = calculate_rtd(df_test)

    # Save or plot to verify
    df_test[['M_cur', 'F_cur', 'M_1', 'F_1', 'M_1x', 'F_1x', 'tradeAction', 'RTD_Signal']].to_csv('data/data_with_rtd.csv')
    print(df_test[['M_cur', 'F_cur', 'M_1', 'F_1', 'M_1x', 'F_1x', 'tradeAction', 'RTD_Signal']].tail())