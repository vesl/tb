from fastapi import APIRouter
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache

router = APIRouter(
    prefix="/status",
    tags=["status"],
)

config = Config()
candles = Candles()

@router.get('/')
def get_status():
    
    status = {}
    # config
    status['config'] = {
        'symbol':config['symbol'],
        'binance_hist_limit':config['binance_hist_limit'],
        'binance_trades_pack_size':config['binance_trades_pack_size'],
    }
    # last id
    cache = Cache(config['app'])
    status['last_id'] = cache.data['trades/binance/last_id']
    # last candle
    last_candle = candles.get_last()
    status['last_candle'] = last_candle['error'] if 'error' in last_candle else last_candle['result'][0]
    
    return status
    