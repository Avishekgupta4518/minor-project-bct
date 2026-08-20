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


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CNN_MODEL_DIR = BASE_DIR / "models" / "cnn_models"

LSTM_MODEL_PATH = BASE_DIR / "models" / "lstm_yield.pth"


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