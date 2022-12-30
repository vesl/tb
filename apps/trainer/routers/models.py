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
    features_list = config['tech_features_selected'].split(',')
    tech_model = ModelTech(period,start,end,features_list)
    tech_model.update_status(False)
    tech_model.update_status({"Load dataset":"..."})
    tech_model.load_dataset()
    tech_model.update_status({"Load dataset":"OK"})
    tech_model.clf_init(json.loads(config['tech_clf_config']))
    tech_model.update_status({"Fit":"..."})
    tech_model.fit()
    tech_model.save_meta()
    tech_model.update_status({"Fit":"OK"})
    tech_model.update_status(False)
    
@router.get('/tech/check_run')
def tech_run():
    cache = Cache(config['app'])
    return cache.data["models/tech/status"]
