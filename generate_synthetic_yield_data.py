from __future__ import annotations

import csv
from pathlib import Path
import random

from PIL import Image, ImageDraw

from config import CROP_NAMES, WEATHER_FEATURES, WEATHER_SEQUENCE_LENGTH

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = DATA_DIR / "images"
CSV_PATH = DATA_DIR / "yield_data.csv"

CROP_COLOR_MAP = {
    "apple": (110, 192, 95),
    "blueberry": (91, 106, 214),
    "cherry": (206, 83, 90),
    "corn": (196, 172, 63),
    "gatekeeper": (110, 118, 138),
    "grape": (110, 70, 160),
    "orange": (227, 149, 54),
    "peach": (241, 162, 148),
    "pepper": (162, 214, 91),
    "potato": (202, 175, 119),
    "raspberry": (195, 77, 120),
    "soybean": (117, 176, 112),
    "strawberry": (218, 92, 102),
    "tomato": (196, 68, 75),
}


def draw_leaf_image(seed: int, crop_name: str) -> Image.Image:
    rng = random.Random(seed)
    base = CROP_COLOR_MAP[crop_name]
    highlight = tuple(min(255, max(0, channel + 40)) for channel in base)
    shadow = tuple(max(0, channel - 45) for channel in base)
    background = (242, 248, 240)

    image = Image.new("RGB", (224, 224), background)
    draw = ImageDraw.Draw(image)

    leaf_center_x = 112
    leaf_center_y = 112
    leaf_width = 150
    leaf_height = 110

    leaf_points = [
        (leaf_center_x, leaf_center_y - leaf_height // 2),
        (leaf_center_x + leaf_width // 2, leaf_center_y - 20),
        (leaf_center_x + leaf_width // 2 + 10, leaf_center_y + 20),
        (leaf_center_x + 20, leaf_center_y + leaf_height // 2),
        (leaf_center_x, leaf_center_y + leaf_height // 2 + 18),
        (leaf_center_x - 24, leaf_center_y + leaf_height // 2 - 6),
        (leaf_center_x - leaf_width // 2, leaf_center_y + 8),
        (leaf_center_x - leaf_width // 2 + 4, leaf_center_y - 28),
    ]
    draw.polygon(leaf_points, fill=base)
    draw.line((leaf_center_x, 20, leaf_center_x, 204), fill=shadow, width=6)
    for offset in (-30, -18, -6, 18, 30):
        draw.line((leaf_center_x, 38, leaf_center_x + offset, 170), fill=highlight, width=3)

    for _ in range(20):
        x = rng.randint(30, 190)
        y = rng.randint(30, 190)
        radius = rng.randint(4, 11)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(rng.randint(80, 140), rng.randint(180, 220), rng.randint(100, 180)))

    draw.rectangle((30, 30, 194, 194), outline=(255, 255, 255, 120), width=2)
    return image


def generate_weather_sequence(sample_idx: int) -> list[list[float]]:
    sequence = []
    climate_shift = ((sample_idx % 20) - 10) / 10.0
    for month in range(WEATHER_SEQUENCE_LENGTH):
        seasonal = (month / WEATHER_SEQUENCE_LENGTH) * 6.0
        temperature = 22.0 + seasonal + ((sample_idx * 7 + month * 3) % 9) - 4.0 + climate_shift * 4.0
        rainfall = 110.0 + ((sample_idx * 19 + month * 23) % 150) + climate_shift * 50.0
        humidity = 52.0 + ((sample_idx * 11 + month * 7) % 43) + climate_shift * 18.0
        soil_moisture = min(100.0, 30.0 + rainfall * 0.16 + humidity * 0.25)
        sequence.append([round(temperature, 2), round(rainfall, 2), round(humidity, 2), round(soil_moisture, 2)])
    return sequence


def generate_yield_value(weather_sequence: list[list[float]], sample_idx: int) -> float:
    average_temperature = sum(item[0] for item in weather_sequence) / len(weather_sequence)
    average_rainfall = sum(item[1] for item in weather_sequence) / len(weather_sequence)
    average_humidity = sum(item[2] for item in weather_sequence) / len(weather_sequence)
    average_soil_moisture = sum(item[3] for item in weather_sequence) / len(weather_sequence)
    temperature_score = max(0.0, 1.0 - abs(average_temperature - 27.0) / 18.0)
    rainfall_score = max(0.0, 1.0 - abs(average_rainfall - 185.0) / 185.0)
    humidity_score = max(0.0, 1.0 - abs(average_humidity - 72.0) / 72.0)
    soil_score = average_soil_moisture / 100.0
    noise = ((sample_idx * 13) % 11) / 100.0 - 0.05
    value = 1.5 + 2.4 * temperature_score + 1.5 * rainfall_score + 1.4 * humidity_score + 1.2 * soil_score + noise
    return round(max(2.0, min(8.5, value)), 2)


def generate_yield_dataset(num_rows: int = 120) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    weather_columns = [
        f"{feature}_{step}"
        for step in range(1, WEATHER_SEQUENCE_LENGTH + 1)
        for feature in WEATHER_FEATURES
    ]
    header = ["date"] + weather_columns + [f"{crop}_image" for crop in CROP_NAMES] + ["yield"]
    rows = [header]

    for sample_idx in range(1, num_rows + 1):
        weather_sequence = generate_weather_sequence(sample_idx)
        row = [f"2026-{((sample_idx - 1) // 12) + 1:02d}-{((sample_idx - 1) % 28) + 1:02d}"]
        for weather_values in weather_sequence:
            row.extend(weather_values)
        for crop_idx, crop_name in enumerate(CROP_NAMES):
            filename = f"{crop_name}_{sample_idx:03d}.jpg"
            image = draw_leaf_image(seed=sample_idx * 17 + crop_idx * 31, crop_name=crop_name)
            image.save(IMAGE_DIR / filename, format="JPEG", quality=90)
            row.append(filename)
        row.append(generate_yield_value(weather_sequence, sample_idx))
        rows.append(row)

    with CSV_PATH.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

    print(f"Generated synthetic yield dataset with {num_rows} rows at {CSV_PATH}")


def ensure_dataset(min_rows: int = 80) -> bool:
    if not CSV_PATH.exists():
        generate_yield_dataset(num_rows=max(min_rows, 80))
        return True

    with CSV_PATH.open("r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    if len(rows) <= 1:
        generate_yield_dataset(num_rows=max(min_rows, 80))
        return True

    if len(rows) - 1 < min_rows:
        generate_yield_dataset(num_rows=max(min_rows, 80))
        return True

    for crop in CROP_NAMES:
        sample_name = f"{crop}_001.jpg"
        if not (IMAGE_DIR / sample_name).exists():
            generate_yield_dataset(num_rows=max(min_rows, 80))
            return True

    required_weather_column = f"{WEATHER_FEATURES[0]}_{WEATHER_SEQUENCE_LENGTH}"
    if required_weather_column not in rows[0]:
        generate_yield_dataset(num_rows=max(min_rows, 80))
        return True

    return False


if __name__ == "__main__":
    ensure_dataset(120)
