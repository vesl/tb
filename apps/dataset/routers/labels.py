from fastapi import APIRouter, HTTPException
from dataset.routers.features import get_features
from tbmods.triple_barrier import TripleBarrier
from tbmods.filters import Filters
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
    close = await get_features('close',timescale,from_date,to_date)
    filters = Filters(close)
    events = filters.cusum_events(config['cusum_pct_threshold'])
    return events.to_json()
    
@router.get('/tbm/{timescale}/{from_date}/{to_date}')
async def get_tbm(timescale,from_date,to_date):
    close = await get_features('close',timescale,from_date,to_date)
    filters = Filters(close)
    events = filters.cusum_events(config['cusum_pct_threshold'])
    candles = Candles()
    candles.from_json(json.loads(close))
    tbm = TripleBarrier(candles.candles,events)
    tbm.apply_horizontal_barriers(config['tbm_up_thresh'],config['tbm_down_thresh'])
    tbm.apply_vertical_barrier()
    return tbm.to_json()