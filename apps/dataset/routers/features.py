from fastapi import APIRouter, HTTPException
from tbmods.indicators import Indicators
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log

router = APIRouter(
    prefix="/features",
    tags=["features"],
)

config = Config()
log = Log(config['app'])
indicators = Indicators()

@router.get('/{features}/{timescale}/{from_date}/{to_date}')
async def get_features(features,timescale,from_date,to_date):
    features = features.split(',')
    qdbr = indicators.candles_from_questdb(timescale,from_date,to_date)
    if 'error' in qdbr: return qdbr
    return indicators.candles[features]
