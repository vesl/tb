from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from tbmods.triple_barrier import TripleBarrier
from tbmods.dataset import Dataset
from tbmods.filters import Filters
from tbmods.config import Config
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
    close = Dataset(timescale,from_date,to_date,'close').load()['close']
    cusum = Filters(close).cusum_events(config['cusum_pct_threshold'])
    # graph
    fig, ax = plt.subplots()
    sns.lineplot(x=close.index,y=close.values,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x=cusum.index,y=close.loc[cusum.index],hue='event',data=cusum,ax=ax)
    fig.savefig('/tmp/cusum.png')
    fig.clf()
    return FileResponse('/tmp/cusum.png',media_type="image/png")

@router.get('/tbm/{timescale}/{from_date}/{to_date}/tbm.png')
def graph_tbm(timescale,from_date,to_date):
    close = Dataset(timescale,from_date,to_date,'close').load()['close']
    cusum = Filters(close).cusum_events(config['cusum_pct_threshold'])
    barriers = TripleBarrier(close,cusum).barriers
    # graph
    fig, ax = plt.subplots()
    sns.lineplot(x=close.index,y=close.values,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x='first_touch',y='close_touch',data=barriers,hue='side',palette=['r','k','g'],ax=ax)
    for i,b in barriers.iterrows():
        mid_price = (b.top+b.bot)/2
        ax.fill([i,b.vertical,b.vertical,i,i],[b.close,b.close,b.top,b.top,b.close],color='green',alpha=0.2)
        ax.fill([i,b.vertical,b.vertical,i,i],[b.bot,b.bot,b.close,b.close,b.bot],color='red',alpha=0.2)
    fig.savefig('/tmp/tbm.png')
    fig.clf()
    return FileResponse('/tmp/tbm.png',media_type="image/png")

@router.get('/balance/{timescale}/{from_date}/{to_date}/balance.png')
def graph_balance(timescale,from_date,to_date):
    close = Dataset(timescale,from_date,to_date,'close').load()['close']
    cusum = Filters(close).cusum_events(config['cusum_pct_threshold'])
    barriers = TripleBarrier(close,cusum).barriers
    # graph
    fig, ax = plt.subplots()
    sns.countplot(x='side',data=barriers)
    fig.savefig('/tmp/balance.png')
    fig.clf()
    return FileResponse('/tmp/balance.png',media_type="image/png")