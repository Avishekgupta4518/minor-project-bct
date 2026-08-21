# Smart Multi-Crop Disease Detection and Yield Prediction

A web-based AI system for detecting crop diseases from leaf images using CNN and predicting crop yield using LSTM networks.

## Features

✅ **Disease Detection**: CNN-based classification of crop diseases from leaf images
✅ **Multi-Crop Support**: 14 different crops (apple, blueberry, cherry, corn, gatekeeper, grape, orange, peach, pepper, potato, raspberry, soybean, strawberry, tomato)
✅ **Yield Prediction**: Weather-based LSTM time-series forecasting
✅ **Web Interface**: User-friendly dashboard for predictions and analytics
✅ **REST API**: JSON endpoints for programmatic access
✅ **Mobile Responsive**: Works on desktop, tablet, and mobile devices
✅ **Authentication**: Farmer registration, login, logout, and role-aware access
✅ **Prediction History**: SQLite-backed disease and yield prediction records
✅ **Analyst/Admin Views**: History analysis and admin user-role management

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

## Run Everything on Windows

From PowerShell, run these commands from the project folder:

```powershell
cd C:\Users\Fix\Desktop\minor_project_bct\minor-project-bct
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in a browser. The trained weather LSTM checkpoint is already in `models/weather_lstm_yield.pth`.

Create an administrator account in a second PowerShell window:

```powershell
cd C:\Users\Fix\Desktop\minor_project_bct\minor-project-bct
.\.venv\Scripts\Activate.ps1
python create_admin.py
```

The application supports these workflows:

- Farmer: choose **Sign in**, create an account, run disease and yield predictions, then open **History**.
- Live yield weather: choose an agricultural region, click **Get Live Weather**, then click **Predict Yield**.
- Analyst: an administrator can change a farmer's role to `analyst`; the analyst can open **Analyst** and view all prediction results.
- Administrator: sign in to open **Admin**, **Dataset**, or **Models**. Uploaded datasets and model files are staged for review and are not activated automatically.

Run the smoke test in another terminal while the app is running:

```powershell
python test_app.py
```

Retrain the weather LSTM only when replacing the bundled dataset with real historical data:

```powershell
python train_lstm.py
```

## API Endpoints

### Health Check
```bash
GET /api/health
```
Returns system status and available crops.

### Authentication and History

- `GET/POST /register` creates a farmer account.
- `GET/POST /login` starts a session.
- `GET /logout` ends the session.
- `GET /history` shows a farmer's saved predictions; analysts and admins can review all saved results.
- `GET /analyst` opens the analyst history view.
- `GET /admin` opens system monitoring and user-role management for administrators.

Prediction history is stored in `data/smart_agriculture.db`. Set `DATABASE_PATH` to use another SQLite database and set `SECRET_KEY` in production.

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
  "predicted_label": "Apple__healthy",
  "confidence": 0.9145,
  "class_labels": ["Apple__Apple_scab", "Apple_Black_rot", "Apple_Cedar_apple_rust", "Apple__healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
  "all_probabilities": [0.02, 0.05, 0.03, 0.91, ...],
  "num_classes": 10
}
```

### Yield Prediction
```bash
POST /api/predict_yield
Content-Type: application/json

{
  "weather": {
    "temperature": 27,
    "rainfall": 185,
    "humidity": 72,
    "soil_moisture": 65
  }
}
```

**Response (200 OK):**
```json
{
  "yield_prediction": 8.52,
  "sequence_length": 12,
  "weather_features": ["temperature", "rainfall", "humidity", "soil_moisture"]
}
```

Use `/api/weather?place=chitwan` to retrieve a live 12-step forecast from Open-Meteo. Available agricultural regions include Kathmandu Valley, Chitwan, Jhapa, Morang, Rupandehi, Banke, Dang, Kailali, Bara, and Kaski. The frontend includes this live-weather flow and also supports manually measured weather values.

The disease selector includes an `Other (not supported)` option. It intentionally does not run an unrelated crop model when a trained model is unavailable.

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
- Input: Sequence of 12 weather steps with temperature, rainfall, humidity, and soil moisture
- Architecture: 2-layer LSTM with hidden size 64
- Output: Single yield prediction value
- Training data: `data/yield_data.csv` weather history and yield target

## Training the LSTM Model

To train the yield prediction model:

```bash
python train_lstm.py
```

**Requirements:**
- Historical yield data in `data/yield_data.csv`
- CSV should contain 12 monthly values for `temperature`, `rainfall`, `humidity`, and `soil_moisture`, plus `yield`
- Training data will be used to fine-tune the LSTM

The bundled demonstration data is synthetic and intentionally includes climate variation. Its current target range is approximately 5.93 to 7.61 tons/hectare. Training prints both validation RMSE and a mean-yield baseline; the LSTM should be compared against that baseline rather than judged from R-squared alone.

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

### Flask development server warning
```
WARNING: This is a development server. Do not use it in a production deployment.
```
This is expected when running `python app.py` locally. It is not an application error. Stop the server with `Ctrl+C`.

### Negative R-squared during LSTM training
R-squared can be negative when a validation split has little target variation or when the model is still learning. The training script now uses a fixed random seed, reports baseline RMSE, and saves the checkpoint by lowest validation RMSE. Replace the synthetic CSV with real historical weather/yield observations for meaningful production accuracy.

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
