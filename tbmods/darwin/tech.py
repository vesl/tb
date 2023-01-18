from tbmods.models.tech import ModelTech
from tbmods.log import Log
from tbmods.config import Config
from random import random,choices
import pandas as pd
import json

config = Config()
log = Log(config['app'])

class DarwinTech:
    
    def __init__(self,period,start,end):
        self.period = period
        self.start = start
        self.end = end
        self.pop_size = 10 # a augmenter après les tests
        self.lag_factor = 50 # a augmenter après les tests
        self.cut_features_thresh = 0.3 # a diminuer après les tests
        self.current_gen = 0
        self.max_gen = 300
        self.n_estimators_factor = 500
        self.pop = []

    def new_random_genotype(self):
        features = config['tech_features_selected'].split(',')
        if random() < self.cut_features_thresh: features = list(dict.fromkeys(choices(features,k=round(len(features)*random())+1)))
        lag = round(random()*self.lag_factor)+1
        [features.extend(['{}-{}'.format(feature,ilag) for ilag in range(1,lag+1)]) for feature in features.copy()]
        features.sort()
        n_estimators = round(random()*self.n_estimators_factor)+1
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
            self.pop.append(self.new_id(self.new_random_genotype()))
        
    def train_pop(self):
        for i in self.pop:
            i.load_dataset()
            i.fit()
            i.meta['score']['f1_score_mean'] = sum(i.meta['score']['f1_score'])/len(i.meta['score']['f1_score'])
            del i.dataset
    
    def rank_pop(self):
        self.pop = sorted(self.pop.copy(),key=lambda i: i.meta['score']['f1_score_mean'],reverse=True)
        
    def orgy(self):
        old_pop = self.pop
        self.pop = []
        while len(old_pop) > 2:
            male = old_pop[0]
            female = old_pop[2]
            del old_pop[0]
            del old_pop[1]
            self.pop.append(self.fuck(male,female))
    
    def fuck(self,male,female):
        male_features_feature_importances = pd.Series(json.loads(male.meta['score']['feature_importances'])).sort_values(ascending=False) 
        female_features_feature_importances = pd.Series(json.loads(female.meta['score']['feature_importances'])).sort_values(ascending=False)
        best_male_features_feature_importances = male_features_feature_importances.index[:round(len(male_features_feature_importances)/2)]
        best_female_features_feature_importances = female_features_feature_importances.index[:round(len(female_features_feature_importances)/2)]
        features = list(set(list(best_male_features_feature_importances) + list(best_female_features_feature_importances)))
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