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
    all_features = json_features['sources']['qdb'] + json_features['sources']['talib']
    dataset = Dataset(timescale,from_date,to_date,all_features).load()
    for n in range(1,4):
        for feature in dataset.columns:
            n_feature = pd.DataFrame(dataset[feature].shift(n),columns=['{}-{}'.format(feature,n)])
            dataset = pd.concat([dataset,],axis=1,join='inner')
    dataset.dropna(inplace=True)
    all_features = dataset.columns
    cusum = Filters(dataset.close).cusum_events(config['cusum_pct_threshold'])
    
    # RECURSIVE TRAIN
    while len(all_features) >= 5:
        print("===> TRAIN")
        print(all_features)
        dataset = dataset.loc[:,all_features]
        print(dataset.head())
        Y = TripleBarrier(dataset.close,cusum).barriers.side
        X = dataset.loc[Y.index]
        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)
        clf = RandomForestClassifier(random_state=42)
        clf.fit(X_train,Y_train)
        Y_pred = clf.predict(X_test)
        f1 = f1_score(Y_test,Y_pred,average=None)
        print(f1)
        cm = confusion_matrix(Y_test,Y_pred)
        print(cm)
        importances = clf.feature_importances_
        fi = pd.Series(importances, index=dataset.columns).sort_values(ascending=False)
        print(fi)
        all_features = fi.iloc[:-6].index.tolist()
        if not 'close' in all_features: all_features.append('close')
    return 1