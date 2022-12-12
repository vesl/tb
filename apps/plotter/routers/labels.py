from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from tbmods.dataset.tech import DatasetTech
from tbmods.config import Config
import matplotlib.pyplot as plt
from tbmods.log import Log
import seaborn as sns
from io import BytesIO
import base64
import json

router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)

config = Config()
log = Log(config['app'])

sns.set(rc = {'figure.figsize':(11,4)})

@router.get('/cusum/{period}/{start}/{end}')
def graph_cusum(period,start,end):
    dataset = DatasetTech(period,start,end,['close'])
    close = dataset.features.close
    cusum = dataset.cusum
    image = BytesIO()
    fig, ax = plt.subplots()
    sns.lineplot(x=close.index,y=close.values,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x=cusum.index,y=close.loc[cusum.index],hue='event',data=cusum,ax=ax)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64,"count_cusum":len(cusum)}

@router.get('/tbm/{period}/{start}/{end}')
def graph_tbm(period,start,end):
    dataset = DatasetTech(period,start,end,['close'])
    close = dataset.features.close
    tbm = dataset.tbm
    image = BytesIO()
    fig, ax = plt.subplots()
    sns.lineplot(x=close.index,y=close.values,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x='first_touch',y='close_touch',data=tbm,hue='side',palette=['r','k','g'],ax=ax)
    for i,b in tbm.iterrows():
        mid_price = (b.top+b.bot)/2
        ax.fill([i,b.vertical,b.vertical,i,i],[b.close,b.close,b.top,b.top,b.close],color='green',alpha=0.2)
        ax.fill([i,b.vertical,b.vertical,i,i],[b.bot,b.bot,b.close,b.close,b.bot],color='red',alpha=0.2)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64,"count_tbm":len(tbm)}

@router.get('/balance/{period}/{start}/{end}')
def graph_balance(period,start,end):
    dataset = DatasetTech(period,start,end,['close'])
    close = dataset.features.close
    tbm = dataset.tbm
    image = BytesIO()
    fig, ax = plt.subplots()
    sns.countplot(x='side',data=tbm)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64}