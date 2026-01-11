import os
import sys

print(f"Python Version: {sys.version}")

try:
    import tensorflow as tf
    print(f"TensorFlow Version: {tf.__version__}")
except ImportError as e:
    print(f"TensorFlow Import Error: {e}")

try:
    import keras
    print(f"Keras Version: {keras.__version__}")
except ImportError as e:
    print(f"Keras Import Error: {e}")

model_path = 'mobilenetv2_daun.h5'

if not os.path.exists(model_path):
    print(f"ERROR: File {model_path} not found!")
    sys.exit(1)

print(f"Attempting to load model from {model_path}...")

try:
    # Try loading with tf.keras first (Standard for TF 2.x)
    try:
        from tensorflow.keras.models import load_model
        print("Using tensorflow.keras.models.load_model")
        model = load_model(model_path)
    except Exception as e1:
        print(f"Failed with tensorflow.keras: {e1}")
        print("Trying standalone keras...")
        from keras.models import load_model
        model = load_model(model_path)
    
    print("SUCCESS: Model loaded successfully!")
    model.summary()
except Exception as e:
    print("\n" + "="*50)
    print("FAILED TO LOAD MODEL")
    print("="*50)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
    import traceback
    traceback.print_exc()
    print("="*50 + "\n")
