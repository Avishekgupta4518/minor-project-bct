# models/cnn_arch.py
import torch
import torch.nn as nn
import torch.nn.functional as F


class GatekeeperCNN(nn.Module):
    def __init__(self, num_classes):
        super(GatekeeperCNN, self).__init__()
        try:
            import timm
        except ImportError as exc:
            raise ImportError(
                "timm is required to load the gatekeeper checkpoint. Install it with `pip install timm`."
            ) from exc

        self.backbone = timm.create_model(
            "efficientnet_b0",
            pretrained=False,
            num_classes=num_classes,
        )
        # The shipped gatekeeper.pth stores its head as classifier.1.*
        # (nn.Sequential[Dropout, Linear]). Rebuild that exact layout,
        # otherwise load_state_dict(strict=False) silently drops the trained
        # classifier weights and leaves a randomly initialized head behind.
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(getattr(self.backbone, "drop_rate", 0.2)),
            nn.Linear(self.backbone.num_features, num_classes),
        )

    def forward(self, x, return_features=False):
        features = self.backbone.forward_features(x)
        pooled = self.backbone.global_pool(features)
        if pooled.ndim == 4:
            pooled = torch.flatten(pooled, 1)

        if return_features:
            if pooled.size(1) >= 256:
                return pooled[:, :256]
            padding = pooled.new_zeros(pooled.size(0), 256 - pooled.size(1))
            return torch.cat([pooled, padding], dim=1)

        return self.backbone.classifier(pooled)
    
    def load_state_dict(self, state_dict, strict=False):
        """
        Load state dict with backbone prefix handling.
        The saved checkpoint doesn't have 'backbone.' prefix, but the model does.
        Uses non-strict loading to handle classifier architecture differences.
        """
        # Check if checkpoint has backbone prefix
        has_backbone_prefix = any(k.startswith('backbone.') for k in state_dict.keys())
        
        if not has_backbone_prefix:
            # Add backbone prefix to all keys
            new_state_dict = {}
            for k, v in state_dict.items():
                new_state_dict[f'backbone.{k}'] = v
            state_dict = new_state_dict
        
        # Load with strict=False to ignore classifier architecture differences
        return super().load_state_dict(state_dict, strict=strict)

class CropCNN(nn.Module):
    """
    Simple 3-layer CNN for crop disease classification.
    Matches the saved checkpoint architecture from trained models.
    
    Input: (batch, 3, 224, 224)
    Output: (batch, num_classes)
    """
    def __init__(self, num_classes):
        super(CropCNN, self).__init__()
        # Convolutional layers with max pooling
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        
        # Max pooling
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # After 3 pooling operations on 224x224 input:
        # 224 -> 112 -> 56 -> 28
        # Flattened: 64 * 28 * 28 = 50176
        self.fc1 = nn.Linear(64 * 28 * 28, 256)
        self.fc2 = nn.Linear(256, num_classes)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x, return_features=False):
        # Conv block 1
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        
        # Conv block 2
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        
        # Conv block 3
        x = self.conv3(x)
        x = self.relu(x)
        x = self.pool(x)
        
        # Flatten and fully connected
        x = x.view(x.size(0), -1)  # (batch, 50176)
        x = self.fc1(x)  # (batch, 256)
        x = self.relu(x)
        x = self.dropout(x)
        
        if return_features:
            return x  # Return 256-dim feature vector
        
        x = self.fc2(x)  # (batch, num_classes)
        return x