# AgriVision AI

**Smart Agriculture Platform for Plant Disease Detection and Crop Yield Prediction**

A deep learning-powered web application that identifies plant diseases from leaf images and predicts rice crop yield across Nepali districts, built as a minor project at Purwanchal University.

---

## Team Members

| Name | Roll No | GitHub |
|------|---------|--------|
| Aaditya Kumar Karna | PUR080BCT001 | [github.com/aadityakarna](https://github.com/aadityakarna) |
| Ankit Kumar Yadav | PUR080BCT016 | [github.com/ankitkumaradav](https://github.com/ankitkumaradav) |
| Avishek Kumar Gupta | PUR080BCT020 | [github.com/avishekgupta](https://github.com/Avishekgupta4518) |
| Hariom Raj Chauhan | PUR080BCT033 | [github.com/hariomchauhan](https://github.com/HariomRajChauhan) |

---

## About the Project

AgriVision AI is an intelligent agriculture assistant that combines computer vision and time-series forecasting to help farmers, analysts, and agricultural officers make data-driven decisions.

### Problem Statement

Agriculture is the backbone of Nepal's economy, employing over 60% of the population. However, farmers often lack access to timely and accurate tools for:
- Identifying crop diseases from leaf symptoms
- Predicting crop yield for planning and resource allocation

Manual disease identification requires expert knowledge and is prone to human error, while yield prediction traditionally relies on rough estimates rather than data-driven models.

### Our Solution

AgriVision AI addresses these challenges with two core ML pipelines:

#### 1. Plant Disease Detection (CNN-based)

A two-stage deep learning pipeline for automatic disease identification:

- **Stage 1 — Gatekeeper CNN**: A species classifier that first identifies which crop the leaf belongs to (apple, tomato, potato, corn, grape, etc.) from 13 supported species.
- **Stage 2 — Per-Crop Disease CNN**: Routes the image to a specialized disease classifier trained specifically for that crop, outputting the exact disease along with a confidence score and treatment recommendation.

The system is trained on the **PlantVillage dataset** and supports 13 crop species with **98+ disease classes** including healthy states.

**Supported Crops**: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Strawberry, Tomato

#### 2. Rice Yield Prediction (LSTM-based)

A Long Short-Term Memory (LSTM) neural network that predicts rice yield (in tonnes/hectare) for Nepali districts based on historical production data spanning multiple years. Users select a district from a dropdown and receive:
- Predicted yield for the upcoming season
- A 10-year historical trend chart
- Comparison with the district's average yield

### Key Features

- **Multi-crop disease detection** — Upload a leaf image and get instant diagnosis for 13 crop species
- **Rice yield forecasting** — District-level yield prediction with historical trends
- **Bilingual interface** — Full English and Nepali language support
- **Role-based access** — Farmer, Analyst, and Admin dashboards with distinct capabilities
- **Dark/Light mode** — Theme toggle with system preference detection
- **Responsive design** — Works across desktop, tablet, and mobile devices
- **Prediction history** — Track past disease detections and yield predictions
- **Admin panel** — Dataset management, model uploads, and user administration
- **CSV report export** — Download detection results for offline use

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Deep Learning** | PyTorch, torchvision, timm |
| **ML Models** | Custom CNN (disease detection), LSTM (yield prediction) |
| **Database** | SQLite |
| **Frontend** | HTML5, CSS3, JavaScript (vanilla) |
| **Charts** | Chart.js |
| **Deployment** | Docker, Railway |
| **Production Server** | Gunicorn |

---

## Project Structure

```
project/
├── app.py                    # Flask application (routes, auth, API endpoints)
├── config.py                 # Crop names, model paths, disease labels, recommendations
├── translations.py           # English and Nepali translations (172 keys)
├── wsgi.py                   # Production entry point (Gunicorn)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker build configuration
├── entrypoint.sh             # Container entrypoint script
├── railway.json              # Railway deployment config
├── models/
│   ├── cnn_arch.py           # CropCNN and GatekeeperCNN architectures
│   ├── lstm_model.py         # RiceYieldLSTM architecture
│   ├── cnn_models/           # 14 trained CNN model weights (.pth)
│   │   ├── gatekeeper.pth    # Species classifier
│   │   ├── apple.pth         # Per-crop disease classifiers
│   │   ├── tomato.pth
│   │   └── ...
│   ├── rice_yield_lstm.pth   # Trained LSTM model
│   └── rice_yield_meta.json  # LSTM metadata (normalization stats)
├── utils/
│   ├── database.py           # SQLite user/prediction storage
│   ├── feature_extractor.py  # Two-stage disease detection pipeline
│   ├── security.py           # CSRF protection, rate limiting, image validation
│   └── yield_pipeline.py     # Rice yield prediction pipeline
├── static/
│   ├── css/style.css         # Full design system with dark mode
│   └── js/
│       ├── app.js            # Client-side logic, theme toggle, UI interactions
│       ├── history.js         # Historical data charts
│       └── vendor/           # Chart.js library
├── templates/
│   ├── base.html             # Layout with sidebar, navigation, SVG sprite
│   ├── index.html            # Dashboard with disease detection and yield prediction
│   ├── auth.html             # Login and registration
│   ├── history.html          # Prediction history with charts
│   ├── admin.html            # Admin panel
│   ├── manage_dataset.html   # Dataset file management
│   ├── manage_models.html    # Model upload management
│   └── error.html            # Error page
└── data/
    ├── rice_yield_districts.csv  # Historical rice yield data
    └── smart_agriculture.db     # SQLite database (auto-created)
```

---

## Model Architecture

### Disease Detection CNN

Each per-crop model is a custom `CropCNN` based on a lightweight convolutional architecture:

- **Input**: 224x224 RGB leaf image (normalized with ImageNet stats)
- **Backbone**: Conv2d layers with BatchNorm and ReLU
- **Classifier**: Dropout + Linear to num disease classes per crop
- **Output**: Disease class probabilities with confidence score

The `GatekeeperCNN` follows the same architecture but is trained on 14 plant species to first route images to the correct crop model.

### Rice Yield LSTM

- **Architecture**: 2-layer LSTM with hidden size 64
- **Input**: Normalized historical yield sequence (10 years)
- **Output**: Predicted yield in tonnes/hectare
- **Validation MAE**: ~0.234 t/ha

---

## Setup and Installation

### Prerequisites

- Python 3.11 or higher
- pip
- Git

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/your-username/agrivision-ai.git
cd agrivision-ai
```

2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

The app starts at `http://localhost:5000`.

5. **Create an admin account**

```bash
python create_admin.py
```

### Docker Setup

```bash
docker build -t agrivision-ai .
docker run -p 5000:5000 agrivision-ai
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes (production) | Flask secret key for session management |
| `PORT` | No | Server port (default: 5000, Railway sets automatically) |

---

## Deployment (Railway)

The application is configured for one-click deployment on Railway:

1. Push to GitHub
2. Connect the repository on [railway.app](https://railway.app)
3. Railway auto-detects the Dockerfile and builds
4. Add `SECRET_KEY` in Railway Variables
5. Generate a public domain in Networking settings

See `Dockerfile` and `railway.json` for the deployment configuration.

---

## How It Works

### Disease Detection Flow

```
User uploads leaf image
        |
        v
   Gatekeeper CNN  -->  Identifies crop species (14 classes)
        |
        v
   Per-crop CNN    -->  Classifies disease (e.g., Tomato_Bacterial_spot)
        |
        v
   Returns: disease name, confidence, probability bars, treatment advice
```

### Yield Prediction Flow

```
User selects district from dropdown
        |
        v
   LSTM Model loads historical yield data for that district
        |
        v
   Predicts next-season yield (t/ha)
        |
        v
   Returns: predicted yield, 10-year trend chart, comparison stats
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard (disease detection + yield prediction) |
| GET/POST | `/login` | User login |
| GET/POST | `/register` | User registration |
| GET | `/logout` | Logout |
| GET | `/history` | Prediction history with charts |
| POST | `/api/detect_disease` | Disease detection API |
| POST | `/api/predict_yield` | Rice yield prediction API |
| GET | `/api/health` | Health check endpoint |
| GET | `/api/csrf-token` | CSRF token for AJAX requests |
| GET | `/admin` | Admin panel (admin only) |
| GET | `/admin/dataset` | Dataset management (admin only) |
| GET | `/admin/models` | Model management (admin only) |
| GET | `/analyst` | Analyst dashboard |

---

## License

This project is developed as an academic minor project at Purwanchal University. All rights reserved.

---

*Built with PyTorch, Flask, and a passion for smart agriculture.*
