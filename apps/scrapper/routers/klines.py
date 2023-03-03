from tbmods.questdb import QuestDB
from tbmods.config import Config
from tbmods.klines import Klines
from binance.spot import Spot
from fastapi import APIRouter
from datetime import datetime
from tbmods.log import Log
import pandas as pd
import time

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
    # compute previous kline time and next kline time
    klines = Klines(symbol,'live')
    klines.get_last_stored()
    current_hour = pd.Timestamp.utcnow().replace(minute=0, second=0)
    if len(klines.last_stored) == 1: previous_kline = klines.last_stored.index[0]
    else: previous_kline = current_hour-pd.Timedelta(hours=2)
    if (current_hour-previous_kline) < pd.Timedelta(hours=2): return 0
    # pull new kline from binance
    bc = Spot()
    new_kline = bc.klines(symbol=symbol,interval='1h',limit=2)[0]
    # check if binance is ready
    if pd.Timestamp(new_kline[0],unit='ms',tz='utc') - previous_kline < pd.Timedelta(minutes=59): return 1
    # store new kline
    klines.ingest(new_kline)
    # sleep waiting for storage
    klines.get_last_stored()
    log.info("{} Ingested kline {}".format(pd.Timestamp.utcnow(),klines.last_stored.index[0]))