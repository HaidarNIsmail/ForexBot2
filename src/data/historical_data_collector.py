import pandas as pd
import MetaTrader5 as mt5
from Config.config import Config

def collect_historical_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_H1, n=10000):
    login = 52103207  # Replace if needed
    server = "ICMarketsSC-Demo"  # Replace if needed
    password = "1MsTz@B48J2LaB"  # Replace with your MT5 password

    if not mt5.initialize(path=Config.MT5_PATH, login=login, server=server, password=password):
        print(f"initialize() failed, check .env and MT5 connection. Error: {mt5.last_error()}")
        mt5.shutdown()
        return None

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)

    if rates is None:
        print(f"Failed to retrieve data for {symbol}. Check MT5 connection and symbol. Error: {mt5.last_error()}")
        mt5.shutdown()
        return None

    mt5.shutdown()

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df  # The return statement MUST be inside the function


if __name__ == "__main__":
    data = collect_historical_data()
    if data is not None:
        data.to_csv(Config.DATA_PATH, index=True)
        print(f"Historical data saved to {Config.DATA_PATH}")
    else:
        print("Failed to collect and save historical data")