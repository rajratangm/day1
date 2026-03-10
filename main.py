from app import system_monitorying
from eda import EDA
from ml_app import ml_app
from pathlib import Path
import pandas as pd

if __name__ == "__main__":
    path = Path('system_data.json')
    data = pd.read_json(path)
    app = ml_app(data)
    app.train_model()

    # Predictions on full dataset (same scale as training)
    preds = app.predict()
    n_inlier = (preds == 1).sum()
    n_outlier = (preds == -1).sum()
    print(f"Training data: {n_inlier} inliers, {n_outlier} outliers (1=normal, -1=outlier)")

    # Sample new points for prediction (use similar scale as your data)
    X_test = pd.DataFrame([
        [45.0, 72.0, 44.0, 4.1e8],
        [88.0, 95.0, 48.0, 4.2e8],
        [5.0, 65.0, 6.0, 4.0e8],
    ], columns=["cpu_usage", "memory_usage", "disk_usage", "network_usage"])
    sample_preds = app.predict(X_test)
    print("Sample predictions (1=normal, -1=outlier):", sample_preds.tolist())

    app.save_model()
    