# models/lstm_model.py
import torch.nn as nn


class RiceYieldLSTM(nn.Module):
    """LSTM over a place's historical annual rice yields; predicts the
    next season's yield (normalized)."""

    def __init__(self, input_size=1, hidden_size=64, num_layers=2, dropout=0.1):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        _out, (h_n, _c_n) = self.lstm(x)
        return self.fc(h_n[-1])
