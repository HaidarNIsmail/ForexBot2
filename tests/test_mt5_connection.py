import pytest
import MetaTrader5 as mt5
from Config.config import Config

def test_mt5_initialization():
    login = 52103207  # Replace with your actual MT5 login
    server = "ICMarketsSC-Demo"  # Replace with your broker's server name
    password = "1MsTz@B48J2LaB"        # Replace with your MT5 password

    print(f"Attempting MT5 initialization with path: {Config.MT5_PATH}, login: {login}, server: {server}")

    if not mt5.initialize(path=Config.MT5_PATH, login=login, server=server, password=password):
        print("MT5 initialization failed.")
        assert False, (
            f"MT5 initialization failed. Check .env and MT5 connection. "
            f"Path used: {Config.MT5_PATH}, login: {login}, server: {server}"
        )
    else:
        print("MT5 initialized successfully.")
        mt5.shutdown()
        # We use just 'assert True' with no extra string to avoid syntax issues in Python
        assert True







# login = 52103207
#         server = "ICMarketsSC-Demo"
#         password = "1MsTz@B48J2LaB"