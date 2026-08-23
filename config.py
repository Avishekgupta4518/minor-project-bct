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
# DISEASE RECOMMENDATIONS (farmer-facing, static lookup — no ML)
# ============================================================

GENERIC_HEALTHY_ADVICE = (
    "No disease detected. Keep monitoring the leaves weekly and maintain your normal watering schedule."
)
GENERIC_DISEASE_ADVICE = (
    "A possible issue was detected. Isolate affected plants if possible and consult your "
    "local agriculture extension officer before applying any treatment."
)

DISEASE_RECOMMENDATIONS = {
    "Apple__Apple_scab": "Remove and destroy fallen infected leaves. Apply a recommended fungicide before wet spring weather; avoid overhead watering.",
    "Apple_Black_rot": "Prune out dead or cankered wood. Remove mummified fruit from the tree and ground to reduce spore spread.",
    "Apple_Cedar_apple_rust": "Remove nearby juniper/cedar hosts if possible. Apply fungicide at pink bud stage next season.",
    "Apple__healthy": GENERIC_HEALTHY_ADVICE,
    "Blueberry___healthy": GENERIC_HEALTHY_ADVICE,
    "Cherry_(including_sour)__Powdery_mildew": "Improve air circulation by pruning dense growth. Apply sulfur-based fungicide at first sign of white powder.",
    "Cherry(including_sour)___healthy": GENERIC_HEALTHY_ADVICE,
    "Corn_(maize)__Cercospora_leaf_spot Gray_leaf_spot": "Rotate crops away from corn/maize next season. Avoid dense planting to improve airflow.",
    "Corn(maize)__Common_rust": "Plant rust-resistant varieties next season. Fungicide is rarely needed unless infection is severe before tasseling.",
    "Corn_(maize)__Northern_Leaf_Blight": "Rotate crops and till under crop residue after harvest to reduce spore carryover.",
    "Corn(maize)___healthy": GENERIC_HEALTHY_ADVICE,
    "Grape__Black_rot": "Remove mummified berries and infected leaves. Apply fungicide starting at bud break in wet seasons.",
    "Grape_Esca(Black_Measles)": "No cure exists — remove and destroy severely affected vines to slow spread. Avoid pruning during wet weather.",
    "Grape__Leaf_blight(Isariopsis_Leaf_Spot)": "Improve canopy airflow with pruning. Apply a copper-based fungicide if humidity stays high.",
    "Grape___healthy": GENERIC_HEALTHY_ADVICE,
    "Orange__Haunglongbing(Citrus_greening)": "No cure exists. Remove and destroy the infected tree to protect nearby citrus, and control psyllid insects.",
    "Peach__Bacterial_spot": "Avoid overhead irrigation. Apply copper-based bactericide early in the season; prune for airflow.",
    "Peach__healthy": GENERIC_HEALTHY_ADVICE,
    "Pepper,bell_Bacterial_spot": "Avoid working in wet fields to prevent spread. Use copper-based sprays and rotate away from peppers/tomatoes next season.",
    "Pepper,_bell__healthy": GENERIC_HEALTHY_ADVICE,
    "Potato__Early_blight": "Remove infected lower leaves. Apply a recommended fungicide and avoid overhead watering late in the day.",
    "Potato_Late_blight": "Act quickly — this spreads fast in wet weather. Remove and destroy infected plants, apply fungicide, avoid working in wet fields.",
    "Potato__healthy": GENERIC_HEALTHY_ADVICE,
    "Raspberry___healthy": GENERIC_HEALTHY_ADVICE,
    "Soybean___healthy": GENERIC_HEALTHY_ADVICE,
    "Squash___Powdery_mildew": "Improve spacing and airflow between plants. Apply sulfur or potassium bicarbonate spray at first sign of white spots.",
    "Strawberry__Leaf_scorch": "Remove old infected leaves after harvest. Avoid overhead watering; apply fungicide if recurring yearly.",
    "Strawberry__healthy": GENERIC_HEALTHY_ADVICE,
    "Tomato__Bacterial_spot": "Avoid overhead watering and working in wet fields. Rotate crops and use copper-based sprays.",
    "Tomato_Early_blight": "Remove lower infected leaves, mulch to prevent soil splash, and apply a recommended fungicide.",
    "Tomato__Late_blight": "Act quickly — remove and destroy infected plants immediately to protect the rest of the field.",
    "Tomato__Leaf_Mold": "Improve greenhouse/field ventilation and reduce humidity around leaves.",
    "Tomato__Septoria_leaf_spot": "Remove infected lower leaves and avoid overhead watering; rotate crops next season.",
    "Tomato__Spider_mites Two-spotted_spider_mite": "Spray leaves with water to dislodge mites, or use an approved miticide/insecticidal soap.",
    "Tomato__Target_Spot": "Remove infected leaves and improve airflow. Apply fungicide if the field stays humid.",
    "Tomato__Tomato_Yellow_Leaf_Curl_Virus": "This spreads via whiteflies — control the whitefly population and remove severely infected plants.",
    "Tomato__Tomato_mosaic_virus": "No cure exists. Remove and destroy infected plants and disinfect tools between use to avoid spreading it.",
    "Tomato___healthy": GENERIC_HEALTHY_ADVICE,
}


def get_disease_recommendation(label, lang="en"):
    """Farmer-facing advice for a predicted disease label, in the given
    language ('en' or 'ne'). Falls back to a generic healthy/diseased
    message (based on the label text) for any label not in the lookup,
    e.g. gatekeeper class placeholders."""
    from translations import (
        DISEASE_RECOMMENDATIONS_NE,
        GENERIC_HEALTHY_ADVICE_NE,
        GENERIC_DISEASE_ADVICE_NE,
    )

    if lang == "ne":
        if not label:
            return GENERIC_DISEASE_ADVICE_NE
        if label in DISEASE_RECOMMENDATIONS_NE:
            return DISEASE_RECOMMENDATIONS_NE[label]
        return GENERIC_HEALTHY_ADVICE_NE if "healthy" in label.lower() else GENERIC_DISEASE_ADVICE_NE

    if not label:
        return GENERIC_DISEASE_ADVICE
    if label in DISEASE_RECOMMENDATIONS:
        return DISEASE_RECOMMENDATIONS[label]
    return GENERIC_HEALTHY_ADVICE if "healthy" in label.lower() else GENERIC_DISEASE_ADVICE


def get_disease_label_display(label, lang="en"):
    """Human-readable disease name for display, translated if lang='ne'.
    The canonical `label` string itself is left untouched everywhere else
    (storage, healthy/diseased logic) — this is presentation-only."""
    if lang == "ne":
        from translations import DISEASE_LABELS_NE
        return DISEASE_LABELS_NE.get(label, label)
    return label


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CNN_MODEL_DIR = BASE_DIR / "models" / "cnn_models"

LSTM_MODEL_PATH = BASE_DIR / "models" / "lstm_yield.pth"
WEATHER_LSTM_MODEL_PATH = BASE_DIR / "models" / "weather_lstm_yield.pth"
SPATIAL_LSTM_MODEL_PATH = BASE_DIR / "models" / "spatial_paddy_lstm_final.pth"
BUDDY_MODEL_PATH = BASE_DIR / "models" / "buddy_fusion.pth"

SPATIAL_LSTM_INPUT_SIZE = 33
SPATIAL_LSTM_HIDDEN_SIZE = 128
SPATIAL_LSTM_NUM_LAYERS = 2
BUDDY_INPUT_SIZE = 12
YIELD_RANGE = (2.0, 8.5)

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
    'jhapa': {
        'name': 'Jhapa, Nepal',
        'latitude': 26.55,
        'longitude': 87.95,
    },
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