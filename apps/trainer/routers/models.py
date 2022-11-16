from sklearn.ensemble import RandomForestClassifier
from fastapi import APIRouter, HTTPException
from tbmods.dataset.tech import DatasetTech
from tbmods.models.tech import Tech
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import pandas as pd
import numpy as np
import requests
import json

router = APIRouter(
    prefix="/models",
    tags=["models"],
)

config = Config()
log = Log(config['app'])

@router.get('/grid_search/tech/{period}/{start}/{end}')
def grid_search_tech(period,start,end):
    
    # Get all available features list for this model
    features_list = list(json.loads(config['tech_features']).keys())
    # Generate features list with lag
    for feature in features_list.copy():
        for lag in range(1,config['tech_grid_search_lag']+1):
            features_list.append('{}-{}'.format(feature,lag))
    # Generate dataset
    dataset = DatasetTech(period,start,end,features_list)

    # GRID SEARCH
    results = []
    while len(features_list) >= 5:
        result = {}
        dataset.features = dataset.features.loc[:,features_list]
        y = dataset.labels
        X = dataset.features
        clf = Tech(RandomForestClassifier(
            n_estimators=300,
            oob_score=True,
            n_jobs=-1,
            verbose=1,
            class_weight='balanced',
            random_state=42,
        ),X,y,features_list)
        result['features'] = features_list
        result['cv_scores'] = clf.cv()
        clf.fit()
        result['f1_score'] = clf.f1_score()
        result['cm'] = clf.confusion_matrix()
        result['fi'] = clf.feature_importances()
        features_list =  result['fi'].iloc[:-6].index.tolist()
        results.append(result)
    
    # GET BEST RESULT
    best_result = {}
    for result in results:
        print(result['f1_score'])
        if any(f1 < 0.5 for f1 in result['f1_score']): continue
        avg = sum(result['f1_score'])/3
        if not 'avg' in best_result or best_result['avg'] < avg:
            best_result = result
            best_result['avg'] = avg
    print("BEST RESULT")
    print("FEATURES : {}".format(list(best_result['features'])))
    print("CV_SCORES : {}".format(list(best_result['cv_scores'])))
    print("F1_SCORE : {}".format(list(best_result['f1_score'])))
    print("CONFUSION MATRIX :")
    print(best_result['cm'])
    print("FEATURES IMPORTANCE :")
    print(best_result['fi'].sort_values(ascending=False))