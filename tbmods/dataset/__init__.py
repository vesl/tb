from tbmods.dataset.indicators import Indicators
from tbmods.candles import Candles
from tbmods.config import Config
import pandas as pd
import json

config = Config()

class Dataset:
    
    def __init__(self,timescale,from_date,to_date,features):
        self.timescale = timescale
        self.from_date = from_date
        self.to_date = to_date
        self.features = features
        self.sources = json.loads(config['features'])['sources']
        
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