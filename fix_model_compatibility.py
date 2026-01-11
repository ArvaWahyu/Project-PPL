import h5py
import json
import os

model_path = 'mobilenetv2_daun.h5'
backup_path = 'mobilenetv2_daun_backup.h5'

if not os.path.exists(model_path):
    print("Model file not found.")
    exit(1)

# Create backup
import shutil
shutil.copyfile(model_path, backup_path)
print(f"Backup created at {backup_path}")

try:
    with h5py.File(model_path, 'r+') as f:
        if 'model_config' in f.attrs:
            config_str = f.attrs['model_config']
            
            # Handle bytes vs string
            if isinstance(config_str, bytes):
                config_str = config_str.decode('utf-8')
            
            # Check if incompatible key exists
            if 'batch_shape' in config_str:
                print("Found incompatible 'batch_shape' in config. Patching to 'batch_input_shape'...")
                
                # Replace the key
                new_config_str = config_str.replace('"batch_shape":', '"batch_input_shape":')
                
                # Write back
                f.attrs['model_config'] = new_config_str.encode('utf-8')
                print("Successfully patched model config!")
            else:
                print("No 'batch_shape' found. Model might already be compatible or have a different issue.")
        else:
            print("No 'model_config' attribute found in H5 file.")

    # Verification attempt
    from tensorflow.keras.models import load_model
    try:
        print("Verifying model load...")
        model = load_model(model_path)
        print("VERIFICATION SUCCESS: Model loaded with TensorFlow 2.12!")
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")

except Exception as e:
    print(f"An error occurred during patching: {e}")
    # Restore backup
    shutil.copyfile(backup_path, model_path)
    print("Restored original file from backup.")
