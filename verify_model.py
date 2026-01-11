import os
import numpy as np
import tensorflow as tf
from app import model, CLASS_NAMES, preprocess_image
from PIL import Image

def test_model():
    print("="*50)
    print("VERIFICATION STARTED")
    print("="*50)

    # 1. Verify Model Loaded
    if model is None:
        print("[FAIL] Model failed to load.")
        return
    else:
        print("[PASS] Model object exists.")

    # 2. Verify Input Shape
    input_shape = model.input_shape
    print(f"Model Input Shape: {input_shape}")
    if input_shape[1:3] == (224, 224):
        print("[PASS] Model input shape is correct (224x224).")
    else:
        print(f"[WARN] Model input shape mismatch: {input_shape}")

    # 3. Verify Output Shape (Should be 8 classes)
    output_shape = model.output_shape
    print(f"Model Output Shape: {output_shape}")
    expected_classes = 8
    if output_shape[-1] == expected_classes:
        print(f"[PASS] Model output shape is correct ({expected_classes} classes).")
    else:
        print(f"[FAIL] Model output shape mismatch. Expected {expected_classes}, got {output_shape[-1]}")

    # 4. Verify Class Names
    print(f"Registered Classes in app.py: {len(CLASS_NAMES)}")
    if len(CLASS_NAMES) == expected_classes:
        print("[PASS] Class list length matches model output.")
    else:
        print(f"[FAIL] Class list length mismatch. App has {len(CLASS_NAMES)}, model has {expected_classes}.")

    # 5. Test Inference with Dummy Image
    print("\nTesting Inference...")
    try:
        # Create a dummy image
        dummy_img = Image.new('RGB', (300, 300), color='green')
        dummy_path = 'temp_test_leaf.jpg'
        dummy_img.save(dummy_path)

        # Preprocess
        processed = preprocess_image(dummy_path)
        
        # Predict
        preds = model.predict(processed)
        print(f"Raw Predictions: {preds}")
        
        confidence = np.max(preds) * 100
        class_idx = np.argmax(preds)
        predicted_label = CLASS_NAMES[class_idx]
        
        print(f"Predicted Class Index: {class_idx}")
        print(f"Predicted Label: {predicted_label}")
        print(f"Confidence: {confidence:.2f}%")
        
        print("[PASS] Inference successful.")
        
        # Cleanup
        if os.path.exists(dummy_path):
            os.remove(dummy_path)
            
    except Exception as e:
        print(f"[FAIL] Inference failed: {e}")
        import traceback
        traceback.print_exc()

    print("="*50)
    print("VERIFICATION COMPLETED")
    print("="*50)

if __name__ == "__main__":
    test_model()
