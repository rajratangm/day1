import psutil
import json
from datetime import datetime
from pathlib import Path 
class system_monitorying:

    def __init__(self):
        self.cpu_usage = psutil.cpu_percent(interval=1) 
        self.memory_usage = psutil.virtual_memory().percent
        self.disk_usage = psutil.disk_usage('/').percent
        self.network_usage = psutil.net_io_counters()
        self.network_usage_sent = self.network_usage.bytes_sent
        self.network_usage_received = self.network_usage.bytes_recv
        self.network_usage_total = self.network_usage.bytes_sent + self.network_usage.bytes_recv
        self.network_usage_percentage = (self.network_usage_total / 1000000000) * 100
        self.network_usage_percentage_sent = (self.network_usage_sent / 1000000000) * 100
        self.network_usage_percentage_received = (self.network_usage_received / 1000000000) * 100
        self.network_usage_percentage_total = (self.network_usage_total / 1000000000) * 100
        self.network_usage_percentage_sent = (self.network_usage_sent / 1000000000) * 100
        self.network_usage_percentage_received = (self.network_usage_received / 1000000000) * 100
        self.network_usage_percentage_total = (self.network_usage_total / 1000000000) * 100
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def get_cpu_usage(self):
        return self.cpu_usage
    
    @property
    def get_memory_usage(self):
        return self.memory_usage
    
    @property
    def get_disk_usage(self):
        return self.disk_usage
    
    def save_data(self):
        path = Path('system_data.json')
        if path.exists():
            with open(path, 'r') as f:
                records = json.load(f)
        else:
            records = []

        data = {**self.__dict__}
        records.append(data)

        with open(path,'w') as f:
            json.dump(records, f)

        



    