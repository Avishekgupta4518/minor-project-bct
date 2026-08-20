# app.py
from flask import Flask, request, jsonify, render_template
import torch
from pathlib import Path
from models.lstm_model import YieldLSTM
from utils.feature_extractor import FeatureExtractor
from config import DEVICE, LSTM_MODEL_PATH, CROP_NAMES
import base64
from PIL import Image
import io

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load LSTM model
lstm_model = YieldLSTM(input_size=256, hidden_size=128, num_layers=2).to(DEVICE)
yield_model_ready = Path(LSTM_MODEL_PATH).exists()
if yield_model_ready:
    lstm_model.load_state_dict(torch.load(LSTM_MODEL_PATH, map_location=DEVICE))
    lstm_model.eval()
else:
    app.logger.warning("Yield model checkpoint not found at %s. /predict_yield will return 503 until the model is trained.", LSTM_MODEL_PATH)

# Feature extractor
feature_extractor = FeatureExtractor()

@app.route('/')
def index():
    """Home page - dashboard"""
    return render_template('index.html', crops=CROP_NAMES, yield_model_ready=yield_model_ready)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'yield_model_ready': yield_model_ready,
        'device': DEVICE,
        'crops': CROP_NAMES
    })

@app.route('/api/detect_disease', methods=['POST'])
def detect_disease():
    """
    Detect disease for a specific crop from an uploaded image.
    
    Expected JSON:
    {
        "crop": "apple",
        "image": "<base64_encoded_image>"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        crop_name = data.get('crop')
        image_data = data.get('image')
        
        if not crop_name or not image_data:
            return jsonify({'error': 'Missing crop or image data'}), 400
        
        if crop_name not in CROP_NAMES:
            return jsonify({'error': f'Crop {crop_name} not supported. Supported crops: {CROP_NAMES}'}), 400
        
        # Decode base64 image
        try:
            img_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        except Exception as e:
            return jsonify({'error': f'Invalid image data: {str(e)}'}), 400
        
        # Detect disease
        result = feature_extractor.detect_disease(crop_name, image)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/predict_yield', methods=['POST'])
def predict_yield():
    """
    Predict crop yield based on multiple crop leaf images.
    
    Expected JSON:
    {
        "apple": "<base64_image>",
        "corn": "<base64_image>",
        ...
    }
    """
    if not yield_model_ready:
        return jsonify({'error': 'Yield model checkpoint not found. Train the LSTM model first.'}), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400

        image_dict = {}
        for crop in CROP_NAMES:
            img_data = data.get(crop)
            if img_data:
                # Assume base64 encoded image
                try:
                    img_bytes = base64.b64decode(img_data)
                    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
                    image_dict[crop] = img
                except Exception as e:
                    return jsonify({'error': f'Invalid image for {crop}: {str(e)}'}), 400
            else:
                # Missing image -> use zero features later
                image_dict[crop] = None

        # Extract features
        features = feature_extractor.extract_features(image_dict)  # (1, 12, 256)
        features = features.to(DEVICE)

        # Predict yield
        with torch.no_grad():
            yield_pred = lstm_model(features).item()

        return jsonify({'yield_prediction': round(yield_pred, 2)}), 200
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)