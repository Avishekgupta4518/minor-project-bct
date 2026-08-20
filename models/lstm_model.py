# models/lstm_model.py
import torch.nn as nn

class YieldLSTM(nn.Module):
    def __init__(self, input_size=256, hidden_size=128, num_layers=2, dropout=0.3):
        super(YieldLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                            batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.regressor = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (batch, seq_len, input_size)
        lstm_out, (h_n, c_n) = self.lstm(x)
        # Use the last hidden state
        last_hidden = h_n[-1]   # (batch, hidden_size)
        return self.regressor(last_hidden)