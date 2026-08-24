# train_rice_lstm.py
"""Train RiceYieldLSTM on district-level historical rice yields.

Input:  data/rice_yield_districts.csv (place, year, yield_t_ha)
Output: models/rice_yield_lstm.pth + models/rice_yield_meta.json

The model sees only past annual yields for a place and predicts the next
season's yield — no weather or other inputs.
"""
import json
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

from config import DEVICE, RICE_DATA_PATH, RICE_META_PATH, RICE_MODEL_PATH, RICE_SEQUENCE_LENGTH
from models.lstm_model import RiceYieldLSTM

EPOCHS = 300
LEARNING_RATE = 5e-3
HIDDEN_SIZE = 64
NUM_LAYERS = 2


def load_series():
    import csv

    series = {}
    with open(RICE_DATA_PATH, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            series.setdefault(row["place"], []).append(
                (int(row["year"]), float(row["yield_t_ha"]))
            )
    for place in series:
        series[place].sort()
    return series


def main():
    torch.manual_seed(42)
    np.random.seed(0)

    series = load_series()
    all_yields = [value for rows in series.values() for _year, value in rows]
    yield_min, yield_max = min(all_yields), max(all_yields)

    def normalize(value):
        return (value - yield_min) / (yield_max - yield_min)

    windows, targets = [], []
    for rows in series.values():
        values = [normalize(value) for _year, value in rows]
        for start in range(len(values) - RICE_SEQUENCE_LENGTH):
            windows.append(values[start:start + RICE_SEQUENCE_LENGTH])
            targets.append(values[start + RICE_SEQUENCE_LENGTH])

    x = torch.tensor(windows, dtype=torch.float32).unsqueeze(-1)
    y = torch.tensor(targets, dtype=torch.float32).unsqueeze(-1)

    split = int(len(x) * 0.9)
    order = torch.randperm(len(x))
    train_idx, val_idx = order[:split], order[split:]
    x_train, y_train = x[train_idx], y[train_idx]
    x_val, y_val = x[val_idx], y[val_idx]

    model = RiceYieldLSTM(hidden_size=HIDDEN_SIZE, num_layers=NUM_LAYERS).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.MSELoss()

    for epoch in range(EPOCHS):
        model.train()
        optimizer.zero_grad()
        loss = criterion(model(x_train), y_train)
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 50 == 0:
            model.eval()
            with torch.no_grad():
                val_loss = criterion(model(x_val), y_val)
                val_mae_t = float((model(x_val) - y_val).abs().mean()) * (yield_max - yield_min)
            print(f"epoch {epoch + 1:4d}  train {loss.item():.6f}  "
                  f"val {val_loss.item():.6f}  val MAE {val_mae_t:.3f} t/ha")

    RICE_MODEL_PATH.parent.mkdir(exist_ok=True)
    torch.save(model.state_dict(), RICE_MODEL_PATH)
    meta = {
        "places": sorted(series),
        "yield_min": yield_min,
        "yield_max": yield_max,
        "sequence_length": RICE_SEQUENCE_LENGTH,
        "last_years": {place: rows[-1][0] for place, rows in series.items()},
    }
    RICE_META_PATH.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"\nsaved {RICE_MODEL_PATH}")
    print(f"saved {RICE_META_PATH} ({len(meta['places'])} places)")


if __name__ == "__main__":
    main()
