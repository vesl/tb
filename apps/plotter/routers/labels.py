from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
import seaborn as sns
import requests
import json

router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)

config = Config()

@router.get('/filters/cusum/{timescale}/{from_date}/{to_date}/cusum.png')
def graph_cusum(timescale,from_date,to_date):
    # get close prices
    r = requests.get('http://dataset/features/close/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Unable to get dataset data")
    close = Candles()
    close.from_json(json.loads(r.json()))
    # get cusum events
    r = requests.get('http://dataset/labels/filters/cusum/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Unable to get dataset data")
    events = Candles()
    events.from_json(json.loads(r.json()))
    # graph
    sns.set(rc = {'figure.figsize':(11,4)})
    sns.lineplot(x=close.candles.index,y='close',data=close.candles,color='green',label='price',alpha=0.3)
    sns.scatterplot(x=events.candles.index,y=close.candles.loc[events.candles.index].close,hue='event',data=events.candles)
    plt.savefig('/tmp/cusum.png')
    plt.close()
    return FileResponse('/tmp/cusum.png',media_type="image/png")

@router.get('/tbm/{timescale}/{from_date}/{to_date}/tbm.png')
def graph_tbm(timescale,from_date,to_date):
    # get close prices
    r = requests.get('http://dataset/features/close/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Unable to get dataset data")
    close = Candles()
    close.from_json(json.loads(r.json()))
    # get tbm
    r = requests.get('http://dataset/labels/tbm/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Unable to get dataset data")
    tbm = Candles()
    tbm.from_json(json.loads(r.json()))