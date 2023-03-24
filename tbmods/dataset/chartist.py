from tbmods.dataset import Dataset
from tbmods.config import Config
from tbmods.log import Log
import numpy as np
import json

config = Config()
log = Log(config['app'])

class DatasetChartist(Dataset):

    def __init__(self,symbol,period,start,end,features_list):
        super().__init__('chartist',symbol,period,start,end,features_list)

    def load_features(self):
        print(len(self.features))
        for name,props in self.features_map.items():
            props['args'] = 0 # a degager c'est degueulasse
            feature = self.sources_map[props['source']](props)
            self.features = self.features.join(feature.rename(name))
        self.features.dropna(inplace=True)
        self.features.loc[~(self.features==0).all(axis=1)]

    def create_features_map(self):
        features_map = {}
        config_features = json.loads(config['{}_features'.format(self.prefix)])
        for feature in self.features_list:
            props = feature.split('-')
            name = props[0]
            if not name in config_features: log.error('Feature {} does not exists in config {}_features'.format(name,self.prefix))
            feature_map = config_features[name]
            feature_map['name'] = name
            features_map[feature] = feature_map.copy()
        return features_map