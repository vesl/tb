from tbmods.indicators.financial import Financial
from tbmods.triple_barrier import TripleBarrier
from tbmods.filters import Filters
from tbmods.klines import Klines
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import numpy as np
import json

config = Config()
log = Log(config['app'])

class Dataset:

    def __init__(self,prefix,symbol,period,start,end,features_list):
        self.prefix = prefix
        self.symbol = symbol
        self.period = period
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        self.features_list = features_list
        self.features = pd.DataFrame(index=pd.date_range(start=self.start,end=self.end,freq='H',tz='UTC'))
        self.klines = Klines(self.symbol,self.period)
        self.klines.load_df(self.start,self.end)
        self.financial = Financial(self.klines.df)
        self.cusum = Filters(self.klines.df.close).cusum_events(config['cusum_pct_threshold'])
        self.features_map = self.create_features_map()
        self.sources_map = {
            'ohlc': self.load_ohlc,
            'indicators': self.load_indicators
        }
    
    def create_features_map(self):
        features_map = {}
        config_features = json.loads(config['ohlc_features'])
        config_features.update(json.loads(config['{}_features'.format(self.prefix)]))
        for feature in self.features_list:
            props = feature.split('-')
            name = props[0]
            lag = props[1]
            args = None if len(props) == 2 else props[2].split('.')
            if not name in config_features: log.error('Feature {} does not exists in config {}_features'.format(name,self.prefix))
            feature_map = config_features[name]
            feature_map['name'] = name
            feature_map['lag'] = lag
            feature_map['args'] = args
            features_map[feature] = feature_map.copy()
        return features_map

    def merge_indexes(self):
        self.index = self.features.index.intersection(self.labels.index)
        self.labels = self.labels.loc[self.index]
        self.features = self.features.loc[self.index]
        self.tbm = self.tbm.loc[self.index]
        self.cusum = self.cusum.loc[self.index]
        
    def load_labels(self):
        self.tbm = TripleBarrier(self.klines.df.close,self.cusum).barriers
        self.labels = self.tbm.side
        self.merge_indexes()
        
    def load_ohlc(self,props):
        return self.klines.df[props['name']]
            
    def load_indicators(self,props):
        return self.financial.compute(props['name'],props['args'])