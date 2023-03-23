from tbmods.dataset import Dataset
from tbmods.config import Config
from tbmods.log import Log
import numpy as np
import json

config = Config()
log = Log(config['app'])

class DatasetIchimoku(Dataset):

    def __init__(self,symbol,period,start,end,features_list):
        super().__init__('ichimoku',symbol,period,start,end,features_list)

    def load_features(self):
        for name,props in self.features_map.items():
            if name in self.features.columns: continue
            feature = self.sources_map[props['source']](props)
            if int(props['lag']) > 0: 
                feature = feature.shift(int(props['lag']))
                price = self.klines.df.close.shift(int(props['lag']))
            else: price = self.klines.df.close
            if props['source'] == 'indicators':
                price_state =  price / feature
                self.features = self.features.join(price_state.rename('price_state-{}'.format(name)))
            if not eval(props['scaled']): feature = feature.pct_change()
            self.features = self.features.join(feature.rename(name))
        self.features.dropna(inplace=True)
        self.features = self.features[np.isfinite(self.features).all(1)]

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