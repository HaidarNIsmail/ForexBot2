import torch

# Define paths to the extracted RL model files
POLICY_PATH = r"C:/Users/haida/PycharmProjects/ForexBot2/models/ppo_forex_model/policy.pth"  # Update with your actual path
VARIABLES_PATH = r"C:/Users/haida/PycharmProjects/ForexBot2/models/ppo_forex_model/pytorch_variables.pth"  # Update with your actual path

def load_rl_policy():
    """
    Load the reinforcement learning policy.
    """
    print("Loading the RL policy...")
    policy = torch.load(POLICY_PATH)
    print("Policy loaded successfully.")
    return policy
