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
        talib_features = [feature for feature in self.sources['talib'] if feature in self.features]
        df_qdb_features = self.load_qdb_features()
        df_talib_features = self.load_talib_features(df_qdb_features,talib_features)
        if len(df_talib_features) > 0: return df_qdb_features.join(df_talib_features,how='inner')
        else: return df_qdb_features
        
    def load_qdb_features(self):
        candles = Candles()
        candles.from_questdb(self.timescale,self.from_date,self.to_date)
        return candles.candles
        
    def load_talib_features(self,df_qdb_features,talib_features):
        indicators = Indicators(df_qdb_features)
        for talib_feature in talib_features:
            indicators.load(talib_feature)
        df_talib_features = indicators.candles.drop(df_qdb_features.columns,axis=1)
        return df_talib_features