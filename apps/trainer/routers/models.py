from sklearn.ensemble import RandomForestClassifier
from tbmods.models.classifier import Classifier
from tbmods.triple_barrier import TripleBarrier
from fastapi import APIRouter, HTTPException
from tbmods.filters import Filters
from tbmods.dataset import Dataset
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

@router.get('/grid_search/flower/{timescale}/{from_date}/{to_date}')
def grid_search_flower(timescale,from_date,to_date):
    
    # GET ALL FEATURES
    json_features = json.loads(config['features'])
    print(json_features)
    features = json_features['sources']['qdb'] + json_features['sources']['talib']
    dataset = Dataset(timescale,from_date,to_date,features).load()
    features = dataset.columns # pour les features mergees
    for n in [12,24,48,72,96,120,144,168]:
        dataset['ma{}'.format(n)] = dataset.close.rolling(n).mean()
    for n in range(1,4):
        for feature in features:
            past_feature = dataset[feature].shift(n)
            dataset['{}-{}'.format(feature,n)] = past_feature.values
    dataset.dropna(inplace=True)
    dataset = dataset.copy() # pour les perfs, il faut join propre
    print(dataset.iloc[0].to_string())
    
    features = dataset.columns
    cusum = Filters(dataset.close).cusum_events(config['cusum_pct_threshold'])
    
    # GRID SEARCH
    results = []
    while len(features) >= 5:
        result = {}
        dataset = dataset.loc[:,features]
        y = TripleBarrier(dataset.close,cusum).barriers.side
        X = dataset.loc[y.index]
        clf = Classifier(RandomForestClassifier(
            n_estimators=300,
            oob_score=True,
            n_jobs=-1,
            verbose=1,
            class_weight='balanced',
            random_state=42,
        ),X,y,features)
        result['features'] = features
        result['cv_scores'] = clf.cv()
        clf.fit()
        result['f1_score'] = clf.f1_score()
        result['cm'] = clf.confusion_matrix()
        result['fi'] = clf.feature_importances()
        features =  result['fi'].iloc[:-6].index.tolist()
        if not 'close' in features: features.append('close')
        results.append(result)
    
    # GET BEST RESULT
    best_result = {}
    for result in results:
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