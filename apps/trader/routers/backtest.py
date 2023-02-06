from tbmods.market.backtest import MarketBacktest
from sklearn.preprocessing import MinMaxScaler
from tbmods.dataset.tech import DatasetTech
from tbmods.filters import Filters
from tbmods.config import Config
from tbmods.cache import Cache
from fastapi import APIRouter
from tbmods.log import Log
import pandas as pd

router = APIRouter(
    prefix="/backtest",
    tags=["backtest"],
)

config = Config()
log = Log(config['app'])

@router.get('/{period}/{start}/{end}')
def get_backtest(period,start,end):
    # init market
    market_backtest = MarketBacktest("USDC",1000,"BTC",0,period,start,end)
    market_backtest.update_status(False)
    # prepare time
    current_time = pd.to_datetime(start,utc=True)
    end_time = pd.to_datetime(end,utc=True)
    # prepare data
    market_backtest.update_status({"Prepare data":"..."})
    dataset = DatasetTech(period,start,end,config['tech_features_selected'].split(','))
    scaler = MinMaxScaler()
    scaler.fit_transform(dataset.features)
    price = dataset.candles.candles.close
    events = Filters(price).cusum_events(config['cusum_pct_threshold'])
    # process
    while current_time <= end_time:
        try:
            market_backtest.set_time(current_time)
            market_backtest.set_price(price.loc[current_time])
            market_backtest.update_status({"Process":str(current_time)})
            if current_time in events.index:
                X = scaler.transform([dataset.features.loc[current_time]])
                market_backtest.trigger(X)
            else: market_backtest.trigger()
        except KeyError: log.warning("Missing price for : {}".format(current_time))
        market_backtest.save_meta()
        current_time += pd.Timedelta(hours=1)
    market_backtest.exit()
    market_backtest.save_meta()
    market_backtest.update_status(False)

@router.get('/check_run')
def tech_run():
    cache = Cache(config['app'])
    return cache.data["backtest/status"]