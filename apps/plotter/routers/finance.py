from fastapi import APIRouter, HTTPException
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import requests
import json

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

config = Config()
log = Log(config['app'])

def lightweight_chart(candles):
    """
    Format candles for lightweight chart
    """
    candles.candles['time'] = candles.candles.index.astype(int)/1000000000
    return candles.candles.to_json(orient="records")

def get_features(features,timescale,from_date,to_date):
    """
    Pull features json data from dataset
    """
    r = requests.get('http://dataset/features/{}/{}/{}/{}'.format(features,timescale,from_date,to_date))
    if r.status_code != 200: features = {'error':'Unable to get dataset data'}
    else: features = json.loads(r.json())
    return features

@router.get('/candles/{timescale}/{from_date}/{to_date}')
async def graph_candles(timescale,from_date,to_date):
    """
    Get candles olhc from dataset and return it as json for lightweight-chart
    """
    features = get_features('open,high,low,close',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/volume/{timescale}/{from_date}/{to_date}')
async def graph_volume(timescale,from_date,to_date):
    """
    Get volume from dataset and return it as json for lightweight-chart
    """
    features = get_features('volume',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/rsi/{timescale}/{from_date}/{to_date}')
async def graph_rsi(timescale,from_date,to_date):
    """
    Get rsi from dataset and return it as json
    """
    features = get_features('rsi',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/adx/{timescale}/{from_date}/{to_date}')
async def graph_adx(timescale,from_date,to_date):
    """
    Get adx from dataset and return it as json
    """
    features = get_features('adx',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)