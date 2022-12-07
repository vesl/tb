from fastapi import APIRouter, HTTPException
from tbmods.dataset.tech import DatasetTech
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import json

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
    
@router.get('/tech/feature/{features}/{period}/{start}/{end}')
async def tech_features(features,period,start,end):
    dataset = DatasetTech(period,start,end,features.split(','))
    dataset.features["time"] = dataset.features.index.astype(int)/1000000000 #format data to LC
    return dataset.features.to_json(orient="records")
    