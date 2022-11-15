from tbmods.indicators.financial import Financial
from tbmods.triple_barrier import TripleBarrier
from tbmods.filters import Filters
from tbmods.candles import Candles
from tbmods.dataset import Dataset
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import numpy as np

config = Config()
log = Log(config['app'])

class DatasetTech(Dataset):
    
    def __init__(self,period,start,end,features_list):
        
        super().__init__(period,start,end,features_list,'tech')
        self.candles = Candles()
        self.candles.from_questdb(self.period,self.start,self.end)
        self.financial = Financial(self.candles.candles)
        self.sources_map = {'ohlc': self.load_ohlc,'indicators': self.load_indicators}
        [self.load_features(name,props) for name,props in self.features_map.items()]
        self.load_labels()
        self.merge_features_labels_indexes()
    
    def merge_features_labels_indexes(self):
        self.index = self.features.index.intersection(self.labels.index)
        self.labels = self.labels.loc[self.index]
        self.features = self.features.loc[self.index]

    def load_features(self,name,props):
        log.info("Load feature {}".format(name))
        feature = self.sources_map[props['source']](props)
        if int(props['lag']) > 0: feature = feature.shift(int(props['lag']))
        if not eval(props['scaled']): feature = feature.pct_change()
        self.features = self.features.join(feature.rename(name))
        self.features.dropna(inplace=True)
        self.features = self.features[np.isfinite(self.features).all(1)]
        
    def load_labels(self):
        cusum = Filters(self.candles.candles.close).cusum_events(config['cusum_pct_threshold'])
        self.labels = TripleBarrier(self.candles.candles.close,cusum).barriers.side
        
    def load_ohlc(self,props):
        return self.candles.candles[props['name']]
            
    def load_indicators(self,props):
        return self.financial.compute(props['name'])