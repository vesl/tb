from fastapi import APIRouter, HTTPException
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import requests
import json

router = APIRouter(
    prefix="/models",
    tags=["models"],
)

config = Config()
log = Log(config['app'])

@router.get('/price/{timescale}/{from_date}/{to_date}')
def price_model(timescale,from_date,to_date):
    # Get dataset
    r = requests.get('http://dataset/features/enabled_features/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: features = {'error':'Unable to get dataset data'}
    else: features = json.loads(r.json())
    print(features)
    return 1