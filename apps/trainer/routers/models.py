from fastapi import APIRouter, HTTPException
from tbmods.dataset.tech import DatasetTech
from tbmods.models.tech import ModelTech
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import pandas as pd
import numpy as np
import requests
import json

router = APIRouter(
    prefix="/models",
    tags=["models"],
)

config = Config()
log = Log(config['app'])

@router.get('/tech/train/{period}/{start}/{end}')
def tech_train(period,start,end):
    
    cache = Cache(config['app'])
    cache.data['/models/tech'] = {"run":True}
    cache.write()
    
    features_list = config['tech_features_selected'].split(',')
    tech_model = ModelTech(period,start,end,features_list)
    tech_model.clf_init(json.loads(config['tech_clf_config']))
    tech_model.fit()
    tech_model.save_meta()
    
    cache.data['/models/tech'] = {"run":False}
    cache.write()
    
@router.get('/tech/run')
def tech_run():
    cache = Cache(config['app'])
    return cache.data['/models/tech']
