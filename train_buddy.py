import random
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from config import BUDDY_MODEL_PATH, CROP_NAMES, DEVICE, WEATHER_SEQUENCE_LENGTH
from generate_synthetic_yield_data import generate_weather_sequence
from models.lstm_model import BuddyFusionNet, SpatialPaddyLSTM
from utils.spatial_features import build_buddy_vector, build_spatial_sequence
from utils.yield_pipeline import denormalize_yield, normalize_yield
from config import SPATIAL_LSTM_HIDDEN_SIZE, SPATIAL_LSTM_INPUT_SIZE, SPATIAL_LSTM_MODEL_PATH, SPATIAL_LSTM_NUM_LAYERS

RANDOM_SEED = 21
SAMPLE_COUNT = 1600
EPOCHS = 40


def fake_disease(crop_name, rng):
    healthy = rng.random() > 0.42
    confidence = 0.55 + rng.random() * 0.44
    if healthy:
        label = f"{crop_name}___healthy"
        predicted_class = 0
    else:
        label = f"{crop_name}__leaf_blight"
        predicted_class = 1 + rng.randrange(3)
    return {
        "predicted_label": label,
        "confidence": round(confidence, 4),
        "predicted_class": predicted_class,
        "num_classes": 10,
        "crop": crop_name,
    }


def main():
    rng = random.Random(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    if not Path(SPATIAL_LSTM_MODEL_PATH).exists():
        raise SystemExit(f"Missing spatial LSTM weights at {SPATIAL_LSTM_MODEL_PATH}")

    spatial = SpatialPaddyLSTM(
        input_size=SPATIAL_LSTM_INPUT_SIZE,
        hidden_size=SPATIAL_LSTM_HIDDEN_SIZE,
        num_layers=SPATIAL_LSTM_NUM_LAYERS,
    ).to(DEVICE)
    spatial.load_state_dict(torch.load(SPATIAL_LSTM_MODEL_PATH, map_location=DEVICE, weights_only=True))
    spatial.eval()

    vectors = []
    targets = []
    places = list(__import__("config").AGRICULTURAL_LOCATIONS.keys())

    with torch.no_grad():
        for sample_idx in range(SAMPLE_COUNT):
            crop_name = rng.choice(CROP_NAMES)
            place_key = rng.choice(places)
            weather_steps = []
            generated = generate_weather_sequence(sample_idx + 1)
            for values in generated:
                weather_steps.append({
                    "temperature": values[0],
                    "rainfall": values[1],
                    "humidity": values[2],
                    "soil_moisture": values[3],
                })
            disease = fake_disease(crop_name, rng)
            sequence, plant = build_spatial_sequence(
                weather_steps,
                crop_name=crop_name,
                disease_result=disease,
                place_key=place_key,
            )
            features = torch.tensor([sequence], dtype=torch.float32, device=DEVICE)
            lstm_norm = float(spatial(features).squeeze().cpu())
            vector, _means = build_buddy_vector(lstm_norm, plant, weather_steps, crop_name=crop_name)
            weather_yield = denormalize_yield(lstm_norm)
            health_factor = 0.52 + 0.48 * plant["health"] * (0.7 + 0.3 * plant["confidence"])
            target = max(2.0, min(8.5, weather_yield * health_factor))
            vectors.append(vector)
            targets.append([normalize_yield(target)])

    x = torch.tensor(vectors, dtype=torch.float32)
    y = torch.tensor(targets, dtype=torch.float32)
    dataset = TensorDataset(x, y)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = BuddyFusionNet().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loss_fn = torch.nn.MSELoss()

    for epoch in range(1, EPOCHS + 1):
        model.train()
        running = 0.0
        for batch_x, batch_y in loader:
            batch_x = batch_x.to(DEVICE)
            batch_y = batch_y.to(DEVICE)
            optimizer.zero_grad()
            pred = model(batch_x)
            loss = loss_fn(pred, batch_y)
            loss.backward()
            optimizer.step()
            running += loss.item() * batch_x.size(0)
        if epoch == 1 or epoch % 10 == 0 or epoch == EPOCHS:
            print(f"Epoch {epoch:02d} | loss {running / len(dataset):.6f}")

    BUDDY_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), BUDDY_MODEL_PATH)
    print(f"Buddy fusion model saved to {BUDDY_MODEL_PATH}")


if __name__ == "__main__":
    main()
