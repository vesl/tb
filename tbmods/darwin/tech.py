from random import random,randint,choices
from tbmods.models.tech import ModelTech
from tbmods.darwin import Darwin
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import json

config = Config()
log = Log(config['app'])

class DarwinTech(Darwin):
    
    def __init__(self,symbol,period,start,end):
        super().__init__('tech',symbol,period,start,end)
        self.pop_size = 10
        self.lag_factor = 9
        self.arg_factor = 18
        self.current_gen = 0
        self.max_gen = 50
        self.n_estimators_factor = 200
        self.keep_best_features = 0.33
        self.max_features = 300
        
    def new_features(self):
        features_map = json.loads(config['ohlc_features'])
        features_map.update(json.loads(config['tech_features']))
        features = list(features_map.keys())
        lag = round(random()*self.lag_factor)+1
        features_list = []
        for feature in features:
            args = False
            if 'nb_args' in features_map[feature]: args = '.'.join([str(int((randint(2,self.arg_factor)/(i+1))+1)) for i in range(int(features_map[feature]['nb_args']))])
            for ilag in range(lag+1):
                if args: features_list.append('{}-{}-{}'.format(feature,ilag,args))
                else: features_list.append('{}-{}'.format(feature,ilag))
        features_list.sort()
        return features_list.copy()
        
    def new_id(self,genotype):
        model = ModelTech(self.symbol,self.period,self.start,self.end,genotype['features'])
        model.clf_init(genotype['config'])
        return model