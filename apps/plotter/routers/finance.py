from fastapi import APIRouter, HTTPException
from tbmods.dataset import Dataset
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import pandas as pd
import requests
import json

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

config = Config()
log = Log(config['app'])

# Errors handling
def dataset_load_error(msg):
    log.error(msg)
    raise HTTPException(status_code=500,detail=msg)

# Format dataframe to lightwieght chart
def df_to_lc(df):
    df['time'] = df.index.astype(int)/1000000000
    return df.to_json(orient="records")

# Routes
@router.get('/{features}/{timescale}/{from_date}/{to_date}')
async def graph_candles(features,timescale,from_date,to_date):
    """
    Get candles from dataset and return it as json for lightweight-chart
    """
    features = features.split(',')
    data = Dataset(timescale,from_date,to_date,features).load()
    if not isinstance(data,pd.DataFrame): dataset_load_error('Unable to load candles from dataset')
    return df_to_lc(data)