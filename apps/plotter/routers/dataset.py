from fastapi import APIRouter, HTTPException
from tbmods.dataset.tech import DatasetTech
from tbmods.models.tech import ModelTech
from tbmods.candles import Candles
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
    
@router.get('/tech/features/{period}/{start}/{end}')
async def tech_features(period,start,end):
    dataset = DatasetTech(period,start,end,config['tech_features_selected'].split(','))
    dataset.features["time"] = dataset.features.index.astype(int)/1000000000 #format data to LC
    return dataset.features.to_json(orient="records")

@router.get('/tech/ohlc/{period}/{start}/{end}')
async def ohlc_features(period,start,end):
    start = pd.to_datetime(start)
    candles = Candles()
    candles.from_questdb(period,pd.to_datetime(start),pd.to_datetime(end))
    candles.candles["time"] = candles.candles.index.astype(int)/1000000000 #format data to LC
    return candles.candles.to_json(orient="records")

@router.get('/tech/correlation/{features}/{period}/{start}/{end}')
def graph_correlation(features,period,start,end):
    tech_model = ModelTech(period,start,end,config['tech_features_selected'].split(','))
    tech_model.load_dataset()
    chi2_test = tech_model.chi2_test()
    image = BytesIO()
    fig,ax = plt.subplots()
    fig.set_size_inches(15,10)
    sns.heatmap(chi2_test,ax=ax,annot=True,annot_kws={"fontsize":7},fmt=".0f")
    ax.set_ylabel("Correlation")
    ax.set_xlabel("Features")
    ax.set_xticklabels(tech_model.features_list,fontsize=8)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64}