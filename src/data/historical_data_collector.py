import pandas as pd
import MetaTrader5 as mt5
from Config.config import Config
import os

def collect_historical_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_H1, n=10000):
    login = int(Config.MT5_LOGIN)
    server = Config.MT5_SERVER
    password = Config.MT5_PASSWORD

    if not mt5.initialize(path=Config.MT5_PATH, login=login, server=server, password=password):
        print(f"initialize() failed, check .env and MT5 connection. Error: {mt5.last_error()}")
        mt5.shutdown()
        return None

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    mt5.shutdown()

    if rates is None:
        print(f"Failed to retrieve data for {symbol}. Check MT5 connection and symbol. Error: {mt5.last_error()}")
        return None

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)

    # Ensure required columns are present
    required_columns = ['open', 'high', 'low', 'close', 'tick_volume']
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        print(f"Warning: Missing columns in the collected data: {', '.join(missing_cols)}")

    return df

if __name__ == "__main__":
    # Define the directory path for saving data
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

    # Create the directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Define the full file path for saving data
    full_data_path = os.path.join(data_dir, 'EURUSD.csv')

    data = collect_historical_data()
    if data is not None:
        data.to_csv(full_data_path, index=True)
        print(f"Historical data saved to {full_data_path}")
    else:
        print("Failed to collect and save historical data.")