from config import (
    AGRICULTURAL_LOCATIONS,
    BUDDY_INPUT_SIZE,
    CROP_NAMES,
    SPATIAL_LSTM_INPUT_SIZE,
    WEATHER_FEATURES,
    WEATHER_RANGES,
    WEATHER_SEQUENCE_LENGTH,
)


def _clamp01(value):
    return max(0.0, min(1.0, float(value)))


def is_healthy_label(label):
    if not label:
        return False
    text = str(label).lower()
    return "healthy" in text and "unhealthy" not in text


def plant_signals_from_disease(disease_result):
    if not disease_result:
        return {
            "health": 0.5,
            "confidence": 0.5,
            "severity": 0.5,
            "healthy_flag": 0.5,
            "class_norm": 0.0,
            "available": False,
        }

    label = disease_result.get("predicted_label") or ""
    confidence = _clamp01(disease_result.get("confidence", 0.5))
    healthy = is_healthy_label(label)
    if healthy:
        health = 0.55 + 0.45 * confidence
        severity = 1.0 - health
        healthy_flag = 1.0
    else:
        health = max(0.05, 0.45 * (1.0 - confidence))
        severity = min(0.95, 0.45 + 0.55 * confidence)
        healthy_flag = 0.0

    predicted_class = float(disease_result.get("predicted_class") or 0)
    num_classes = max(1.0, float(disease_result.get("num_classes") or 10))
    return {
        "health": _clamp01(health),
        "confidence": confidence,
        "severity": _clamp01(severity),
        "healthy_flag": healthy_flag,
        "class_norm": _clamp01(predicted_class / num_classes),
        "available": True,
    }


def normalize_weather_value(feature, value):
    minimum, maximum = WEATHER_RANGES[feature]
    span = maximum - minimum
    if span <= 0:
        return 0.0
    return _clamp01((float(value) - minimum) / span)


def location_coordinates(place_key):
    location = AGRICULTURAL_LOCATIONS.get((place_key or "").lower())
    if not location:
        location = AGRICULTURAL_LOCATIONS["kathmandu"]
    lat = (float(location["latitude"]) - 26.0) / 4.0
    lon = (float(location["longitude"]) - 80.0) / 8.0
    return _clamp01(lat), _clamp01(lon)


def crop_index(crop_name):
    if crop_name in CROP_NAMES:
        return CROP_NAMES.index(crop_name)
    return 0


def build_spatial_sequence(weather_steps, crop_name=None, disease_result=None, place_key=None):
    if len(weather_steps) != WEATHER_SEQUENCE_LENGTH:
        raise ValueError(f"Expected {WEATHER_SEQUENCE_LENGTH} weather steps.")

    plant = plant_signals_from_disease(disease_result)
    lat_norm, lon_norm = location_coordinates(place_key)
    crop_idx = crop_index(crop_name)
    crop_norm = crop_idx / max(1, len(CROP_NAMES) - 1)
    one_hot = [0.0] * len(CROP_NAMES)
    one_hot[crop_idx] = 1.0

    rainfall_running = 0.0
    sequence = []
    for step_index, weather_step in enumerate(weather_steps):
        normalized = [normalize_weather_value(feature, weather_step[feature]) for feature in WEATHER_FEATURES]
        temperature = float(weather_step["temperature"])
        rainfall = float(weather_step["rainfall"])
        humidity = float(weather_step["humidity"])
        soil_moisture = float(weather_step["soil_moisture"])
        rainfall_running += rainfall
        season_progress = step_index / max(1, WEATHER_SEQUENCE_LENGTH - 1)
        temp_dev = _clamp01(1.0 - abs(temperature - 27.0) / 18.0)
        rain_balance = _clamp01(1.0 - abs(rainfall - 185.0) / 185.0)
        humidity_dev = _clamp01(1.0 - abs(humidity - 72.0) / 72.0)
        soil_deficit = _clamp01(1.0 - soil_moisture / 100.0)
        rain_accum = _clamp01(rainfall_running / (WEATHER_SEQUENCE_LENGTH * 300.0))
        stress = _clamp01(plant["severity"] * (0.5 + 0.5 * (1.0 - plant["confidence"])))

        features = (
            normalized
            + [lat_norm, lon_norm, season_progress, temp_dev, rain_balance, humidity_dev, soil_deficit, rain_accum, crop_norm]
            + one_hot
            + [
                plant["health"],
                plant["confidence"],
                plant["severity"],
                stress,
                plant["class_norm"],
                plant["healthy_flag"],
            ]
        )
        if len(features) != SPATIAL_LSTM_INPUT_SIZE:
            raise ValueError(f"Spatial feature width is {len(features)}, expected {SPATIAL_LSTM_INPUT_SIZE}.")
        sequence.append(features)
    return sequence, plant


def weather_means(weather_steps):
    means = {}
    for feature in WEATHER_FEATURES:
        means[feature] = sum(float(step[feature]) for step in weather_steps) / len(weather_steps)
    return means


def build_buddy_vector(lstm_norm, plant, weather_steps, crop_name=None):
    means = weather_means(weather_steps)
    soil_norm = normalize_weather_value("soil_moisture", means["soil_moisture"])
    agreement = 1.0 - abs(plant["health"] - soil_norm)
    vector = [
        _clamp01(lstm_norm),
        plant["health"],
        plant["confidence"],
        plant["severity"],
        plant["healthy_flag"],
        crop_index(crop_name) / max(1, len(CROP_NAMES) - 1),
        normalize_weather_value("temperature", means["temperature"]),
        normalize_weather_value("rainfall", means["rainfall"]),
        normalize_weather_value("humidity", means["humidity"]),
        soil_norm,
        _clamp01(agreement),
        _clamp01(plant["health"] * plant["confidence"]),
    ]
    if len(vector) != BUDDY_INPUT_SIZE:
        raise ValueError(f"Buddy feature width is {len(vector)}, expected {BUDDY_INPUT_SIZE}.")
    return vector, means
