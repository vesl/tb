from tbmods.dataset.ichimoku import DatasetIchimoku
from fastapi import APIRouter, HTTPException
from tbmods.dataset.tech import DatasetTech
from tbmods.models.tech import ModelTech
from tbmods.klines import Klines
from tbmods.config import Config
import matplotlib.pyplot as plt
from tbmods.log import Log
from io import BytesIO
import seaborn as sns
import pandas as pd
import base64

router = APIRouter(
    prefix="/dataset",
    tags=["dataset"],
)

config = Config()
log = Log(config['app'])

# Routes
@router.get('/{prefix}/features/map')
async def get_features_map(prefix):
    return config['{}_features'.format(prefix)]
    
@router.get('/{prefix}/features/{symbol}/{period}/{start}/{end}')
async def get_features(prefix,symbol,period,start,end):
    if prefix == 'tech': dataset = DatasetTech(symbol,period,start,end,config['tech_features_selected'].split(','))
    if prefix == 'ichimoku': dataset = DatasetIchimoku(symbol,period,start,end,config['ichimoku_features_selected'].split(','))
    dataset.load_features()
    dataset.features["time"] = dataset.features.index.astype(int)/1000000000 #format data to LC
    return dataset.features.to_json(orient="records")

@router.get('/ohlc/{symbol}/{period}/{start}/{end}')
async def get_ohlc_features(symbol,period,start,end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    klines = Klines(symbol,'historical')
    klines.load_df(start,end)
    klines.df["time"] = klines.df.index.astype(int)/1000000000 #format data to LC
    return klines.df.to_json(orient="records")