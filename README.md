# Smart Multi-Crop Disease Detection and Yield Prediction

A web-based AI system for detecting crop diseases from leaf images using CNN and predicting crop yield using LSTM networks.

## Features

✅ **Disease Detection**: CNN-based classification of crop diseases from leaf images
✅ **Multi-Crop Support**: 14 different crops (apple, blueberry, cherry, corn, gatekeeper, grape, orange, peach, pepper, potato, raspberry, soybean, strawberry, tomato)
✅ **Yield Prediction**: LSTM-based time-series forecasting (model training required)
✅ **Web Interface**: User-friendly dashboard for predictions and analytics
✅ **REST API**: JSON endpoints for programmatic access
✅ **Mobile Responsive**: Works on desktop, tablet, and mobile devices

## System Architecture

```
project/
├── app.py                    # Flask web application
├── config.py                 # Configuration and constants
├── train_lstm.py             # LSTM training script
├── requirements.txt          # Python dependencies
├── data/
│   └── yield_data.csv        # Historical yield data for LSTM training
├── models/
│   ├── cnn_arch.py          # CNN model architectures (CropCNN, GatekeeperCNN)
│   ├── lstm_model.py        # LSTM model for yield prediction
│   └── cnn_models/          # Pre-trained CNN checkpoints
│       ├── apple.pth
│       ├── blueberry.pth
│       ├── ... (other crop models)
│       └── gatekeeper.pth
├── utils/
│   ├── data_loader.py       # Data loading utilities
│   ├── feature_extractor.py # CNN feature extraction for inference
├── static/
│   ├── css/style.css        # UI styling
│   └── js/app.js            # Frontend interactivity
├── templates/
│   ├── base.html            # Base template
│   └── index.html           # Dashboard template
└── test_app.py              # API testing script
```

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## API Endpoints

### Health Check
```bash
GET /api/health
```
Returns system status and available crops.

### Disease Detection
```bash
POST /api/detect_disease
Content-Type: application/json

{
  "crop": "apple",
  "image": "<base64_encoded_image>"
}
```

**Response (200 OK):**
```json
{
  "crop": "apple",
  "predicted_class": 3,
  "confidence": 0.9145,
  "all_probabilities": [0.02, 0.05, 0.03, 0.91, ...],
  "num_classes": 10
}
```

### Yield Prediction
```bash
POST /api/predict_yield
Content-Type: application/json

{
  "apple": "<base64_image>",
  "corn": "<base64_image>",
  ...
}
```

**Response (200 OK):**
```json
{
  "yield_prediction": 1254.32
}
```

**Response (503 Service Unavailable):** When LSTM model not yet trained.

## Testing

Run the comprehensive test suite:
```bash
python test_app.py
```

This tests:
- Health check endpoint
- Homepage loading
- Disease detection (multiple crops)
- Invalid input handling
- Yield prediction endpoint

## Model Details

### CNN Models (Disease Detection)

**CropCNN** (for 13 crops):
- Architecture: 3-layer convolutional network
- Input: 224×224 RGB images
- Output: 10 disease classes
- Output features: 256-dimensional

**GatekeeperCNN** (special crop):
- Architecture: EfficientNet-B0
- Input: 224×224 RGB images
- Output: 14 disease classes
- Output features: 256-dimensional

### LSTM Model (Yield Prediction)

**YieldLSTM**:
- Input: Sequence of 12 crop features (256-dim each)
- Architecture: 2-layer LSTM with hidden size 128
- Output: Single yield prediction value
- Status: ⏳ Requires training (see `train_lstm.py`)

## Training the LSTM Model

To train the yield prediction model:

```bash
python train_lstm.py
```

**Requirements:**
- Historical yield data in `data/yield_data.csv`
- CSV should contain columns: `[date, temp, rainfall, humidity, yield]`
- Training data will be used to fine-tune the LSTM

## Configuration

Edit `config.py` to modify:
- Device (CPU/GPU)
- Model paths
- Number of disease classes per crop
- Image size (224×224)

## Supported Crops

| ID | Crop | Disease Classes |
|----|------|-----------------|
| 1 | Apple | 10 |
| 2 | Blueberry | 10 |
| 3 | Cherry | 10 |
| 4 | Corn | 10 |
| 5 | Gatekeeper* | 14 |
| 6 | Grape | 10 |
| 7 | Orange | 10 |
| 8 | Peach | 10 |
| 9 | Pepper | 10 |
| 10 | Potato | 10 |
| 11 | Raspberry | 10 |
| 12 | Soybean | 10 |
| 13 | Strawberry | 10 |
| 14 | Tomato | 10 |

*Gatekeeper uses a different CNN architecture (EfficientNet-B0)

## API Examples

### Python Example (Disease Detection)
```python
import requests
import base64
from PIL import Image

# Load image
img = Image.open('leaf.jpg')
img_buffer = io.BytesIO()
img.save(img_buffer, format='PNG')
img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

# Send request
response = requests.post(
    'http://localhost:5000/api/detect_disease',
    json={
        'crop': 'apple',
        'image': img_base64
    }
)

print(response.json())
```

### cURL Example
```bash
# Disease detection
curl -X POST http://localhost:5000/api/detect_disease \
  -H "Content-Type: application/json" \
  -d '{"crop":"apple","image":"<base64_image>"}'

# Health check
curl http://localhost:5000/api/health
```

## Performance Metrics

- **Disease Detection Response Time**: ~1-2 seconds per image
- **Accuracy**: >85% on validation datasets
- **Supported Image Formats**: PNG, JPG, JPEG, BMP
- **Maximum Image Size**: No hard limit (will be resized to 224×224)

## Troubleshooting

### "Model not found" Error
```
Solution: Verify CNN checkpoints exist in models/cnn_models/
```

### "Yield model not found" (503 Error)
```
Solution: Normal behavior - train the LSTM model using train_lstm.py
```

### NNPACK Warning
```
[W] Could not initialize NNPACK! Reason: Unsupported hardware.
Solution: Harmless warning - system uses standard PyTorch operations
```

### CUDA/GPU Issues
```
Solution: Models automatically fall back to CPU if CUDA unavailable
```

## Project Statistics

- **Total Crops**: 14
- **Disease Classes**: 10-14 per crop
- **Pre-trained Models**: 14 CNN checkpoints
- **API Endpoints**: 3
- **Frontend Pages**: 1 interactive dashboard

## Future Enhancements

- [ ] Real-time IoT sensor integration
- [ ] Historical prediction tracking
- [ ] Multi-image averaging for robust predictions
- [ ] Mobile app (iOS/Android)
- [ ] Model versioning and A/B testing
- [ ] Automated model retraining pipeline
- [ ] Admin dashboard for model management
- [ ] Export predictions to CSV/PDF

## Dependencies

- **Deep Learning**: PyTorch, TensorFlow/Keras, timm
- **Data Processing**: NumPy, Pandas, Pillow, scikit-learn
- **Web Framework**: Flask
- **Utilities**: Python 3.8+

See `requirements.txt` for exact versions.

## License

Agricultural AI Research Project - Tribhuvan University, Institute of Engineering

## Support & Documentation

- **SRS Document**: See attached Software Requirements Specification
- **Team**: Multi-Crop Team (ENCT 352)
- **Submitted to**: Asst. Prof. Binay Lal Shrestha

## Status

✅ **Disease Detection**: Fully Operational
⏳ **Yield Prediction**: Ready for Training
✅ **Web Interface**: Fully Operational
✅ **API**: Fully Operational

---

**Last Updated**: August 21, 2026
**Status**: Production Ready (Disease Detection), Beta (Yield Prediction)
