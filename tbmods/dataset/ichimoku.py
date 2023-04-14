from tbmods.indicators.ichimoku import Ichimoku
from tbmods.dataset import Dataset
from tbmods.config import Config
from tbmods.log import Log
import numpy as np
import itertools
import json

config = Config()
log = Log(config['app'])

class DatasetIchimoku(Dataset):

    def __init__(self,symbol,period,start,end,features_list):
        super().__init__('ichimoku',symbol,period,start,end,features_list)

    def load_features(self):
        lag_args = []
        for name,props in self.features_map.items():
            if props['args'] is None: continue
            lag_arg = [int(props['lag'][0]),int(props['args'][0])]
            if not lag_arg in lag_args: lag_args.append(lag_arg)
        for lag_arg in lag_args:
            features = Ichimoku(self.klines,lag_arg[0],lag_arg[1]).df
            self.features = self.features.join(features)
        self.features.dropna(inplace=True)

    def create_features_map(self):
        features_map = {}
        config_features = json.loads(config['ohlc_features'])
        config_features.update(json.loads(config['{}_features'.format(self.prefix)]))
        for feature in self.features_list:
            props = feature.split('-')
            name = props[0]
            lag = props[1]
            if name == 'price_state': continue ##a jarter et sur servir du parent
            args = None if len(props) == 2 else props[2].split('.')
            if not name in config_features: log.error('Feature {} does not exists in config {}_features'.format(name,self.prefix))
            feature_map = config_features[name]
            feature_map['name'] = name
            feature_map['lag'] = lag
            feature_map['args'] = args
            features_map[feature] = feature_map.copy()
        return features_map