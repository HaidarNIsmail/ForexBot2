import os
from dotenv import load_dotenv
import pathlib

# Determine the path to the .env file
config_file_directory = pathlib.Path(__file__).parent.resolve()
env_file = config_file_directory.parent / ".env"  # Assuming .env is in the project root

# Check if .env file exists
if not env_file.exists():
    with open(env_file, "w") as f:
        f.write("MT5_PATH=\nDATA_PATH=\nMT5_LOGIN=\nMT5_SERVER=\nMT5_PASSWORD=\n")
        print("Created .env file with template values. Please fill in your details in the .env file.")

# Load environment variables from .env file
load_dotenv(dotenv_path=env_file)


class Config:
    MT5_PATH = os.getenv("MT5_PATH")  # Correct usage
    DATA_PATH = os.getenv("DATA_PATH")  # Correct usage
    MT5_LOGIN = os.getenv("MT5_LOGIN")
    MT5_SERVER = os.getenv("MT5_SERVER") # Correct usage
    MT5_PASSWORD = os.getenv("MT5_PASSWORD") # Correct usage




# Debugging: Print loaded configuration
print("=== Configuration Loaded ===")
print(f"MT5_PATH: {Config.MT5_PATH}")
print(f"DATA_PATH: {Config.DATA_PATH}")
print(f"MT5_LOGIN: {Config.MT5_LOGIN}")
print(f"MT5_SERVER: {Config.MT5_SERVER}")
print(f"MT5_PASSWORD: {Config.MT5_PASSWORD}")

print("============================")