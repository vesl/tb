from tbmods.indicators.financial import Financial
from tbmods.triple_barrier import TripleBarrier
from tbmods.filters import Filters
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import numpy as np
import json

config = Config()
log = Log(config['app'])

class DatasetTech:

    def __init__(self,period,start,end,features_list):
        self.period = period
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        self.features = pd.DataFrame(index=self.create_index_datetime())
        self.features_list = features_list
        self.features_map_base = json.loads(config['tech_features'])
        self.features_map = self.create_features_map()
        self.candles = Candles()
        self.candles.from_questdb(self.period,self.start,self.end)
        self.financial = Financial(self.candles.candles)
        self.sources_map = {'ohlc': self.load_ohlc,'indicators': self.load_indicators}
        [self.load_features(name,props) for name,props in self.features_map.items()]
        self.load_labels()
        self.merge_indexes()
    
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
    
    def merge_indexes(self):
        self.index = self.features.index.intersection(self.labels.index)
        self.labels = self.labels.loc[self.index]
        self.features = self.features.loc[self.index]
        self.tbm = self.tbm.loc[self.index]
        self.cusum = self.cusum.loc[self.index]

    def load_features(self,name,props):
        log.info("Load feature {}".format(name))
        feature = self.sources_map[props['source']](props)
        if int(props['lag']) > 0: feature = feature.shift(int(props['lag']))
        if not eval(props['scaled']): feature = feature.pct_change()
        self.features = self.features.join(feature.rename(name))
        self.features.dropna(inplace=True)
        self.features = self.features[np.isfinite(self.features).all(1)]
        
    def load_labels(self):
        self.cusum = Filters(self.candles.candles.close).cusum_events(config['cusum_pct_threshold'])
        self.tbm = TripleBarrier(self.candles.candles.close,self.cusum).barriers
        self.labels = self.tbm.side
        
    def load_ohlc(self,props):
        return self.candles.candles[props['name']]
            
    def load_indicators(self,props):
        return self.financial.compute(props['name'])