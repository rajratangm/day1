import pandas as pd 
from pathlib import Path  
from matplotlib import pyplot as plt

class EDA:

    def __init__(self):
        path = Path('system_data.json')
        self.data = pd.read_json(path)
        self.data = self.data.drop(columns=['timestamp'])

    
    def _describe_data(self):
        return self.data.describe()
    
    def _plot_data(self):
        plot = plt.figure(figsize=(10, 10))
        plt.plot(self.data)
        plt.show()
        return plot
    
    def _save_png(self):
        plt = self._plot_data()
        plt.savefig('eda.pdf')
        plt.close()
    
    def _save_pdf(self):
        with open('eda.pdf', 'w') as f:
            f.write(self.data)
    
    def perform_eda(self): 
        val = self._describe_data()
        print(val)
        # self._save_png()
        # self._save_pdf()