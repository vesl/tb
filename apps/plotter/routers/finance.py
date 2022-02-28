from fastapi import APIRouter, HTTPException
from tbmods.indicators import Indicators
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import requests

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

config = Config()
log = Log(config['app'])

@router.get('/ohlc/{timescale}/{from_date}/{to_date}')
async def graph_price(timescale,from_date,to_date):
    """
    Purpose: get candles olhc from dataset and return it as json for lightweight-chart
    """
    r = requests.get('http://dataset/features/ohlc/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Unable to get dataset data")
    ohlc = r.json()
    if 'error' in ohlc: raise HTTPException(status_code=500,detail=ohlc['error'])
    candles = Candles()
    candles.from_json(ohlc)
    candles.candles['time'] = candles.candles.index.astype(int)/1000000000
    return candles.candles.to_json(orient="records")