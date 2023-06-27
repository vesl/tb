from tbmods.triple_barrier import TripleBarrier
from tbmods.features import Features
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd

config = Config()
log = Log(config['app'])

class Dataset:
    
    def __init__(self,name,start,end,symbol,period):
        self.name = name
        self.get_map()
        self.start = start
        self.end = end
        self.symbol = symbol
        self.period = period
        self.load_features()
        self.load_events()
        self.load_labels()

    def get_map(self):
        mongodb = MongoDB()
        try:
            self._map = mongodb.find('TB','datasets_maps',{'name':{'$eq':self.name}})[0]
        except IndexError:
            log.error("Can't find dataset named {} in mongo".format(self.name))
        mongodb.close()
        
    def get_features_map(self,features_map_name):
        mongodb = MongoDB()
        try:
            return mongodb.find('TB','features_maps',{'name':{'$eq':features_map_name}})[0]
        except IndexError:
            log.error("Can't find feature map named {} in mongo".format(features_map_name))
        mongodb.close()

    def load_features(self):
        self.features = pd.DataFrame()
        for features_map_name in self._map['features_maps']:
            features_map = self.get_features_map(features_map_name)
            features = Features(features_map,self.start,self.end,self.symbol,self.period)
            self.features = self.features.join(features.df,how='outer')
        self.features.index.name = None
        self.features.dropna(inplace=True)
    
    def load_events(self):
        chartist_features_map = self.get_features_map('talib_pattern_recognition')
        chartist_features = Features(chartist_features_map,self.start,self.end,self.symbol,self.period)
        self.events = chartist_features.df.loc[chartist_features.df.index.intersection(self.features.index)]
    
    def load_labels(self):
        triple_barrier = TripleBarrier(self.features['close!lag=0'],self.events)
        self.labels = triple_barrier.barriers.side