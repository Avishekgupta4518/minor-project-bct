# train_lstm.py
import numpy as np
import torch
import torch.optim as optim
from pathlib import Path
from sklearn.metrics import mean_squared_error, r2_score
from torch.utils.data import DataLoader

from config import DEVICE, WEATHER_FEATURES, WEATHER_LSTM_MODEL_PATH
from generate_synthetic_yield_data import ensure_dataset
from models.lstm_model import YieldLSTM
from utils.data_loader import YieldDataset

RANDOM_SEED = 42
torch.manual_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)

# Make sure the yield dataset is present before training.
ensure_dataset(min_rows=120)

base_dir = Path(__file__).resolve().parent
csv_file = base_dir / "data" / "yield_data.csv"
dataset = YieldDataset(csv_file)

dataset_size = len(dataset)
if dataset_size < 2:
    raise ValueError(
        "Yield training data is missing or too small. Populate data/yield_data.csv with at least two rows before training."
    )

train_size = int(0.8 * dataset_size)
val_size = dataset_size - train_size
split_generator = torch.Generator().manual_seed(RANDOM_SEED)
train_dataset, val_dataset = torch.utils.data.random_split(
    dataset, [train_size, val_size], generator=split_generator
)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

model = YieldLSTM(input_size=len(WEATHER_FEATURES), hidden_size=64, num_layers=2).to(DEVICE)
criterion = torch.nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)

best_rmse = float('inf')
patience = 10
patience_counter = 0

for epoch in range(1, 81):
    model.train()
    train_loss = 0.0
    for X, y in train_loader:
        X, y = X.to(DEVICE), y.to(DEVICE)
        optimizer.zero_grad()
        pred = model(X)
        loss = criterion(pred.squeeze(), y)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * X.size(0)

    model.eval()
    val_preds, val_targets = [], []
    val_loss = 0.0
    with torch.no_grad():
        for X, y in val_loader:
            X, y = X.to(DEVICE), y.to(DEVICE)
            pred = model(X)
            loss = criterion(pred.squeeze(), y)
            val_loss += loss.item() * X.size(0)
            val_preds.extend(pred.cpu().numpy().flatten())
            val_targets.extend(y.cpu().numpy().flatten())

    val_loss /= len(val_dataset)
    rmse = np.sqrt(mean_squared_error(val_targets, val_preds))
    r2 = r2_score(val_targets, val_preds)
    baseline_preds = np.full(len(val_targets), np.mean(val_targets))
    baseline_rmse = np.sqrt(mean_squared_error(val_targets, baseline_preds))

    print(
        f"Epoch {epoch:2d} | Train Loss: {train_loss/len(train_dataset):.6f} "
        f"| Val Loss: {val_loss:.6f} | RMSE: {rmse:.4f} "
        f"| Baseline RMSE: {baseline_rmse:.4f} | R²: {r2:.4f}"
    )

    scheduler.step(val_loss)

    if rmse < best_rmse:
        best_rmse = rmse
        patience_counter = 0
        torch.save(model.state_dict(), WEATHER_LSTM_MODEL_PATH)
        print("   -> New best model saved.")
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print("Early stopping.")
            break

print(f"Training complete. Best validation RMSE: {best_rmse:.4f}")
print(f"Model saved to: {WEATHER_LSTM_MODEL_PATH}")