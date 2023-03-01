from fastapi import APIRouter, HTTPException
from tbmods.dataset.tech import DatasetTech
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
    tech_model.update_status(False)
    
@router.get('/tech/check_run')
def tech_run():
    cache = Cache(config['app'])
    return cache.data["models/tech/status"]
    
@router.get('/tech/darwin/{period}/{start}/{end}')
def tech_darwin(period,start,end):
    tech_darwin = DarwinTech(period,start,end)
    tech_darwin.evolve()
    return "ok"