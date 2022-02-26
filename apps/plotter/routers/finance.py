from fastapi import APIRouter, HTTPException
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

config = Config()
log = Log(config['app'])

@router.get('/price/{timescale}/{from_date}/{to_date}')
async def graph_price(timescale,from_date,to_date):
    """
    Purpose: get candles and return it as json for lightweight-chart
    """
    candles = Candles()
    candles.from_questdb(timescale,from_date,to_date)
    if type(candles.candles) == type(None): raise HTTPException(status_code=425)
    candles.candles['time'] = candles.candles.index.astype(int)/1000000000
    return candles.candles.to_json(orient="records")