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
    return 1