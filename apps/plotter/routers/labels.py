from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from tbmods.dataset.tech import DatasetTech
from tbmods.config import Config
import matplotlib.pyplot as plt
from tbmods.log import Log
from io import BytesIO
import seaborn as sns
import base64

router = APIRouter(
    prefix="/labels",
    tags=["labels"],
)

config = Config()
log = Log(config['app'])

@router.get('/cusum/{symbol}/{period}/{start}/{end}')
def graph_cusum(symbol,period,start,end):
    dataset = DatasetTech(symbol,period,start,end,['close-0'])
    close = dataset.klines.df.close
    cusum = dataset.cusum
    image = BytesIO()
    fig, ax = plt.subplots()
    sns.lineplot(x=close.index,y=close.values,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x=cusum.index,y=close.loc[cusum.index],hue='event',data=cusum,ax=ax)
    fig.set_size_inches(15,6)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64,"count_cusum":len(cusum),"threshold":config['cusum_pct_threshold']}

@router.get('/tbm/{symbol}/{period}/{start}/{end}')
def graph_tbm(symbol,period,start,end):
    dataset = DatasetTech(symbol,period,start,end,['close-0'])
    close = dataset.klines.df.close
    tbm = dataset.tbm
    image = BytesIO()
    fig, ax = plt.subplots()
    sns.lineplot(x=close.index,y=close.values,color='green',label='price',alpha=0.3,ax=ax)
    sns.scatterplot(x='first_touch',y='close_touch',data=tbm,hue='side',palette=['r','k','g'][:len(tbm.side.value_counts())],ax=ax)
    sns.scatterplot(x=tbm.index,y='close',data=tbm,color='grey',marker="_",ax=ax)
    for i,b in tbm.iterrows():
        ax.fill([i,b.vertical,b.vertical,i],[b.bot,b.bot,b.top,b.top],color='grey',alpha=0.2)
        ax.fill([i,b.vertical,b.vertical,i],[b.top,b.top,max(close),max(close)],color='green',alpha=0.2)
        ax.fill([i,b.vertical,b.vertical,i],[b.bot,b.bot,min(close),min(close)],color='red',alpha=0.2)
    fig.set_size_inches(15,6)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64,"count_tbm":len(tbm)}

@router.get('/balance/{symbol}/{period}/{start}/{end}')
def graph_balance(symbol,period,start,end):
    dataset = DatasetTech(symbol,period,start,end,['close-0'])
    tbm = dataset.tbm
    image = BytesIO()
    fig, ax = plt.subplots()
    sns.countplot(x='side',data=tbm)
    fig.set_size_inches(15,6)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64}