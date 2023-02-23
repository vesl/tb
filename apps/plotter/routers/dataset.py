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
@router.get('/tech/features/map')
async def tech_features_map():
    return config['tech_features']
    
@router.get('/tech/features/{symbol}/{period}/{start}/{end}')
async def tech_features(symbol,period,start,end):
    dataset = DatasetTech(symbol,period,start,end,config['tech_features_selected'].split(','))
    dataset.features["time"] = dataset.features.index.astype(int)/1000000000 #format data to LC
    return dataset.features.to_json(orient="records")

@router.get('/tech/ohlc/{symbol}/{period}/{start}/{end}')
async def ohlc_features(symbol,period,start,end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    klines = Klines(symbol)
    klines.load_df(period,start,end)
    klines.df['time'] = klines.df.index.astype(int)/1000000000 #format data to LC
    return klines.df.to_json(orient="records")

@router.get('/tech/correlation/{features}/{symbol}/{period}/{start}/{end}')
def graph_correlation(features,symbol,period,start,end):
    tech_model = ModelTech(symbol,period,start,end,config['tech_features_selected'].split(','))
    tech_model.load_dataset()
    chi2_test = tech_model.chi2_test()
    image = BytesIO()
    fig,ax = plt.subplots()
    fig.set_size_inches(15,10)
    sns.heatmap(chi2_test,ax=ax,annot=True,annot_kws={"fontsize":7},fmt=".0f")
    ax.set_ylabel("Correlation")
    ax.set_xlabel("Features")
    ax.set_xticks(list(range(len(tech_model.features_list))),labels=tech_model.features_list,fontsize=3)
    #ax.set_xticklabels()
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64}