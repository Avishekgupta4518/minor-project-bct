from __future__ import annotations

import csv
from pathlib import Path
import random

from PIL import Image, ImageDraw

from config import CROP_NAMES

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


def generate_yield_value(sample_idx: int, crop_idx: int) -> float:
    crop_bias = {
        "apple": 5.2,
        "blueberry": 4.7,
        "cherry": 5.6,
        "corn": 6.1,
        "gatekeeper": 5.0,
        "grape": 5.8,
        "orange": 5.3,
        "peach": 5.1,
        "pepper": 4.9,
        "potato": 6.4,
        "raspberry": 4.8,
        "soybean": 6.0,
        "strawberry": 5.5,
        "tomato": 5.9,
    }
    seasonal = (sample_idx / 12.0) * 0.9
    crop_factor = crop_idx * 0.08
    noise = ((sample_idx * 13 + crop_idx * 17) % 11) / 10.0 - 0.5
    value = crop_bias[CROP_NAMES[crop_idx]] + seasonal + crop_factor + noise
    return round(max(3.0, min(8.5, value)), 2)


def generate_yield_dataset(num_rows: int = 120) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    header = [f"{crop}_image" for crop in CROP_NAMES] + ["yield"]
    rows = [header]

    for sample_idx in range(1, num_rows + 1):
        row = []
        for crop_idx, crop_name in enumerate(CROP_NAMES):
            filename = f"{crop_name}_{sample_idx:03d}.jpg"
            image = draw_leaf_image(seed=sample_idx * 17 + crop_idx * 31, crop_name=crop_name)
            image.save(IMAGE_DIR / filename, format="JPEG", quality=90)
            row.append(filename)
        row.append(generate_yield_value(sample_idx, (sample_idx + 1) % len(CROP_NAMES)))
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

    return False


if __name__ == "__main__":
    ensure_dataset(120)
