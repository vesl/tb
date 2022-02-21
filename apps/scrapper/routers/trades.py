from fastapi import APIRouter, HTTPException
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
from binance.spot import Spot
from datetime import datetime,timedelta
import requests

router = APIRouter(
    prefix="/trades",
    tags=["trades"],
)

config = Config()
log = Log(config['app'])
cache = Cache(config['app'])

@router.get('/binance')
def get_binance_trades():
    """
    Purpose: collect 1 minute of trades from binance and send it to candles
    Steps:
    * get last_id from cache
    * get 1 trade from binance and compute current minute, then the next minute
    * get trades from binance while they are before the next minute
    * filter trades after the next minute (pull packs of binance_hist_limit from binance)
    * send it to candles
    *** This is not async to avoid race condition on cache
    """
    last_id = cache.data['trades/binance/last_id'] if 'trades/binance/last_id' in cache.data else -1
    log.info('Last id is {}'.format(last_id))
    
    binance_client = Spot(key=config['binance_api_key'], secret=config['binance_api_secret'])
    trades = binance_client.historical_trades(config['symbol'],limit=1,fromId=last_id+1)
    if len(trades) == 0: raise HTTPException(status_code=425,detail="Too early for first trade")
    
    # trick , because datetime cant handle millisecond timestamps
    dt = datetime(1970, 1, 1) + timedelta(milliseconds=trades[0]['time'])
    log.info('First trade is at {}'.format(dt))
    ts_end = int(datetime.timestamp(dt + (datetime.min - dt) % timedelta(minutes=1))*1000)
    ts = int(datetime.timestamp(dt)*1000)
    
    while(ts <= ts_end):
        pack=binance_client.historical_trades(config['symbol'],limit=config['binance_hist_limit'],fromId=trades[-1]['id']+1)
        if len(pack) == 0: raise HTTPException(status_code=425,detail="Too early for last trade")
        trades.extend(pack)
        ts=trades[-1]['time']
    
    trades = list(filter(lambda trade: trade['time'] <= ts_end, trades))
    log.info('Got {} trades'.format(len(trades)))
    dt_end = datetime(1970, 1, 1) + timedelta(milliseconds=trades[-1]['time'])
    log.info('Last trade is at {}'.format(dt_end))
    
    try:
        r = requests.put(config['candles_trades_store_url'],json={"trades":trades})
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=500,detail="Sent to candles failed. {}".format(e))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Sent to candles failed")
    cache.data['trades/binance/last_id'] = trades[-1]['id']
    cache.write()
    return {"Scrapped": "from {} to {}".format(dt,dt_end)}
    
    