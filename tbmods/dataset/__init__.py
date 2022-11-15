from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import json

config = Config()
log = Log(config['app'])

class Dataset:
    
    def __init__(self,period,start,end,features_list,dataset_type):
        self.period = period
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        self.features = pd.DataFrame(index=self.create_index_datetime())
        self.features_list = features_list
        self.dataset_type = dataset_type
        self.features_map_base = json.loads(config['{}_features'.format(self.dataset_type)])
        self.features_map = self.create_features_map()
        
    def create_index_datetime(self):
        pd_freqs = {'1m':'T','1h':'H','1d':'D'}
        if not self.period in pd_freqs: log.error('Period {} not managed'.format(self.period))
        index = pd.date_range(start=self.start,end=self.end,freq=pd_freqs[self.period],tz='UTC')
        return index
        
    def create_features_map(self):
        features_map = {}
        for feature in self.features_list:
            name, lag = (feature,0) if not '-' in feature else (feature.split('-'))
            if not name in self.features_map_base: log.error('Feature {} does not exists in features_map_base'.format(name))
            feature_map = self.features_map_base[name]
            feature_map['name'] = name
            feature_map['lag'] = lag
            features_map[feature] = feature_map.copy()
        return features_map