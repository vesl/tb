from tbmods.market.backtest import MarketBacktest
from sklearn.preprocessing import MinMaxScaler
from tbmods.dataset.tech import DatasetTech
from tbmods.filters import Filters
from tbmods.config import Config
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
    # prepare time
    current_time = pd.to_datetime(start,utc=True)
    end_time = pd.to_datetime(end,utc=True)
    # prepare data
    dataset = DatasetTech(period,start,end,config['tech_features_selected'].split(','))
    scaler = MinMaxScaler()
    scaler.fit_transform(dataset.features)
    price = dataset.candles.candles.close
    events = Filters(price).cusum_events(config['cusum_pct_threshold'])
    # init market
    market = MarketBacktest("USDC",1000,"BTC",0)
    # process
    while current_time <= end_time:
        try:
            market.set_time(current_time)
            market.set_price(price.loc[current_time])
            if current_time in events.index:
                X = scaler.transform([dataset.features.loc[current_time]])
                market.trigger(X)
            else: market.trigger()
        except KeyError: log.warning("Missing price for : {}".format(current_time))
        current_time += pd.Timedelta(hours=1)