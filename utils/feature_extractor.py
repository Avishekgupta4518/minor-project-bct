# utils/feature_extractor.py
import torch
from torchvision import transforms
from PIL import Image

from config import CROP_NAMES, DISEASE_CLASS_NAMES, NUM_DISEASE_CLASSES, CNN_MODEL_PATHS, DEVICE
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
        model.load_state_dict(checkpoint)
        model.eval()
        self.models[crop_name] = model
        return model

    def extract_features(self, image_dict):
        """
        image_dict: {crop_name: PIL.Image or image path}
        Returns: tensor of shape (1, num_crops, feature_dim) where feature_dim = 256
        """
        feature_list = []
        for crop in CROP_NAMES:
            img = image_dict.get(crop)
            if img is None:
                feat = torch.zeros(256)  # default zero vector
            else:
                model = self._load_model(crop)
                if isinstance(img, str):
                    img = Image.open(img).convert('RGB')
                img_tensor = self.transforms(img).unsqueeze(0).to(DEVICE)
                with torch.no_grad():
                    feat = model(img_tensor, return_features=True).squeeze(0).cpu()
            feature_list.append(feat)
        # Stack to shape (1, num_crops, 256)
        features = torch.stack(feature_list).unsqueeze(0)  # (1, 12, 256)
        return features

    def detect_disease(self, crop_name, image):
        """
        Detect disease for a specific crop from an image.
        
        Args:
            crop_name: Name of the crop (str)
            image: PIL Image object or path to image
            
        Returns:
            dict with disease class, confidence score, and class probabilities
        """
        if crop_name not in CROP_NAMES:
            return {'error': f'Crop {crop_name} not supported'}

        model = self._load_model(crop_name)

        if isinstance(image, str):
            image = Image.open(image).convert('RGB')

        img_tensor = self.transforms(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            output = model(img_tensor)  # (1, num_classes)
            probabilities = torch.softmax(output, dim=1)[0]  # (num_classes,)
            confidence, predicted_class = torch.max(probabilities, dim=0)
        
        confidence = confidence.item()
        predicted_class = predicted_class.item()
        probabilities = probabilities.cpu().numpy().tolist()
        class_names = DISEASE_CLASS_NAMES[crop_name]
        
        return {
            'crop': crop_name,
            'predicted_class': predicted_class,
            'predicted_label': class_names[predicted_class],
            'confidence': round(confidence, 4),
            'all_probabilities': probabilities,
            'class_labels': class_names,
            'num_classes': len(probabilities)
        }