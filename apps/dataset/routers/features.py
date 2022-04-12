from fastapi import APIRouter, HTTPException
from tbmods.indicators import Indicators
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log

router = APIRouter(
    prefix="/features",
    tags=["features"],
)

config = Config()
log = Log(config['app'])

@router.get('/{features}/{timescale}/{from_date}/{to_date}')
async def get_features(features,timescale,from_date,to_date):
    """
    Load ohlc from indicators, then add extra features
    """
    # split features
    if features == 'enabled_features': features = config['enabled_features'].split(',')
    else: features = features.split(',')
    # init indicators and load basic features (ohlc+volume)
    indicators = Indicators()
    qdbr = indicators.candles_from_questdb(timescale,from_date,to_date)
    if 'error' in qdbr: return qdbr
    # load extra features
    for feature in features:
        if feature not in indicators.candles.columns:
            if indicators.load_indicator(feature) is False: return {'error':'Unable to load {} feature'.format(feature)}
    return indicators.candles[features].to_json()
