import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils.feature_extractor import FeatureExtractor


def test_feature_extractor_does_not_load_models_at_init():
    extractor = FeatureExtractor()
    assert extractor.models == {}


test_feature_extractor_does_not_load_models_at_init()
