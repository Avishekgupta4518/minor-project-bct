# utils/feature_extractor.py
import torch
from torchvision import transforms
from PIL import Image

from config import (
    CROP_NAMES,
    DISEASE_CLASS_NAMES,
    GATEKEEPER_CROP,
    GATEKEEPER_CLASS_TO_CROP,
    NUM_DISEASE_CLASSES,
    CNN_MODEL_PATHS,
    DEVICE,
    SPECIES_CROPS,
    get_disease_recommendation,
    get_disease_label_display,
)
from models.cnn_arch import CropCNN, GatekeeperCNN

if hasattr(torch.backends, "nnpack"):
    torch.backends.nnpack.enabled = False


class FeatureExtractor:
    def __init__(self):
        self.models = {}
        self.transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def _load_model(self, crop_name):
        if crop_name in self.models:
            return self.models[crop_name]

        model_path = CNN_MODEL_PATHS[crop_name]
        if crop_name == "gatekeeper":
            model = GatekeeperCNN(num_classes=NUM_DISEASE_CLASSES[crop_name]).to(DEVICE)
        else:
            model = CropCNN(num_classes=NUM_DISEASE_CLASSES[crop_name]).to(DEVICE)

        checkpoint = torch.load(model_path, map_location=DEVICE, weights_only=True)
        load_result = model.load_state_dict(checkpoint, strict=False)
        missing_weights = [key for key in getattr(load_result, "missing_keys", []) if not key.endswith("num_batches_tracked")]
        if missing_weights:
            raise RuntimeError(
                f"Checkpoint {model_path} is missing weights for {missing_weights}; "
                f"it does not match the {type(model).__name__} architecture. "
                "Predictions would be random — refusing to load."
            )
        model.eval()
        self.models[crop_name] = model
        return model

    def _prepare_image(self, image):
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        return self.transforms(image).unsqueeze(0).to(DEVICE)

    def detect_crop_species(self, image):
        """
        Run the gatekeeper model to identify which crop species the leaf
        belongs to. The gatekeeper's 14 output classes are plant species
        (GATEKEEPER_CLASS_TO_CROP); classes without a disease CNN (squash)
        are skipped, so the best supported species is returned.

        Returns:
            dict with predicted crop name, confidence, full probabilities,
            raw_top_crop and fallback flag
        """
        model = self._load_model(GATEKEEPER_CROP)
        img_tensor = self._prepare_image(image)

        with torch.no_grad():
            output = model(img_tensor)
            probabilities = torch.softmax(output, dim=1)[0]

        probs = probabilities.cpu()
        class_probs = [
            (crop_name, float(probs[index]))
            for index, crop_name in GATEKEEPER_CLASS_TO_CROP.items()
            if index < len(probs)
        ]
        ranked = sorted(class_probs, key=lambda item: item[1], reverse=True)
        raw_top_crop, _raw_top_conf = ranked[0]
        supported_ranking = [item for item in ranked if item[0] in SPECIES_CROPS]
        predicted_crop, confidence = supported_ranking[0]
        return {
            'predicted_crop': predicted_crop,
            'confidence': round(confidence, 4),
            'probabilities': {crop: round(prob, 4) for crop, prob in class_probs},
            'raw_top_crop': raw_top_crop,
            'fallback': raw_top_crop != predicted_crop,
        }

    def auto_detect_disease(self, image, lang="en"):
        """
        Two-stage gatekeeper pipeline:
          1. GatekeeperCNN classifies the leaf's crop species.
          2. The matching per-crop CropCNN classifies the disease.
        """
        routing = self.detect_crop_species(image)
        crop_name = routing['predicted_crop']
        if not crop_name:
            return {'error': 'Gatekeeper could not identify the crop species.'}

        result = self.detect_disease(crop_name, image, lang=lang)
        if 'error' in result:
            return result

        result['gatekeeper'] = routing
        return result

    def detect_disease(self, crop_name, image, lang="en"):
        """
        Detect disease for a specific crop from an image.
        
        Args:
            crop_name: Name of the crop (str)
            image: PIL Image object or path to image
            lang: 'en' or 'ne' — only affects recommendation/display text,
                  never the canonical predicted_label used for storage/logic.
            
        Returns:
            dict with disease class, confidence score, and class probabilities
        """
        if crop_name == GATEKEEPER_CROP:
            return {'error': 'The gatekeeper identifies the crop species only. Use crop "auto" for full disease detection.'}
        if crop_name not in CROP_NAMES:
            return {'error': f'Crop {crop_name} not supported'}

        model = self._load_model(crop_name)
        img_tensor = self._prepare_image(image)

        with torch.no_grad():
            output = model(img_tensor)  # (1, num_classes)
            probabilities = torch.softmax(output, dim=1)[0]  # (num_classes,)
            confidence, predicted_class = torch.max(probabilities, dim=0)
        
        confidence = confidence.item()
        predicted_class = predicted_class.item()
        probabilities = probabilities.cpu().numpy().tolist()
        class_names = DISEASE_CLASS_NAMES[crop_name]
        
        predicted_label = class_names[predicted_class]
        return {
            'crop': crop_name,
            'predicted_class': predicted_class,
            'predicted_label': predicted_label,
            'predicted_label_display': get_disease_label_display(predicted_label, lang=lang),
            'confidence': round(confidence, 4),
            'all_probabilities': probabilities,
            'class_labels': class_names,
            'num_classes': len(probabilities),
            'recommendation': get_disease_recommendation(predicted_label, lang=lang),
        }