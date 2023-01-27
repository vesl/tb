from tbmods.models.tech import ModelTech
from tbmods.log import Log
from tbmods.config import Config
from random import random,randint,choices
import pandas as pd
import json

config = Config()
log = Log(config['app'])

class DarwinTech:
    
    def __init__(self,period,start,end):
        self.period = period
        self.start = start
        self.end = end
        self.pop_size = 20
        self.lag_factor = 18
        self.current_gen = 0
        self.max_gen = 50
        self.n_estimators_factor = 500
        self.keep_best_features = 0.33
        self.max_features = 200
        self.pop = []
        
    def new_features(self):
        features_map = json.loads(config['tech_features'])
        features = list(features_map.keys())
        lag = round(random()*self.lag_factor)+1
        features_list = []
        for feature in features:
            args = False
            if 'nb_args' in features_map[feature]: args = '.'.join([str(int((randint(2,18)/(i+1))+1)) for i in range(int(features_map[feature]['nb_args']))])
            for ilag in range(lag+1):
                if args: features_list.append('{}-{}-{}'.format(feature,ilag,args))
                else: features_list.append('{}-{}'.format(feature,ilag))
        features_list.sort()
        return features_list.copy()
        
    def new_random_genotype(self):
        n_estimators = round(random()*self.n_estimators_factor)+1
        features = self.new_features()
        return {
            "features": features,
            "config": {
                "n_estimators":n_estimators,
                "oob_score":True,
                "n_jobs":-1,
                "verbose":1,
                "class_weight":"balanced",
                "random_state":42
            }
        }
        
    def new_id(self,genotype):
        tech_model = ModelTech(self.period,self.start,self.end,genotype['features'])
        tech_model.clf_init(genotype['config'])
        return tech_model
        
    def fill_pop(self):
        while len(self.pop)<self.pop_size:
            genotype = self.new_random_genotype()
            new_id = self.new_id(genotype)
            self.pop.append(new_id)
        
    def train_pop(self):
        for i in self.pop:
            i.load_dataset()
            i.fit()
            i.meta['score']['f1_score_mean'] = sum(i.meta['score']['f1_score'])/len(i.meta['score']['f1_score'])
            del i.dataset
    
    def rank_pop(self):
        self.pop = sorted(self.pop.copy(),key=lambda i: i.meta['score']['f1_score_mean'],reverse=True)
        
    def orgy(self):
        old_pop = self.pop.copy()
        self.pop = []
        while len(old_pop) > 2:
            male = old_pop[0]
            female = old_pop[2]
            child = self.fuck(male,female)
            self.pop.append(child)
            del old_pop[0]
            del old_pop[1]
    
    def fuck(self,male,female):
        feature_importances = pd.concat([pd.Series(json.loads(male.meta['score']['feature_importances'])),pd.Series(json.loads(female.meta['score']['feature_importances']))]).sort_values(ascending=False)
        best_features = list(set(list(feature_importances.index[:round(len(feature_importances)*self.keep_best_features)])))
        features = best_features + self.new_features()
        if len(features) > self.max_features: features = features[:self.max_features]
        features = list(set(features))
        n_estimators_male = male.meta['clf_config']['n_estimators']
        n_estimators_female = male.meta['clf_config']['n_estimators']
        n_estimators = (n_estimators_male+n_estimators_female)/2
        genotype = {
            "features": features,
            "config": {
                "n_estimators":n_estimators,
                "oob_score":True,
                "n_jobs":-1,
                "verbose":1,
                "class_weight":"balanced",
                "random_state":42
            }
        }
        return self.new_id(genotype)
        
    def evolve(self):
        while self.current_gen < self.max_gen:
            log.info('Generation {}'.format(self.current_gen))
            self.fill_pop()
            self.train_pop()
            self.rank_pop()
            self.pop[0].save_meta()
            self.orgy()
            self.current_gen += 1