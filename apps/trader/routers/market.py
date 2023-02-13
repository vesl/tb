from tbmods.market.backtest import MarketBacktest
from sklearn.preprocessing import MinMaxScaler
from tbmods.dataset.tech import DatasetTech
from tbmods.market.paper import MarketPaper
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

def prepare_data(period,start,end):
    dataset = DatasetTech(period,start,end,config['tech_features_selected'].split(','))
    scaler = MinMaxScaler()
    scaler.fit_transform(dataset.features)
    price = dataset.candles.candles.close
    events = Filters(price).cusum_events(config['cusum_pct_threshold'])
    return dataset,scaler,price,events

@router.get('/backtest/{period}/{start}/{end}')
def get_backtest(period,start,end):
    # init market
    market_backtest = MarketBacktest("USDC",1000,"BTC",0)
    market_backtest.update_status(False)
    # prepare time
    current_time = pd.to_datetime(start,utc=True)
    end_time = pd.to_datetime(end,utc=True)
    # prepare data
    market_backtest.update_status({"Prepare data":"{...}"})
    dataset,scaler,price,events = prepare_data(period,start,end)
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

@router.get('/paper')
def get_paper():
    timer = datetime.now()
    # init market
    market_paper = MarketPaper("USDC",1000,"BTC",0)
    market_paper.name = 'paper'
    market_paper.load_meta()
    # prepare time
    start = config['tech_data_start']
    period = config['tech_data_period']
    end = pd.to_datetime('today')+pd.Timedelta(days=1)
    current_time = pd.to_datetime(start,utc=True)
    end_time = pd.to_datetime(end,utc=True)
    # get last_time and next_time
    cache = Cache(config['app'])
    if len(cache.data['paper/status']) > 0 : last_time = pd.to_datetime(cache.data['paper/status']["last_time"])
    else:
        log.info("Empty cache init last_time")
        last_time = pd.to_datetime('now',utc=True).floor('H')
        market_paper.update_status({"last_time":str(last_time)})
    next_time = last_time + pd.Timedelta(hours=1)
    # prepare data
    dataset,scaler,price,events = prepare_data(period,start,end)
    if next_time in dataset.full_features.index:
        log.info("Last time {}".format(last_time))
        log.info("Next time {}".format(next_time))
        if next_time in events.index:
            log.info("Event detected !")
            X = scaler.transform([dataset.full_features.loc[next_time]])
            market_paper.trigger(X)
        else:
            log.info("No event detected last one {}".format(events.index[-1]))
            market_paper.trigger()
        market_paper.update_status({"last_time":str(next_time)})
        market_paper.save_meta()
    log.info("Duration : {}".format(datetime.now()-timer))

@router.get('/{prefix}/check_run')
def market_run(prefix):
    cache = Cache(config['app'])
    return cache.data["{}/status".format(prefix)]