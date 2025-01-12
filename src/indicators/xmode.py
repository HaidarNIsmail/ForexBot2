import math
import pandas as pd
import numpy as np

def xmode_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Translates the core numeric logic from your Pine Script X-Mode approach into Python.
    Returns a DataFrame with the 'Signal' and 'Positions' columns (and optional debug columns).
    """

    # We copy to avoid modifying the original df in place.
    df = df.copy()

    # -----------------------
    # 1) Expose the columns you need from your DF (Close, High, Low)
    #    since your code references them frequently:
    #    In your snippet, you had `high, low, open, close`.
    #    We'll assume your Pandas DataFrame columns are "High", "Low", "Open", "Close".

    # If your snippet references other transformations (like ignoring wicks, or adjusting hi/lo),
    # handle that logic here. For example:
    #    uPrice = df["High"]  # if not ignoring wicks
    #    lPrice = df["Low"]

    uPrice = df["High"]
    lPrice = df["Low"]

    # -----------------------
    # 2) Example: We'll replicate part of your logic for a single lookback,
    #    e.g. "lookback = 128" from your snippet.
    #    This is a placeholder.  You can replicate multiple sets
    #    (like lookback1, lookback2, etc.) if you want to calculate more zones.

    lookback = 128

    # Compute vLow, vHigh (lowest, highest price over lookback bars)
    df["vLow"] = lPrice.rolling(lookback).min()
    df["vHigh"] = uPrice.rolling(lookback).max()
    df["vDist"] = df["vHigh"] - df["vLow"]  # might be used in your code

    # Example SHIFT logic: if vLow < 0, we do some shift
    # We'll store a boolean or numeric for SHIFT.
    # In Pine, shift = vLow < 0 ? true : false
    df["shift"] = (df["vLow"] < 0)

    # Next, we replicate some of the scale logic from your snippet:
    # e.g., sfVar = math.log(0.4 * tmpHigh) / logTen - math.floor(...)
    # We'll define a function that does these calculations row by row.
    # This is a minimal partial example.

    logTen = math.log(10)
    logEight = math.log(8)

    def xmode_calc_row(row):
        """
        For each row, replicate the scale calculations from your snippet
        to produce final lines or zones.  We'll do a minimal example.
        """
        vLow_val = row["vLow"]
        vHigh_val = row["vHigh"]
        # skip if missing data
        if pd.isna(vLow_val) or pd.isna(vHigh_val):
            return np.nan, np.nan  # can't calc

        # We'll replicate: tmpHigh = ...
        tmpHigh = vHigh_val  # ignoring negative shift logic for now
        tmpLow = vLow_val

        # partial example: let's define a single zone = midpoint
        zone_mid = (tmpHigh + tmpLow)/2.0
        # we could do more advanced lines like "ZeroEight" = absTop - 11*Increment, etc.
        # But let's keep it short for demonstration.

        # We'll return the zone.
        # If you want multiple lines, return them as well, e.g. (zone_mid, zone_top, zone_bottom)
        return zone_mid, 0.0

    df[["xmode_zone", "dummy_col"]] = df.apply(xmode_calc_row, axis=1, result_type="expand")

    # -----------------------
    # 3) Generate a final "Signal" using the zone we computed:
    #    For instance: if Close > xmode_zone => buy, else sell
    df["Signal"] = np.where(df["Close"] > df["xmode_zone"], 1.0, -1.0)

    # Then compute "Positions" from changes in "Signal" (like your standard approach).
    df["Positions"] = df["Signal"].diff()
    df["Positions"] = df["Positions"].replace({2.0: 1.0, -2.0: -1.0}).fillna(0.0)

    return df

# Optional debug run
if __name__ == "__main__":
    import os

    data_path = os.path.join(os.path.dirname(__file__), "..","..","data","data_with_indicators.csv")
    try:
        df_in = pd.read_csv(data_path, index_col="time")
        df_out = xmode_strategy(df_in)
        print(df_out[["Close","xmode_zone","Signal","Positions"]].tail(50))
    except FileNotFoundError:
        print(f"Data not found at {data_path}")
    except Exception as e:
        print("Error in xmode_strategy:", e)