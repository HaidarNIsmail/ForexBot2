import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Load .env file with credentials
load_dotenv()


# Initialize MetaTrader 5 connection
def init_mt5():
    mt5.initialize()


def fetch_data(symbol, timeframe, n_bars):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_bars)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df


def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1)
    tr_max = tr.max(axis=1)
    atr = tr_max.rolling(window=period).mean()
    return atr


def place_order(symbol, volume, action, stop_loss=None, take_profit=None):
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 10
    request = {
        "action": action,  # 0 = buy, 1 = sell
        "symbol": symbol,
        "volume": volume,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": deviation,
        "type": 0,  # Market order
        "type_filling": 1,  # FOK
        "type_time": 0,  # GTC
        "expiration": 0,
        "comment": "Test order",
    }
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order failed: ", result)
    else:
        print("Order sent: ", result)


# Example main function for testing
def main():
    # Initialize MetaTrader 5
    init_mt5()

    # Fetch data for EURUSD
    symbol = "EURUSD"
    data = fetch_data(symbol, mt5.TIMEFRAME_M1, 1000)
    atr = calculate_atr(data)

    # Example: Use ATR for stop-loss and take-profit levels
    stop_loss = data['close'].iloc[-1] - 2 * atr.iloc[-1]  # 2x ATR for stop loss
    take_profit = data['close'].iloc[-1] + 2 * atr.iloc[-1]  # 2x ATR for take profit

    # Place a buy order with dynamic stop-loss and take-profit based on ATR
    place_order(symbol, 0.1, action=0, stop_loss=stop_loss, take_profit=take_profit)

    # Disconnect from MetaTrader 5
    mt5.shutdown()


if __name__ == "__main__":
    main()




