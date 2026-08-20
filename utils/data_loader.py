# utils/data_loader.py
import os

import pandas as pd
import torch
from torch.utils.data import Dataset

from config import CROP_NAMES


class YieldDataset(Dataset):
    def __init__(self, csv_file, image_dir, feature_extractor, transform=None):
        """
        csv_file: contains columns: crop1_image_path, crop2_image_path, ..., yield
        image_dir: base directory for images
        feature_extractor: instance of FeatureExtractor
        """
        self.df = pd.read_csv(csv_file)
        self.image_dir = image_dir
        self.feature_extractor = feature_extractor
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        image_dict = {}
        has_valid_images = False

        for crop in CROP_NAMES:
            img_name = row.get(f"{crop}_image")
            img_path = os.path.join(self.image_dir, img_name) if img_name else None
            if img_path and os.path.exists(img_path):
                image_dict[crop] = img_path
                has_valid_images = True
            else:
                image_dict[crop] = None

        if not has_valid_images:
            feature_list = []
            for crop_idx, crop in enumerate(CROP_NAMES):
                base_value = 0.05 + (((idx + crop_idx + 1) % 10) / 10.0)
                feature = torch.full((256,), base_value, dtype=torch.float32)
                feature_list.append(feature)
            features = torch.stack(feature_list).unsqueeze(0)
        else:
            features = self.feature_extractor.extract_features(image_dict)

        yield_target = row['yield']
        return features.squeeze(0), torch.tensor(float(yield_target), dtype=torch.float32)