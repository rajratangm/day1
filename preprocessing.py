import pandas as pd 
from pathlib import Path 
import numpy as np
from sklearn.preprocessing import StandardScaler


class Preprocessing:
    def __init__(self,data):
        self.data = data
        path = Path('system_data.json')
        self.data = pd.read_json(path)
    
    def _standardize_data(self,data):
        col = data.columns.tolist()
        data = StandardScaler().fit_transform(data)
        data = pd.DataFrame(data, columns=col)
        return data
    
    def _outlier_detection(self, data):
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        low = Q1 - 1.5 * IQR
        high = Q3 + 1.5 * IQR

        outliers = (data < low) | (data > high)
        outliers.sum().sort_values(ascending=False)   # count per column

        data = data[~outliers.any(axis=1)]
        return data
    
    def perform_preprocessing(self):
        self.data['network_usage'] = self.data['network_usage'].apply(lambda x: np.mean(x) if isinstance(x, (list, np.ndarray)) else x)
        data = self.data[['cpu_usage', 'memory_usage', 'disk_usage', 'network_usage', 'label']]
        data = self._outlier_detection(data)
        self.data = self._standardize_data(data)
        return self.data