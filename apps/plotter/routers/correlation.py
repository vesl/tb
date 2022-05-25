from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from tbmods.triple_barrier import TripleBarrier
from tbmods.dataset import Dataset
from tbmods.filters import Filters
from tbmods.config import Config
import seaborn as sns
import pandas as pd
import json

router = APIRouter(
    prefix="/correlation",
    tags=["correlation"],
)

config = Config()

sns.set(font_scale=0.5,rc = {'figure.figsize':(11,5)})

@router.get('/features/{timescale}/{from_date}/{to_date}/features.png')
def graph_balance(timescale,from_date,to_date):
    config['features'] = json.loads(config['features'])
    features_avail = ",".join(config['features']['sources']['qdb']+config['features']['sources']['talib'])
    features = Dataset(timescale,from_date,to_date,features_avail).load()
    cusum = Filters(features['close']).cusum_events(config['cusum_pct_threshold'])
    labels = TripleBarrier(features['close'],cusum).barriers['side']
    # merge features and labels
    features = features.join(labels,how='inner')
    # graph
    fig,ax = plt.subplots()
    sns.heatmap(features.corr(),ax=ax)
    fig.savefig('/tmp/features_corr.png')
    fig.clf()
    return FileResponse('/tmp/features_corr.png',media_type="image/png")