from fastapi import APIRouter, HTTPException
from binance.spot import Spot
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log

router = APIRouter(
    prefix="/trades",
    tags=["trades"],
)

config = Config()
log = Log(config['app'])

@router.get('/')
def scrap_trades():
    """
    Purpose: get binance trades and ingest it in questdb
    * Decrease config['binance_trades_pack_size'] to pull new trades faster, or Increase to pull history faster
    """

    # init cache and get last id
    cache = Cache(config['app'])
    last_id = cache.data['trades/binance/last_id'] if 'trades/binance/last_id' in cache.data else -1
    log.info('Last id is {}'.format(last_id))
    
    # init binance client and get 10 packs of 1000 trades to be sure to get at least 2 candles (we drop last one)
    binance_client = Spot(key=config['binance_api_key'], secret=config['binance_api_secret'])
    trades = []
    prev_nb_trades = -1
    while (len(trades) < config['binance_trades_pack_size']) and (len(trades) > prev_nb_trades):
        prev_nb_trades = len(trades)
        trades.extend(binance_client.historical_trades(config['symbol'],limit=config['binance_hist_limit'],fromId=last_id+1))
        last_id = trades[-1]['id']
    log.info("Got {} trades".format(len(trades)))
    
    # init candles class 
    candles = Candles()
    last_id = candles.from_trades(trades)
    if not last_id:
        log.error("Maybe minute is not finished, try again later")
        raise HTTPException(status_code=425,detail="Maybe minute is not finished, try again later")
    ingest = candles.ingest()
    if 'error' in ingest:
        log.error("Trades not ingested {}".format(ingest['error']))
        raise HTTPException(status_code=500,detail="Trades not ingested {}".format(ingest['error']))
    
    # update cache and write
    cache.data['trades/binance/last_id'] = last_id
    cache.write()
    
    return {"ingested":"{} candles".format(len(candles.candles))}