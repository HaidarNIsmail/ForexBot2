import tensorflow as tf

def load_model():
    """
    Load the trained TensorFlow model for backtesting.
    """
    model_path = r"C:/Users/haida/PycharmProjects/ForexBot2/models/trained_model.h5"  # Update the path if necessary
    try:
        print(f"Attempting to load model from {model_path}")
        model = tf.keras.models.load_model(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}. Please check the path.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while loading the model: {e}")
        raise

