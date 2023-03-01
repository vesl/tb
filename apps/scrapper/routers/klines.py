from tbmods.questdb import QuestDB
from tbmods.config import Config
from tbmods.klines import Klines
from binance.spot import Spot
from fastapi import APIRouter
from datetime import datetime
from tbmods.log import Log
import pandas as pd

router = APIRouter(
    prefix="/klines",
    tags=["klines"],
)

questdb = QuestDB
config = Config()
log = Log(config['app'])

"""
CREATE TABLE live_BTCUSDT(
  open_time TIMESTAMP, 
  open DOUBLE,
  high DOUBLE,
  low DOUBLE,
  close DOUBLE,
  volume DOUBLE,
  close_time TIMESTAMP,
  quote_asset_volume DOUBLE,
  number_of_trades INT,
  taker_buy_base_asset_volume DOUBLE,
  taker_buy_quote_asset_volume DOUBLE,
  ignore DOUBLE
) timestamp(open_time);
"""

@router.get('/update/{symbol}')
def klines(symbol):
    # get last kline
    klines = Klines(symbol,'live')
    klines.get_last_stored()
    # compute last time, set it to prev 2 hours if table is empty
    if len(klines.last_stored) == 1: last_time = klines.last_stored.index[0]
    else: last_time = pd.Timestamp.utcnow().round('H')-pd.Timedelta(hours=2)
    # if last kline younger than 1h we are up to date
    now = pd.Timestamp.utcnow()
    if (now - klines.last_stored.index) < pd.Timedelta(hours=1): return 0
    # get next klines
    bc = Spot()
    next_time = int((last_time + pd.Timedelta(hours=1)).timestamp()*1000)
    last_klines = bc.klines(symbol=symbol,interval='1h',startTime=next_time)
    klines.ingest(last_klines[0])
    klines.get_last_stored()
    log.info("{} Ingested kline {}".format(pd.Timestamp.utcnow(),klines.last_stored.index[0]))