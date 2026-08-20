# utils/data_loader.py
import os

import pandas as pd
import torch
from torch.utils.data import Dataset

from config import WEATHER_FEATURES, WEATHER_RANGES, WEATHER_SEQUENCE_LENGTH


class YieldDataset(Dataset):
    def __init__(self, csv_file, image_dir=None, feature_extractor=None, transform=None):
        """
        csv_file: contains columns: crop1_image_path, crop2_image_path, ..., yield
        image_dir: base directory for images
        feature_extractor: instance of FeatureExtractor
        """
        self.df = pd.read_csv(csv_file)
        self.transform = transform

        weather_columns = [
            f"{feature}_{step}"
            for step in range(1, WEATHER_SEQUENCE_LENGTH + 1)
            for feature in WEATHER_FEATURES
        ]
        missing_columns = [column for column in weather_columns if column not in self.df.columns]
        if missing_columns:
            raise ValueError(
                "Yield data is missing weather columns. Regenerate data/yield_data.csv "
                "with generate_synthetic_yield_data.py."
            )

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        weather_sequence = []
        for step in range(1, WEATHER_SEQUENCE_LENGTH + 1):
            weather_sequence.append([
                (float(row[f"{feature}_{step}"]) - WEATHER_RANGES[feature][0])
                / (WEATHER_RANGES[feature][1] - WEATHER_RANGES[feature][0])
                for feature in WEATHER_FEATURES
            ])

        weather = torch.tensor(weather_sequence, dtype=torch.float32)
        yield_target = row["yield"]
        return weather, torch.tensor(float(yield_target), dtype=torch.float32)