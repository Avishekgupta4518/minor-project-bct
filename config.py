# config.py
from pathlib import Path

import torch


# ============================================================
# CROP / MODEL NAMES
# ============================================================

CROP_NAMES = [
    'apple',
    'blueberry',
    'cherry',
    'corn',
    'gatekeeper',
    'grape',
    'orange',
    'peach',
    'pepper',
    'potato',
    'raspberry',
    'soybean',
    'strawberry',
    'tomato'
]


# ============================================================
# NUMBER OF DISEASE CLASSES FOR EACH CROP
# ============================================================
# IMPORTANT:
# These values should match the classes used when training
# each individual CNN model.

NUM_DISEASE_CLASSES = {
    'apple': 10,
    'blueberry': 10,
    'cherry': 10,
    'corn': 10,
    'gatekeeper': 14,
    'grape': 10,
    'orange': 10,
    'peach': 10,
    'pepper': 10,
    'potato': 10,
    'raspberry': 10,
    'soybean': 10,
    'strawberry': 10,
    'tomato': 10
}

DISEASE_CLASSES = {
    "Apple": [
        "Apple__Apple_scab", "Apple_Black_rot", "Apple_Cedar_apple_rust", "Apple__healthy",
        "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"
    ],
    "Blueberry": ["Blueberry___healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Cherry": ["Cherry_(including_sour)__Powdery_mildew", "Cherry(including_sour)___healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Corn": [
        "Corn_(maize)__Cercospora_leaf_spot Gray_leaf_spot", "Corn(maize)__Common_rust",
        "Corn_(maize)__Northern_Leaf_Blight", "Corn(maize)___healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"
    ],
    "Grape": ["Grape__Black_rot", "Grape_Esca(Black_Measles)", "Grape__Leaf_blight(Isariopsis_Leaf_Spot)", "Grape___healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Orange": ["Orange__Haunglongbing(Citrus_greening)", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Peach": ["Peach__Bacterial_spot", "Peach__healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Pepper,": ["Pepper,bell_Bacterial_spot", "Pepper,_bell__healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Potato": ["Potato__Early_blight", "Potato_Late_blight", "Potato__healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Raspberry": ["Raspberry___healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Soybean": ["Soybean___healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Squash": ["Squash___Powdery_mildew", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Strawberry": ["Strawberry__Leaf_scorch", "Strawberry__healthy", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid", "Invalid"],
    "Tomato": [
        "Tomato__Bacterial_spot", "Tomato_Early_blight", "Tomato__Late_blight", "Tomato__Leaf_Mold",
        "Tomato__Septoria_leaf_spot", "Tomato__Spider_mites Two-spotted_spider_mite", "Tomato__Target_Spot",
        "Tomato__Tomato_Yellow_Leaf_Curl_Virus", "Tomato__Tomato_mosaic_virus", "Tomato___healthy"
    ],
}

DISEASE_CLASS_NAMES = {
    "apple": DISEASE_CLASSES["Apple"],
    "blueberry": DISEASE_CLASSES["Blueberry"],
    "cherry": DISEASE_CLASSES["Cherry"],
    "corn": DISEASE_CLASSES["Corn"],
    "grape": DISEASE_CLASSES["Grape"],
    "orange": DISEASE_CLASSES["Orange"],
    "peach": DISEASE_CLASSES["Peach"],
    "pepper": DISEASE_CLASSES["Pepper,"],
    "potato": DISEASE_CLASSES["Potato"],
    "raspberry": DISEASE_CLASSES["Raspberry"],
    "soybean": DISEASE_CLASSES["Soybean"],
    "squash": DISEASE_CLASSES["Squash"],
    "strawberry": DISEASE_CLASSES["Strawberry"],
    "tomato": DISEASE_CLASSES["Tomato"],
    "gatekeeper": [f"Gatekeeper__class_{index}" for index in range(14)],
}


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CNN_MODEL_DIR = BASE_DIR / "models" / "cnn_models"

LSTM_MODEL_PATH = BASE_DIR / "models" / "lstm_yield.pth"
WEATHER_LSTM_MODEL_PATH = BASE_DIR / "models" / "weather_lstm_yield.pth"

WEATHER_FEATURES = [
    "temperature",
    "rainfall",
    "humidity",
    "soil_moisture",
]
WEATHER_SEQUENCE_LENGTH = 12
WEATHER_RANGES = {
    "temperature": (0.0, 45.0),
    "rainfall": (0.0, 300.0),
    "humidity": (0.0, 100.0),
    "soil_moisture": (0.0, 100.0),
}

AGRICULTURAL_LOCATIONS = {
    "kathmandu": {"name": "Kathmandu Valley", "latitude": 27.7172, "longitude": 85.3240},
    "chitwan": {"name": "Chitwan", "latitude": 27.5291, "longitude": 84.3542},
    "jhapa": {"name": "Jhapa", "latitude": 26.5455, "longitude": 87.8942},
    "morang": {"name": "Morang", "latitude": 26.6636, "longitude": 87.4542},
    "rupandehi": {"name": "Rupandehi", "latitude": 27.5065, "longitude": 83.4470},
    "banke": {"name": "Banke", "latitude": 28.0500, "longitude": 81.6167},
    "dang": {"name": "Dang", "latitude": 28.0500, "longitude": 82.3000},
    "kailali": {"name": "Kailali", "latitude": 28.6932, "longitude": 80.5936},
    "bara": {"name": "Bara", "latitude": 27.1000, "longitude": 85.0667},
    "kaski": {"name": "Kaski", "latitude": 28.2096, "longitude": 83.9856},
    "sunsari": {"name": "Sunsari", "latitude": 26.6636, "longitude": 87.3450},
    "saptari": {"name": "Saptari", "latitude": 26.6333, "longitude": 86.7500},
    "siraha": {"name": "Siraha", "latitude": 26.6542, "longitude": 86.2087},
    "parsa": {"name": "Parsa", "latitude": 27.1333, "longitude": 84.8667},
    "makwanpur": {"name": "Makwanpur", "latitude": 27.4167, "longitude": 85.0333},
    "nawalpur": {"name": "Nawalpur", "latitude": 27.7000, "longitude": 84.1167},
    "kapilvastu": {"name": "Kapilvastu", "latitude": 27.5500, "longitude": 83.0500},
    "bardiya": {"name": "Bardiya", "latitude": 28.3000, "longitude": 81.3500},
    "surkhet": {"name": "Surkhet", "latitude": 28.6000, "longitude": 81.6333},
    "kavrepalanchok": {"name": "Kavrepalanchok", "latitude": 27.5333, "longitude": 85.5667},
    "sindhuli": {"name": "Sindhuli", "latitude": 27.2500, "longitude": 85.9667},
    "ilam": {"name": "Ilam", "latitude": 26.9167, "longitude": 87.9167},
    "mustang": {"name": "Mustang", "latitude": 28.9985, "longitude": 83.8473},
}


# ============================================================
# DEVICE
# ============================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ============================================================
# MODEL FILES
# ============================================================

CNN_MODEL_PATHS = {
    crop: CNN_MODEL_DIR / f"{crop}.pth"
    for crop in CROP_NAMES
}


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 256

NUM_CROPS = len(CROP_NAMES)