from tbmods.darwin.ichimoku import DarwinIchimoku
from tbmods.models.ichimoku import ModelIchimoku
from fastapi import APIRouter, HTTPException
from tbmods.darwin.tech import DarwinTech
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

@router.get('/{prefix}/train/{symbol}/{period}/{start}/{end}')
def train(prefix,symbol,period,start,end):
    features_list = config['{}_features_selected'.format(prefix)].split(',')
    if prefix == 'tech': model = ModelTech(symbol,period,start,end,features_list)
    if prefix == 'ichimoku': model = ModelIchimoku(symbol,period,start,end,features_list)
    model.update_status(False)
    model.update_status({"Load dataset":"..."})
    model.load_dataset()
    model.update_status({"Load dataset":"OK"})
    model.clf_init(json.loads(config['tech_clf_config']))
    model.update_status({"Fit":"..."})
    model.fit(True)
    model.save_meta()
    model.update_status({"Fit":"OK"})
    model.save_model()
    model.save_scaler()
    model.update_status(False)

@router.get('/{prefix}/check_run')
def check_run(prefix):
    cache = Cache(config['app'])
    return cache.data["models/{}/status".format(prefix)]
    
@router.get('/{prefix}/darwin/{symbol}/{period}/{start}/{end}')
def get_darwin(prefix,symbol,period,start,end):
    if prefix == 'tech': darwin = DarwinTech(symbol,period,start,end)
    if prefix == 'ichimoku': darwin = DarwinIchimoku(symbol,period,start,end)
    darwin.evolve()