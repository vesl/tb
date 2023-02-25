from tbmods.market.backtest import MarketBacktest
from sklearn.preprocessing import MinMaxScaler
from tbmods.dataset.tech import DatasetTech
from tbmods.market.paper import MarketPaper
from tbmods.market.live import MarketLive
from datetime import datetime, timedelta
from tbmods.filters import Filters
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

def prepare_data(symbol,period,start,end):
    dataset = DatasetTech(symbol,period,start,end,config['tech_features_selected'].split(','))
    scaler = MinMaxScaler()
    scaler.fit_transform(dataset.features.values)
    price = dataset.klines.df.close
    events = Filters(price).cusum_events(config['cusum_pct_threshold'])
    return dataset,scaler,price,events

@router.get('/backtest/{symbol}/{period}/{start}/{end}')
def get_backtest(symbol,period,start,end):
    # init market
    market_backtest = MarketBacktest("BUSD",1000,"BTC",0)
    market_backtest.update_status(False)
    # prepare time
    current_time = pd.to_datetime(start,utc=True)
    end_time = pd.to_datetime(end,utc=True)
    # prepare data
    market_backtest.update_status({"Prepare data":"{...}"})
    dataset,scaler,price,events = prepare_data(symbol,period,start,end)
    # process
    while current_time <= end_time:
        try:
            market_backtest.set_time(current_time)
            market_backtest.set_price(price.loc[current_time])
            market_backtest.update_status({"Process":str(current_time)})
            if current_time in events.index:
                X = scaler.transform([dataset.features.loc[current_time].values])
                market_backtest.trigger(X)
            else: market_backtest.trigger()
        except KeyError: log.warning("Missing price for : {}".format(current_time))
        market_backtest.save_meta()
        current_time += pd.Timedelta(hours=1)
    market_backtest.exit()
    market_backtest.save_meta()
    market_backtest.update_status(False)
    
@router.get('/{prefix}/check_run')
def market_run(prefix):
    cache = Cache(config['app'])
    return cache.data["{}/status".format(prefix)]