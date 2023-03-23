from random import random,randint,choices
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import json

config = Config()
log = Log(config['app'])

class Darwin:
    
    def __init__(self,prefix,symbol,period,start,end):
        self.prefix = prefix
        self.symbol = symbol
        self.period = period
        self.start = start
        self.end = end
        self.pop = []
    
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