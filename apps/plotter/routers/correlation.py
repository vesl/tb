from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
import seaborn as sns
import pandas as pd
import requests
import json

router = APIRouter(
    prefix="/correlation",
    tags=["correlation"],
)

config = Config()

sns.set(rc = {'figure.figsize':(11,4)})

@router.get('/features/{timescale}/{from_date}/{to_date}/features.png')
def graph_balance(timescale,from_date,to_date):
    # get features
    r = requests.get('http://dataset/features/enabled_features/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail='Unable to get dataset data')
    else: features = json.loads(r.json())
    candles = Candles()
    candles.from_json(features)
    # get labels
    r = requests.get('http://dataset/labels/tbm/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Unable to get dataset data")
    barriers = Candles()
    barriers.from_json(json.loads(r.json()))
    # merge features and labels
    candles.candles = candles.candles.reindex(candles.candles.index.intersection(barriers.candles.index))
    candles.candles['side'] = barriers.candles.side.loc[candles.candles.index]
    # graph
    fig,ax = plt.subplots()
    sns.heatmap(candles.candles.corr(),ax=ax)
    fig.savefig('/tmp/features_corr.png')
    fig.clf()
    return FileResponse('/tmp/features_corr.png',media_type="image/png")