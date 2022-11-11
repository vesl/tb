from tbmods.dataset.indicators import Indicators
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import json

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

class DatasetTech(Dataset):
    
    def __init__(self,period,start,end,features):
        super().__init__(period,start,end,features)
        self.features = pd.DataFrame(index=self.index_datetime())
        [self.load(name,props) for name,props in self.features_map.items()]
    
    def load(self,name,props):
        
        # compute lag
        props['lag'] = 0 if not '-' in name else name.split('-')[1]
        name = name if not '-' in name else name.split[0]
        
        log.info("Load feature {} lag {} source {} scaled {}".format(name,props['lag'],props['source'],props['scaled']))
        
"""
    def load(self):
        prev_features = [feature for feature in self.features if '-' in feature]
        talib_features = set([feature.split('-')[0] for feature in self.features if feature.split('-')[0] in self.sources['talib']])
        df_qdb_features = self.load_qdb_features()
        df_talib_features = self.load_talib_features(df_qdb_features,talib_features)
        if len(df_talib_features) > 0: df_features = df_talib_features
        else: df_features = df_qdb_features 
        if len(prev_features) > 0: df_features = self.load_prev_features(df_features,prev_features)
        try:
            return df_features.loc[:,self.features]
        except KeyError:
            return df_features
        
    def load_qdb_features(self):
        candles = Candles()
        candles.from_questdb(self.timescale,self.from_date,self.to_date)
        return candles.candles
        
    def load_talib_features(self,df_qdb_features,talib_features):
        indicators = Indicators(df_qdb_features)
        for talib_feature in talib_features:
            indicators.load(talib_feature)
        return indicators.candles
        
    def load_prev_features(self,df_features,prev_features):
        for feature in prev_features:
            split = feature.split('-')
            df_features = df_features.join(df_features[split[0]].shift(int(split[1])).rename('-'.join(split)))
        return df_features
"""