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

@router.get('/tech/train/{symbol}/{period}/{start}/{end}')
def tech_train(symbol,period,start,end):
    features_list = config['tech_features_selected'].split(',')
    tech_model = ModelTech(symbol,period,start,end,features_list)
    tech_model.update_status(False)
    tech_model.update_status({"Load dataset":"..."})
    tech_model.load_dataset()
    tech_model.update_status({"Load dataset":"OK"})
    tech_model.clf_init(json.loads(config['tech_clf_config']))
    tech_model.update_status({"Fit":"..."})
    tech_model.fit(True)
    tech_model.save_meta()
    tech_model.update_status({"Fit":"OK"})
    tech_model.save_model()
    tech_model.save_scaler()
    tech_model.update_status(False)

@router.get('/tech/check_run')
def tech_run():
    cache = Cache(config['app'])
    return cache.data["models/tech/status"]
    
@router.get('/tech/darwin/{symbol}/{period}/{start}/{end}')
def tech_darwin(symbol,period,start,end):
    tech_darwin = DarwinTech(symbol,period,start,end)
    tech_darwin.evolve()
    
@router.get('/ichimoku/train/{symbol}/{period}/{start}/{end}')
def ichimoku_train(symbol,period,start,end):
    features_list = config['ichimoku_features_selected'].split(',')
    ichimoku_model = ModelIchimoku(symbol,period,start,end,features_list)
    ichimoku_model.update_status(False)
    ichimoku_model.update_status({"Load dataset":"..."})
    ichimoku_model.load_dataset()
    ichimoku_model.update_status({"Load dataset":"OK"})
    ichimoku_model.clf_init(json.loads(config['tech_clf_config']))
    ichimoku_model.update_status({"Fit":"..."})
    ichimoku_model.fit(True)
    ichimoku_model.save_meta()
    ichimoku_model.update_status({"Fit":"OK"})
    ichimoku_model.save_model()
    ichimoku_model.save_scaler()
    ichimoku_model.update_status(False)

@router.get('/ichimoku/check_run')
def ichimoku_run():
    cache = Cache(config['app'])
    return cache.data["models/ichimoku/status"]
    
@router.get('/ichimoku/darwin/{symbol}/{period}/{start}/{end}')
def ichimoku_darwin(symbol,period,start,end):
    ichimoku_darwin = DarwinIchimoku(symbol,period,start,end)
    ichimoku_darwin.evolve()