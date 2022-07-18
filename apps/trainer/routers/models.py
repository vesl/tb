from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from tbmods.triple_barrier import TripleBarrier
from fastapi import APIRouter, HTTPException
from tbmods.filters import Filters
from tbmods.dataset import Dataset
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
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
    # Get dataset
    json_features = json.loads(config['features'])
    all_features = json_features['sources']['qdb'] + json_features['sources']['talib']
    dataset = Dataset(timescale,from_date,to_date,all_features).load()
    cusum = Filters(dataset.close).cusum_events(config['cusum_pct_threshold'])
    Y = TripleBarrier(dataset.close,cusum).barriers.side
    X = dataset.loc[Y.index]
    clf = RandomForestClassifier(random_state=42)
    scores = cross_val_score(clf, X, Y, cv=5)
    print(scores)
    print(Y.shape)
    return 1