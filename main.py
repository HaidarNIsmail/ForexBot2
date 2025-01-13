from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access environment variables
mt5_path = os.getenv('MT5_PATH')
data_path = os.getenv('DATA_PATH')
mt5_login = os.getenv('MT5_LOGIN')
mt5_server = os.getenv('MT5_SERVER')
mt5_password = os.getenv('MT5_PASSWORD')

# Print values to verify they are loaded correctly
print("MT5_PATH:", mt5_path)
print("DATA_PATH:", data_path)
print("MT5_LOGIN:", mt5_login)
print("MT5_SERVER:", mt5_server)
print("MT5_PASSWORD:", mt5_password)