from fastapi import APIRouter, HTTPException
from dataset.routers.features import get_features
from tbmods.triple_barrier import TripleBarrier
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
import pandas as pd
import json

router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)

config = Config()

@router.get('/')
async def get_labels():
    return ""
    
@router.get('/filters/cusum/{timescale}/{from_date}/{to_date}')
async def get_cusum(timescale,from_date,to_date):
    cusum_events = pd.DataFrame(columns=['event'])
    close = await get_features('close',timescale,from_date,to_date)
    candles = Candles()
    candles.from_json(json.loads(close))
    close_diff = candles.candles['close'].pct_change().dropna()
    spos,sneg = 0,0
    for date in close_diff.index:
        threshold = config['cusum_pct_threshold']/100
        spos,sneg = max(0,spos+close_diff.loc[date]),min(0,sneg+close_diff.loc[date])
        if sneg < -threshold: cusum_events = pd.concat([cusum_events,pd.DataFrame({'event':sneg},index=[date])])
        elif spos > threshold: cusum_events = pd.concat([cusum_events,pd.DataFrame({'event':spos},index=[date])])
    return cusum_events.to_json()
    
@router.get('/tbm/{timescale}/{from_date}/{to_date}')
async def get_tbm(timescale,from_date,to_date):
    close = await get_features('close',timescale,from_date,to_date)
    candles = Candles()
    candles.from_json(json.loads(close))
    tbm = TripleBarrier(candles.candles)
    