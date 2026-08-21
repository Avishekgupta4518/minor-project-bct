# models/lstm_model.py
import torch
import torch.nn as nn


class YieldLSTM(nn.Module):
    def __init__(self, input_size=4, hidden_size=64, num_layers=2, dropout=0.3):
        super(YieldLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                            batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.regressor = nn.Sequential(
            nn.Linear(hidden_size + input_size, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        lstm_out, (h_n, c_n) = self.lstm(x)
        last_hidden = h_n[-1]
        seasonal_weather = x.mean(dim=1)
        return self.regressor(torch.cat((last_hidden, seasonal_weather), dim=1))


class SpatialPaddyLSTM(nn.Module):
    """Architecture matching models/spatial_paddy_lstm_final.pth."""

    def __init__(self, input_size=33, hidden_size=128, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x, return_hidden=False):
        _lstm_out, (h_n, _c_n) = self.lstm(x)
        last_hidden = h_n[-1]
        yield_norm = self.fc(last_hidden)
        if return_hidden:
            return yield_norm, last_hidden
        return yield_norm


class BuddyFusionNet(nn.Module):
    """Small MLP that joins plant-health (CNN) signals with LSTM yield."""

    def __init__(self, input_size=12, hidden_size=32, dropout=0.15):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.net(x)