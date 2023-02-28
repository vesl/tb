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

class DatasetTech:

    def __init__(self,symbol,period,start,end,features_list):
        self.symbol = symbol
        self.period = 'historical'
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        self.features = pd.DataFrame(index=pd.date_range(start=self.start,end=self.end,freq='H',tz='UTC'))
        self.features_list = features_list
        self.features_map = self.create_features_map()
        # klines
        self.klines = Klines(self.symbol,self.period)
        self.klines.load_df(self.start,self.end)
        # klines
        self.financial = Financial(self.klines.df)
        self.sources_map = {'ohlc': self.load_ohlc,'indicators': self.load_indicators}
        [self.load_features(name,props) for name,props in self.features_map.items()]
        self.load_labels()
        self.merge_indexes()
    
    def create_features_map(self):
        features_map = {}
        config_tech_features = json.loads(config['tech_features'])
        for feature in self.features_list:
            props = feature.split('-')
            name = props[0]
            lag = props[1]
            args = None if len(props) == 2 else props[2].split('.')
            if not name in config_tech_features: log.error('Feature {} does not exists in config tech_features'.format(name))
            feature_map = config_tech_features[name]
            feature_map['name'] = name
            feature_map['lag'] = lag
            feature_map['args'] = args
            features_map[feature] = feature_map.copy()
        return features_map

    def merge_indexes(self):
        self.index = self.features.index.intersection(self.labels.index)
        self.labels = self.labels.loc[self.index]
        self.full_features = self.features.copy()
        self.features = self.features.loc[self.index]
        self.tbm = self.tbm.loc[self.index]
        self.cusum = self.cusum.loc[self.index]

    def load_features(self,name,props):
        #log.info("Load feature {}".format(name))
        feature = self.sources_map[props['source']](props)
        if int(props['lag']) > 0: feature = feature.shift(int(props['lag']))
        if not eval(props['scaled']): feature = feature.pct_change()
        self.features = self.features.join(feature.rename(name))
        self.features.dropna(inplace=True)
        self.features = self.features[np.isfinite(self.features).all(1)]
        
    def load_labels(self):
        self.cusum = Filters(self.klines.df.close).cusum_events(config['cusum_pct_threshold'])
        self.tbm = TripleBarrier(self.klines.df.close,self.cusum).barriers
        self.labels = self.tbm.side
        
    def load_ohlc(self,props):
        return self.klines.df[props['name']]
            
    def load_indicators(self,props):
        return self.financial.compute(props['name'],props['args'])