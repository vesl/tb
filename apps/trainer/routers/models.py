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

@router.get('/tech/train/{features}/{period}/{start}/{end}')
def grid_search_tech(period,start,end):
    features_list = config['tech_features_selected'].split(',')
    model = ModelTech(period,start,end,features_list)
    model.clf_init(json.loads(config['tech_clf_config']))
    model.fit()
    model.save_meta()