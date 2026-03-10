## System Monitoring Anomaly Detection with Isolation Forest

This project is a small end-to-end **system monitoring + anomaly detection** pipeline built in Python. It:

- Collects system metrics (CPU, memory, disk, network) using `psutil`
- Stores time-stamped snapshots in `system_data.json`
- Explores and understands the data in a Jupyter notebook (`eda.ipynb`)
- Preprocesses features (cleaning, outlier handling, scaling)
- Trains an **Isolation Forest** model to detect anomalous system states
- Saves the trained model and scaler for consistent predictions

For a detailed, narrative explanation of the model and pipeline, see the accompanying Medium article:

- **Medium:** [Building a System Monitoring Anomaly Detector with Isolation Forest](https://medium.com/p/38d5b3a6b3e3?postPublishedType=initial)

---

## Project Structure

- `app.py`  
  Collects a single snapshot of system metrics using `psutil` and appends it to `system_data.json`.

- `system_data.json`  
  JSON array of historical system snapshots. Each record includes:
  - `cpu_usage`, `memory_usage`, `disk_usage`
  - `network_usage` (raw, list-like from `psutil`), plus derived totals/percentages
  - `timestamp`
  - `label` (0/1) – a simple heuristic label added for experimentation and evaluation

- `eda.ipynb`  
  Exploratory Data Analysis notebook:
  - Cleans `network_usage` (list → numeric)
  - Computes descriptive statistics and correlations
  - Plots distributions, KDEs, scatter matrices, box plots
  - Investigates outliers (IQR, Q–Q plots) and scale differences
  - Experiments with scaling (e.g. `StandardScaler`) and train/test splitting

- `preprocessing.py`  
  Preprocessing utilities:
  - Convert list-like `network_usage` into a numeric scalar
  - Select relevant numeric columns (including `label` when needed)
  - IQR-based outlier filtering
  - Optional standardization with `StandardScaler`

- `ml_app.py`  
  Model application and pipeline:
  - Builds a numeric feature matrix from the raw DataFrame
  - Fits a `StandardScaler` and an `IsolationForest` model
  - Uses the same scaler for prediction (avoids train/predict scale mismatch)
  - Saves both model and scaler together to `model.pkl`
  - Provides a `load_model` classmethod for reusing the trained model

- `main.py`  
  Example entry point:
  - Loads `system_data.json`
  - Trains the Isolation Forest model on historical data
  - Prints inlier/outlier counts on the training set
  - Runs predictions on a small sample of manually specified snapshots

- `requirements.txt`  
  Python dependencies for reproducing the environment.

- `eda.py`, `system_data.txt`  
  Additional utilities and raw data notes used during development and EDA.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/day1.git
cd day1
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # macOS / Linux
# .\venv\Scripts\activate   # Windows (PowerShell)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Collect system metrics

Run `app.py` (or integrate it into a scheduler like cron) to append one snapshot to `system_data.json`:

```bash
python app.py
```

Over time, this builds up a history of system metrics suitable for EDA and modeling.

### 2. Explore the data (EDA)

Open the notebook in Jupyter:

```bash
jupyter notebook eda.ipynb
```

Use the notebook to:
- Inspect distributions and correlations
- Understand typical vs atypical system states
- Try out alternative preprocessing or feature engineering ideas

### 3. Train the Isolation Forest model

`main.py` demonstrates how to train the model on the collected data:

```bash
python main.py
```

Typical output includes:

- **Training data:** number of inliers and outliers detected by the model  
- **Sample predictions:** model output (`1` = inlier/normal, `-1` = outlier/anomaly) on a few example points

During training:
- The feature matrix is built from `cpu_usage`, `memory_usage`, `disk_usage`, and a numeric `network_usage`
- Features are standardized with `StandardScaler`
- `IsolationForest` is fit on the scaled features
- The fitted model and scaler are saved together to `model.pkl`

### 4. Predict on new snapshots

To get anomaly predictions on new data:

1. Collect new snapshots into `system_data.json`, or prepare a small `pandas.DataFrame` with the same feature columns.
2. Load the trained model and scaler (using the `load_model` helper in `ml_app.py`).
3. Build the feature matrix, apply the scaler, and call `model.predict(X)`.

For example (in a Python shell or script):

```python
import pandas as pd
from ml_app import ml_app

# Load raw data (or new samples)
data = pd.read_json("system_data.json")

# Load trained model + scaler
app = ml_app.load_model(path="model.pkl", data=data)

# Predict anomalies on the full dataset
preds = app.predict()
print("Anomaly predictions (1=normal, -1=outlier):", preds)
```

---

## Notes on Modeling and Drift

- **Unsupervised:** Isolation Forest does not require labels; it infers what is “normal” from the data distribution.
- **Contamination:** The `contamination` parameter (e.g. `0.1`) roughly controls the fraction of points treated as anomalies.
- **Feature scaling:** Standardizing features is important so that high-magnitude features (like network byte counts) do not dominate splits.
- **Concept drift:** If `system_data.json` grows over time as the system evolves, the definition of “normal” changes. In practice, you should:
  - Retrain the model periodically (daily/weekly) or when enough new data has accumulated.
  - Consider training on a rolling window (e.g. last N days) to focus on recent behavior.

For deeper discussion of Isolation Forest, feature scaling, and the complete pipeline, refer to the Medium article linked above.

---

## Contact

- **Email:** rajratangulab.more@gmail.com  
- **GitHub:** [@rajratanm](https://github.com/rajratanm)

