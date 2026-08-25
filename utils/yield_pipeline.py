# utils/yield_pipeline.py
import json
from pathlib import Path

import torch

from config import DEVICE, RICE_DATA_PATH, RICE_META_PATH, RICE_MODEL_PATH, RICE_SEQUENCE_LENGTH
from models.lstm_model import RiceYieldLSTM


class RiceYieldPipeline:
    """Predicts rice yield for a place from its historical annual yields."""

    def __init__(self):
        self.ready = Path(RICE_MODEL_PATH).exists() and Path(RICE_META_PATH).exists()
        if not self.ready:
            return

        meta = json.loads(RICE_META_PATH.read_text(encoding="utf-8"))
        self.places = meta["places"]
        self.yield_min = float(meta["yield_min"])
        self.yield_max = float(meta["yield_max"])
        self.sequence_length = int(meta.get("sequence_length", RICE_SEQUENCE_LENGTH))
        self.last_years = meta.get("last_years", {})

        import csv

        self.history = {}
        with open(RICE_DATA_PATH, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                self.history.setdefault(row["place"].strip().lower(), []).append(
                    (int(row["year"]), float(row["yield_t_ha"]))
                )
        for place in self.history:
            self.history[place].sort()

        self.model = RiceYieldLSTM().to(DEVICE)
        state = torch.load(RICE_MODEL_PATH, map_location=DEVICE, weights_only=True)
        self.model.load_state_dict(state)
        self.model.eval()

    def predict(self, place):
        if not self.ready:
            raise RuntimeError("Rice yield model checkpoint is missing. Run train_rice_lstm.py.")

        key = place.strip().lower()
        if key not in self.history:
            raise ValueError(f"Unknown place: {place}. Supported: {', '.join(self.places)}.")

        rows = self.history[key][-self.sequence_length:]
        if len(rows) < self.sequence_length:
            raise ValueError(f"Not enough historical data for {place}.")

        def normalize(value):
            return (value - self.yield_min) / (self.yield_max - self.yield_min)

        sequence = [normalize(value) for _year, value in rows]
        features = torch.tensor([sequence], dtype=torch.float32, device=DEVICE).unsqueeze(-1)
        with torch.no_grad():
            normalized = float(self.model(features).squeeze())

        clipped = max(0.0, min(1.0, normalized))
        predicted = round(self.yield_min + clipped * (self.yield_max - self.yield_min), 2)
        last_year = rows[-1][0]
        recent = self.history[key][-10:]
        return {
            "crop": "rice",
            "place": key,
            "yield_prediction": predicted,
            "unit": "t/ha",
            "based_on_years": self.sequence_length,
            "last_record_year": f"{str(last_year)[:4]}/{str(last_year)[4:]}",
            "recent_history": [
                {
                    "year": f"{str(year)[:4]}/{str(year)[4:]}",
                    "yield_t_ha": value,
                }
                for year, value in recent
            ],
        }
