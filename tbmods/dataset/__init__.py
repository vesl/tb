from tbmods.config import Config
from tbmods.log import Log
import pandas as pd

config = Config()
log = Log(config['app'])

class Dataset:
    
    def __init__(self,period,start,end,features_map):
        self.period = period
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        self.features_map = features_map
        
    def index_datetime(self):
        pd_freqs = {'1m':'T','1h':'H','1d':'D'}
        if not self.period in pd_freqs: log.error('Period {} not managed'.format(self.period))
        index = pd.date_range(start=self.start,end=self.end,freq=pd_freqs[self.period])
        return index
        
    def handle_lag(self,name):
        return (name,0) if not '-' in name else (name.split('-'))