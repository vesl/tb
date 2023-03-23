from tbmods.dataset import Dataset
from tbmods.config import Config
from tbmods.log import Log
import numpy as np

config = Config()
log = Log(config['app'])

class DatasetTech(Dataset):

    def __init__(self,symbol,period,start,end,features_list):
        super().__init__('tech',symbol,period,start,end,features_list)
        
    def load_features(self):
        for name,props in self.features_map.items():
            if name in self.features.columns: continue
            feature = self.sources_map[props['source']](props)
            if int(props['lag']) > 0: feature = feature.shift(int(props['lag']))
            if not eval(props['scaled']): feature = feature.pct_change()
            self.features = self.features.join(feature.rename(name))
        self.features.dropna(inplace=True)
        self.features = self.features[np.isfinite(self.features).all(1)]