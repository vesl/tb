from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
import seaborn as sns
import pandas as pd
import requests
import json

router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)

config = Config()

sns.set(rc = {'figure.figsize':(11,4)})

@router.get('/cusum/{timescale}/{from_date}/{to_date}/cusum.png')
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
    fig, ax = plt.subplots()
    sns.lineplot(x=close.candles.index,y='close',data=close.candles,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x=events.candles.index,y=close.candles.loc[events.candles.index].close,hue='event',data=events.candles,ax=ax)
    fig.savefig('/tmp/cusum.png')
    fig.clf()
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
    barriers = Candles()
    barriers.from_json(json.loads(r.json()))
    barriers.candles.vertical = pd.to_datetime(barriers.candles.vertical,unit='ms')
    barriers.candles.first_touch = pd.to_datetime(barriers.candles.first_touch,unit='ms')
    # graph
    fig, ax = plt.subplots()
    sns.lineplot(x=close.candles.index,y='close',data=close.candles,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x='first_touch',y='close_touch',data=barriers.candles,hue='side',palette=['r','k','g'],ax=ax)
    for i,b in barriers.candles.iterrows():
        mid_price = (b.top+b.bot)/2
        ax.fill([i,b.vertical,b.vertical,i,i],[b.close,b.close,b.top,b.top,b.close],color='green',alpha=0.2)
        ax.fill([i,b.vertical,b.vertical,i,i],[b.bot,b.bot,b.close,b.close,b.bot],color='red',alpha=0.2)
    fig.savefig('/tmp/tbm.png')
    fig.clf()
    return FileResponse('/tmp/tbm.png',media_type="image/png")

@router.get('/balance/{timescale}/{from_date}/{to_date}/balance.png')
def graph_balance(timescale,from_date,to_date):
    # get tbm
    r = requests.get('http://dataset/labels/tbm/{}/{}/{}'.format(timescale,from_date,to_date))
    if r.status_code != 200: raise HTTPException(status_code=500,detail="Unable to get dataset data")
    barriers = Candles()
    barriers.from_json(json.loads(r.json()))
    # graph
    fig, ax = plt.subplots()
    sns.countplot(x='side',data=barriers.candles)
    fig.savefig('/tmp/balance.png')
    fig.clf()
    return FileResponse('/tmp/balance.png',media_type="image/png")