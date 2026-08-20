#!/usr/bin/env python
# test_app.py - Test script for the Smart Multi-Crop application

import sys
import torch
import base64
from io import BytesIO
from PIL import Image
import requests
import threading
import time
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from app import app

def create_test_image(size=224):
    """Create a simple test image"""
    img = Image.new('RGB', (size, size), color=(73, 109, 137))
    return img

def image_to_base64(img):
    """Convert PIL image to base64 string"""
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def run_flask():
    """Run Flask app in background"""
    app.run(port=5000, debug=False, use_reloader=False, threaded=True)

def test_api():
    """Test API endpoints"""
    print("\n" + "="*60)
    print("Testing Smart Multi-Crop API")
    print("="*60)
    
    time.sleep(3)  # Wait for server to start
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n[Test 1] Health Check")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed")
            print(f"  Status: {data['status']}")
            print(f"  Yield model ready: {data['yield_model_ready']}")
            print(f"  Device: {data['device']}")
            print(f"  Supported crops: {len(data['crops'])}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Homepage
    print("\n[Test 2] Homepage")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✓ Homepage loaded successfully")
            print(f"  HTML length: {len(response.text)} characters")
        else:
            print(f"✗ Homepage failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Disease detection with test image
    print("\n[Test 3] Disease Detection (Apple)")
    try:
        test_img = create_test_image()
        img_base64 = image_to_base64(test_img)
        
        payload = {
            "crop": "apple",
            "image": img_base64
        }
        
        response = requests.post(f"{base_url}/api/detect_disease", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Disease detection successful")
            print(f"  Crop: {data['crop']}")
            print(f"  Predicted class: {data['predicted_class']}")
            print(f"  Confidence: {data['confidence']:.4f}")
            print(f"  Classes detected: {data['num_classes']}")
        else:
            print(f"✗ Disease detection failed: {response.status_code}")
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Disease detection - Gatekeeper
    print("\n[Test 4] Disease Detection (Gatekeeper)")
    try:
        test_img = create_test_image()
        img_base64 = image_to_base64(test_img)
        
        payload = {
            "crop": "gatekeeper",
            "image": img_base64
        }
        
        response = requests.post(f"{base_url}/api/detect_disease", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Disease detection successful")
            print(f"  Crop: {data['crop']}")
            print(f"  Predicted class: {data['predicted_class']}")
            print(f"  Confidence: {data['confidence']:.4f}")
            print(f"  Classes detected: {data['num_classes']}")
        else:
            print(f"✗ Disease detection failed: {response.status_code}")
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 5: Disease detection - Invalid crop
    print("\n[Test 5] Disease Detection (Invalid crop)")
    try:
        test_img = create_test_image()
        img_base64 = image_to_base64(test_img)
        
        payload = {
            "crop": "invalid_crop",
            "image": img_base64
        }
        
        response = requests.post(f"{base_url}/api/detect_disease", json=payload)
        if response.status_code == 400:
            print(f"✓ Correctly rejected invalid crop")
            print(f"  Response: {response.json()['error']}")
        else:
            print(f"✗ Expected 400 error, got {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 6: Yield prediction (should return 503 if model not trained)
    print("\n[Test 6] Yield Prediction")
    try:
        test_img = create_test_image()
        img_base64 = image_to_base64(test_img)
        
        payload = {
            "apple": img_base64,
            "corn": img_base64,
        }
        
        response = requests.post(f"{base_url}/api/predict_yield", json=payload)
        if response.status_code == 503:
            print(f"✓ Correctly returned 503 - Model not trained")
            print(f"  Message: {response.json()['error']}")
        elif response.status_code == 200:
            data = response.json()
            print(f"✓ Yield prediction successful")
            print(f"  Predicted yield: {data['yield_prediction']}")
        else:
            print(f"✗ Yield prediction failed: {response.status_code}")
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60 + "\n")

if __name__ == '__main__':
    # Start Flask in background thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()
    
    # Run tests
    try:
        test_api()
    except KeyboardInterrupt:
        print("\nTests interrupted")
    except Exception as e:
        print(f"\nTest error: {e}")
        import traceback
        traceback.print_exc()
