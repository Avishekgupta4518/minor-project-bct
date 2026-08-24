#!/usr/bin/env python
# test_app.py - Smoke test for the Smart Multi-Crop application.
# Starts the Flask dev server in a background thread, then exercises the API.

import base64
import re
import sys
import threading
import time
import traceback
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))

from app import app

BASE_URL = "http://127.0.0.1:5000"
CSRF_PATTERN = re.compile(r'<meta name="csrf-token" content="([^"]+)"')


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
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False, threaded=True)


def new_session():
    """
    Create a requests session with a valid CSRF token.

    The server rejects token-less POSTs (403), so first fetch the homepage,
    which sets the session cookie and embeds the token in a meta tag.
    """
    session = requests.Session()
    response = session.get(f"{BASE_URL}/", timeout=30)
    match = CSRF_PATTERN.search(response.text)
    if not match:
        raise RuntimeError("Could not find CSRF token on the homepage.")
    session.headers.update({"X-CSRF-Token": match.group(1)})
    return session


def test_api():
    """Test API endpoints"""
    print("\n" + "=" * 60)
    print("Testing Smart Multi-Crop API")
    print("=" * 60)

    time.sleep(3)  # Wait for server to start

    # Test 1: Health check
    print("\n[Test 1] Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
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

    # Test 2: Homepage + CSRF session
    print("\n[Test 2] Homepage & CSRF session")
    client = None
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print(f"✓ Homepage loaded successfully")
            print(f"  HTML length: {len(response.text)} characters")
        else:
            print(f"✗ Homepage failed: {response.status_code}")
        client = new_session()
        print("✓ CSRF session established")
    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return

    img_base64 = image_to_base64(create_test_image())

    # Test 3: Disease detection (apple)
    print("\n[Test 3] Disease Detection (Apple)")
    try:
        payload = {"crop": "apple", "image": img_base64}
        response = client.post(f"{BASE_URL}/api/detect_disease", json=payload)
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
        traceback.print_exc()

    # Test 4: Gatekeeper auto-detection pipeline
    print("\n[Test 4] Gatekeeper Auto-Detection")
    try:
        payload = {"crop": "auto", "image": img_base64}
        response = client.post(f"{BASE_URL}/api/detect_disease", json=payload)
        if response.status_code == 200:
            data = response.json()
            routing = data.get("gatekeeper", {})
            print(f"✓ Gatekeeper routing successful")
            print(f"  Detected crop: {routing.get('predicted_crop')}")
            print(f"  Routing confidence: {routing.get('confidence'):.4f}")
            print(f"  Disease model used: {data['crop']}")
            print(f"  Predicted label: {data['predicted_label']}")
        else:
            print(f"✗ Gatekeeper auto-detection failed: {response.status_code}")
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()

    # Test 5: Invalid crop is rejected
    print("\n[Test 5] Disease Detection (Invalid crop)")
    try:
        payload = {"crop": "invalid_crop", "image": img_base64}
        response = client.post(f"{BASE_URL}/api/detect_disease", json=payload)
        if response.status_code == 400:
            print(f"✓ Correctly rejected invalid crop")
            print(f"  Response: {response.json()['error']}")
        else:
            print(f"✗ Expected 400 error, got {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 6: Token-less POST is rejected by CSRF protection
    print("\n[Test 6] CSRF Protection")
    try:
        payload = {"crop": "apple", "image": img_base64}
        response = requests.post(f"{BASE_URL}/api/detect_disease", json=payload)
        if response.status_code == 403:
            print(f"✓ Token-less POST correctly rejected")
        else:
            print(f"✗ Expected 403 error, got {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 7: Place-only rice yield prediction
    print("\n[Test 7] Rice Yield Prediction")
    try:
        payload = {"place": "jhapa"}
        response = client.post(f"{BASE_URL}/api/predict_yield", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Rice yield prediction successful")
            print(f"  Predicted yield: {data['yield_prediction']} t/ha")
            print(f"  Based on: {data['based_on_years']} years (latest {data['last_record_year']})")
        else:
            print(f"✗ Yield prediction failed: {response.status_code}")
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 8: Unsupported place is rejected
    print("\n[Test 8] Invalid place")
    try:
        payload = {"place": "atlantis"}
        response = client.post(f"{BASE_URL}/api/predict_yield", json=payload)
        if response.status_code == 400 and "Unknown place" in response.json().get("error", ""):
            print("✓ Correctly rejected unsupported place")
        else:
            print(f"✗ Unexpected response: {response.status_code} {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60 + "\n")


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
        traceback.print_exc()
