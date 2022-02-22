from candles.classes.body_requests import Trades
from candles.classes.candles import Candles
from fastapi import APIRouter, HTTPException
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd

router = APIRouter(
    prefix="/minutes",
    tags=["minutes"],
)

config = Config()
log = Log(config['app'])


@router.put('/ingest')
async def ingest_trades(trades: Trades):
    """
    Purpose : get 1 min json trades , create a candle, and store it into questdb
    Steps : 
    * Create df from json , keep only : price,qty,time columns
    * Create candle
    * Instanciate candle class and store candle
    """

    df = pd.DataFrame(trades.dict()['trades']).loc[:,['price','qty','time']].set_index('time').sort_index()
    df.index = pd.to_datetime(df.index,unit='ms')
    
    candle = {}
    candle['open'] = df.iloc[0].price
    candle['high'] = df.price.max()
    candle['low'] = df.price.min()
    candle['close'] = df.iloc[-1].price
    candle['volume'] = df.qty.sum()
    candle['candle_time'] = pd.Timestamp(df.index[0]).floor(freq='T').timestamp()
    log.info("Ingesting candle {}".format(candle))
    
    candles = Candles(pd.DataFrame([candle]),timescale='minute')
    if not candles.ingest(): raise HTTPException(status_code=500,detail="Failed to insert candle(s) into questdb")
    
    return {"ingested":"Done"}
    