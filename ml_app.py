from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
from pathlib import Path
import numpy as np
import pickle

FEATURE_COLS = ['cpu_usage', 'memory_usage', 'disk_usage', 'network_usage']


class ml_app:
    def __init__(self, data):
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100,
        )
        self.scaler = StandardScaler()
        self.data = data
        self._scaler_fitted = False

    def _get_feature_matrix(self, data):
        """Prepare numeric feature matrix. Same logic for train and predict."""
        df = data.copy() if hasattr(data, 'copy') else pd.DataFrame(data)
        if 'network_usage' in df.columns:
            df['network_usage'] = df['network_usage'].apply(
                lambda x: np.mean(x) if isinstance(x, (list, np.ndarray)) else x
            )
        return df[[c for c in FEATURE_COLS if c in df.columns]].astype(float)

    def train_model(self):
        X = self._get_feature_matrix(self.data)
        X_scaled = self.scaler.fit_transform(X)
        self._scaler_fitted = True
        self.model.fit(X_scaled)

    def predict(self, data=None):
        """Predict using same scaling as training."""
        if data is None:
            data = self.data
        X = self._get_feature_matrix(data)
        if self._scaler_fitted:
            X = self.scaler.transform(X)
        return self.model.predict(X)

    def save_model(self, path='model.pkl'):
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler, 'scaler_fitted': self._scaler_fitted}, f)

    @classmethod
    def load_model(cls, path='model.pkl', data=None):
        with open(path, 'rb') as f:
            obj = pickle.load(f)
        if isinstance(obj, dict):
            app = cls(data=pd.DataFrame() if data is None else data)
            app.model = obj['model']
            app.scaler = obj.get('scaler', StandardScaler())
            app._scaler_fitted = obj.get('scaler_fitted', False)
            return app
        app = cls(data=pd.DataFrame() if data is None else data)
        app.model = obj
        app._scaler_fitted = False
        return app
