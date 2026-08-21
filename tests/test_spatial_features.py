import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils.spatial_features import build_spatial_sequence, plant_signals_from_disease
from config import SPATIAL_LSTM_INPUT_SIZE, WEATHER_SEQUENCE_LENGTH


def sample_weather():
    return [{
        "temperature": 27.0,
        "rainfall": 180.0,
        "humidity": 70.0,
        "soil_moisture": 62.0,
    } for _ in range(WEATHER_SEQUENCE_LENGTH)]


def test_spatial_width_includes_plant_signals():
    disease = {
        "predicted_label": "Tomato___healthy",
        "confidence": 0.91,
        "predicted_class": 9,
        "num_classes": 10,
    }
    sequence, plant = build_spatial_sequence(
        sample_weather(),
        crop_name="tomato",
        disease_result=disease,
        place_key="chitwan",
    )
    assert len(sequence) == WEATHER_SEQUENCE_LENGTH
    assert len(sequence[0]) == SPATIAL_LSTM_INPUT_SIZE
    assert plant["available"] is True
    assert plant["healthy_flag"] == 1.0


def test_unhealthy_label_lowers_health():
    healthy = plant_signals_from_disease({
        "predicted_label": "Potato__healthy",
        "confidence": 0.9,
        "predicted_class": 2,
        "num_classes": 3,
    })
    sick = plant_signals_from_disease({
        "predicted_label": "Potato_Late_blight",
        "confidence": 0.9,
        "predicted_class": 1,
        "num_classes": 3,
    })
    assert healthy["health"] > sick["health"]


test_spatial_width_includes_plant_signals()
test_unhealthy_label_lowers_health()
