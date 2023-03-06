from tbmods.market.backtest import MarketBacktest
from sklearn.preprocessing import RobustScaler
from tbmods.dataset.tech import DatasetTech
from tbmods.market.paper import MarketPaper
from tbmods.market.live import MarketLive
from datetime import datetime, timedelta
from tbmods.config import Config
from tbmods.cache import Cache
from fastapi import APIRouter
from tbmods.log import Log
import pandas as pd

router = APIRouter(
    prefix="/market",
    tags=["markett"],
)

config = Config()
log = Log(config['app'])

@router.get('/backtest/{symbol}/{period}/{start}/{end}')
def get_backtest(symbol,period,start,end):

    # init
    current_time = pd.to_datetime(start,utc=True)
    end_time = pd.to_datetime(end,utc=True)
    market_backtest = MarketBacktest(symbol,period,"USDT",1000,"BTC",0)
    
    dataset = DatasetTech(symbol,period,start,end,config['tech_features_selected'].split(','))
    dataset.load_features()
    price = dataset.klines.df.close
    events = dataset.cusum

    while current_time <= end_time:

        market_backtest.set_time(current_time)

        if not market_backtest.get_klines():
            current_time += pd.Timedelta(hours=1)
            continue

        if not market_backtest.get_price():
            current_time += pd.Timedelta(hours=1)
            continue


        market_backtest.check_event()
        market_backtest.trigger()

        current_time += pd.Timedelta(hours=1)
    market_backtest.exit()

@router.get('/paper')
def get_paper():
    pass

@router.get('/live')
def get_live():
    market_live = MarketLive('USDT','BTC')
    print(market_live.wallet)
    
@router.get('/{prefix}/check_run')
def market_run(prefix):
    cache = Cache(config['app'])
    return cache.data["{}/status".format(prefix)]