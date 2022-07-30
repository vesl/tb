from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from tbmods.triple_barrier import TripleBarrier
from fastapi import APIRouter, HTTPException
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
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

@router.get('/price/{timescale}/{from_date}/{to_date}')
def price_model(timescale,from_date,to_date):
    
    # FEATURES
    
  
    json_features = json.loads(config['features'])
    features = json_features['sources']['qdb'] + json_features['sources']['talib']
    dataset = Dataset(timescale,from_date,to_date,features).load()
    features = dataset.columns # pour les features mergees
    for n in range(1,4):
        for feature in features:
            past_feature = dataset[feature].shift(n)
            dataset['{}-{}'.format(feature,n)] = past_feature.values
    dataset.dropna(inplace=True)
    dataset = dataset.copy() # pour les perfs, il faut join propre
    features = dataset.columns
    cusum = Filters(dataset.close).cusum_events(config['cusum_pct_threshold'])
    """

    features = ['fastk','volume-3','trix-2','minusdi-2','roc-2','roc-1','ppo-3','trix-3','volume-1','roc','fastk-1','bop','willr-1','ppo-2','volume-2','minusdm-1','macdhist-1','fastk-2','cmo','mom','close','plusdi-1','willr','minusdi-3','macdhist-2']
    dataset = Dataset(timescale,from_date,to_date,features).load()
    print(dataset.columns)

    PENSER A BOUCLER SUR LES MOVING AVERAGE

    return 1    
    # RECURSIVE TRAIN
    """
    print('Minus 144')
    close = dataset.close
    remove_close = 0
    while len(features) >= 5:
        if remove_close == 1: features.remove('close')
        dataset = dataset.loc[:,features]
        Y = TripleBarrier(close,cusum).barriers.side
        X = dataset.loc[Y.index]
        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)
        clf = RandomForestClassifier(random_state=42)
        clf.fit(X_train,Y_train)
        Y_pred = clf.predict(X_test)
        f1 = f1_score(Y_test,Y_pred,average=None)
        print('score {}'.format(f1))
        cm = confusion_matrix(Y_test,Y_pred)
        print(cm)
        importances = clf.feature_importances_
        fi = pd.Series(importances, index=features).sort_values(ascending=False)
        print('feature_importance {}'.format(fi['minusdi']))
        features = fi.iloc[:-6].index.tolist()
        if not 'close' in features: 
            remove_close = 1
            features.append('close')