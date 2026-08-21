from pathlib import Path

import torch

from config import (
    BUDDY_MODEL_PATH,
    DEVICE,
    SPATIAL_LSTM_HIDDEN_SIZE,
    SPATIAL_LSTM_INPUT_SIZE,
    SPATIAL_LSTM_MODEL_PATH,
    SPATIAL_LSTM_NUM_LAYERS,
    WEATHER_FEATURES,
    WEATHER_RANGES,
    WEATHER_SEQUENCE_LENGTH,
    YIELD_RANGE,
)
from models.lstm_model import BuddyFusionNet, SpatialPaddyLSTM
from utils.spatial_features import build_buddy_vector, build_spatial_sequence


def denormalize_yield(value):
    minimum, maximum = YIELD_RANGE
    clipped = max(0.0, min(1.0, float(value)))
    return minimum + clipped * (maximum - minimum)


def normalize_yield(value):
    minimum, maximum = YIELD_RANGE
    return max(0.0, min(1.0, (float(value) - minimum) / (maximum - minimum)))


def parse_weather_payload(data):
    weather_sequence = data.get("weather_sequence")
    if weather_sequence is not None:
        if not isinstance(weather_sequence, list) or len(weather_sequence) != WEATHER_SEQUENCE_LENGTH:
            raise ValueError(f"weather_sequence must contain {WEATHER_SEQUENCE_LENGTH} steps.")
        weather_steps = weather_sequence
    else:
        weather = data.get("weather")
        if not isinstance(weather, dict):
            raise ValueError("Weather data or a 12-step weather_sequence is required.")
        weather_steps = [weather] * WEATHER_SEQUENCE_LENGTH

    normalized_steps = []
    for weather_step in weather_steps:
        if not isinstance(weather_step, dict):
            raise ValueError("Each weather step must be an object.")
        cleaned = {}
        for feature in WEATHER_FEATURES:
            if feature not in weather_step:
                raise ValueError(f"Missing weather fields: {feature}")
            try:
                value = float(weather_step[feature])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{feature} must be numeric.") from exc
            minimum, maximum = WEATHER_RANGES[feature]
            if not minimum <= value <= maximum:
                raise ValueError(f"{feature} must be between {minimum:g} and {maximum:g}.")
            cleaned[feature] = value
        normalized_steps.append(cleaned)
    return normalized_steps


class YieldPipeline:
    def __init__(self):
        self.device = DEVICE
        self.spatial_model = SpatialPaddyLSTM(
            input_size=SPATIAL_LSTM_INPUT_SIZE,
            hidden_size=SPATIAL_LSTM_HIDDEN_SIZE,
            num_layers=SPATIAL_LSTM_NUM_LAYERS,
        ).to(self.device)
        self.buddy_model = BuddyFusionNet().to(self.device)
        self.spatial_ready = Path(SPATIAL_LSTM_MODEL_PATH).exists()
        self.buddy_ready = Path(BUDDY_MODEL_PATH).exists()

        if self.spatial_ready:
            state = torch.load(SPATIAL_LSTM_MODEL_PATH, map_location=self.device, weights_only=True)
            self.spatial_model.load_state_dict(state)
            self.spatial_model.eval()
        if self.buddy_ready:
            state = torch.load(BUDDY_MODEL_PATH, map_location=self.device, weights_only=True)
            self.buddy_model.load_state_dict(state)
            self.buddy_model.eval()

    def predict(self, weather_steps, crop_name=None, disease_result=None, place_key=None):
        if not self.spatial_ready:
            raise RuntimeError("Spatial LSTM checkpoint is missing.")

        sequence, plant = build_spatial_sequence(
            weather_steps,
            crop_name=crop_name,
            disease_result=disease_result,
            place_key=place_key,
        )
        features = torch.tensor([sequence], dtype=torch.float32, device=self.device)
        with torch.no_grad():
            lstm_norm_tensor, _hidden = self.spatial_model(features, return_hidden=True)
            lstm_norm = float(lstm_norm_tensor.squeeze().cpu())

        lstm_yield = round(denormalize_yield(lstm_norm), 2)
        buddy_vector, weather_means = build_buddy_vector(lstm_norm, plant, weather_steps, crop_name=crop_name)
        fused_yield = lstm_yield
        if self.buddy_ready:
            buddy_tensor = torch.tensor([buddy_vector], dtype=torch.float32, device=self.device)
            with torch.no_grad():
                fused_norm = float(self.buddy_model(buddy_tensor).squeeze().cpu())
            fused_yield = round(denormalize_yield(fused_norm), 2)

        adjustment = round(fused_yield - lstm_yield, 2)
        relationship = "aligned"
        if not plant["available"]:
            relationship = "weather_only"
        elif plant["healthy_flag"] >= 0.5 and adjustment >= 0:
            relationship = "plant_supports_weather"
        elif plant["healthy_flag"] < 0.5 and adjustment < 0:
            relationship = "disease_reduces_yield"
        elif abs(adjustment) < 0.08:
            relationship = "weak_shift"
        else:
            relationship = "mixed_signals"

        return {
            "lstm_yield": lstm_yield,
            "fused_yield": fused_yield,
            "yield_prediction": fused_yield,
            "adjustment": adjustment,
            "relationship": relationship,
            "plant": plant,
            "weather_means": {key: round(value, 2) for key, value in weather_means.items()},
            "crop": crop_name,
            "place": place_key,
            "sequence_length": WEATHER_SEQUENCE_LENGTH,
            "buddy_ready": self.buddy_ready,
            "spatial_ready": self.spatial_ready,
        }
