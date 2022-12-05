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
@router.get('/tech/features/list')
async def tech_features_list():
    return config['tech_features']
    
@router.get('/tech/feature/{feature}/{period}/{start}/{end}')
async def tech_features(feature,period,start,end):
    dataset = DatasetTech(period,start,end,[feature])
    return dataset.features.to_json(orient="records")
    