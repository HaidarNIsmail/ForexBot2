import os
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from dotenv import load_dotenv
from forex_env import ForexTradingEnv

# Load environment variables
load_dotenv()

# Paths
data_path = os.getenv("DATA_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/output/EURUSD_with_indicators.csv")
model_save_path = os.getenv("MODEL_SAVE_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/models/ppo_forex_model.zip")
log_path = os.getenv("LOG_PATH", "C:/Users/haida/PycharmProjects/ForexBot2/logs")
timesteps = int(os.getenv("TIMESTEPS", 100000))
learning_rate = float(os.getenv("LEARNING_RATE", 3e-4))

try:
    # Load and validate data
    print("Loading dataset...")
    data = pd.read_csv(data_path)
    print("Dataset loaded. Preview:")
    print(data.head())

    # Drop non-numeric columns
    print("Dropping non-numeric columns...")
    data = data.select_dtypes(include=['float64', 'int64'])
    print(f"Columns retained: {list(data.columns)}")

    # Handle NaN values
    print("Handling NaN values...")
    data.fillna(method='ffill', inplace=True)
    data.fillna(method='bfill', inplace=True)
    print("NaN values handled.")

    # Pad data to match observation requirements
    print("Padding data...")
    required_features = 24
    current_features = data.shape[1]
    if current_features < required_features:
        padding = required_features - current_features
        for i in range(padding):
            data[f'padding_{i+1}'] = 0
    print(f"Data padded to {required_features} features.")

    # Initialize environment
    print("Initializing ForexTrading environment...")
    env = DummyVecEnv([lambda: ForexTradingEnv(data=data, window_size=10)])
    print("Environment initialized successfully.")

    # Set up PPO model
    print("Setting up PPO model...")
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=learning_rate, tensorboard_log=log_path)

    # Add a checkpoint callback
    checkpoint_callback = CheckpointCallback(save_freq=10000, save_path=os.path.dirname(model_save_path), name_prefix="ppo_checkpoint")

    # Start training
    print("Starting training...")
    model.learn(total_timesteps=timesteps, callback=checkpoint_callback)
    print("Training completed.")

    # Save the model
    print("Saving the trained model...")
    model.save(model_save_path)
    print(f"Model saved at {model_save_path}")

except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
































