from trainer.routers.datasets import get_dataset_features_maps_by_name
from tbmods.models.random_forest import ModelRandomForest
from fastapi import APIRouter, HTTPException
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.log import Log
import os

router = APIRouter(
    prefix="/models",
    tags=["models"],
)

config = Config()
log = Log(config['app'])

@router.get('/status/{model}')
def get_model_status(model):
    return os.environ["{}_STATUS".format(model.upper())]

@router.get('/get/names/{_type}')
def get_models_names_by_type(_type):
    mongodb = MongoDB()
    maps = [doc['name'] for doc in mongodb.find("TB","models_maps",{"type":_type})]
    mongodb.close()
    return maps

@router.get('/get/types')
def get_models_types():
    mongodb = MongoDB()
    types = []
    for doc in mongodb.groupby("TB","models_maps","type"):
        types.append(doc["_id"])
    mongodb.close()
    return types

@router.get('/train/random_forest/{dataset_name}/{symbol}/{save}')
def train_random_forest(dataset_name,symbol,save):
    """
    Train random_forest model
    save : 0 or 1
    """
    model = ModelRandomForest(dataset_name,symbol)
    model.train()
    if bool(int(save)): model.save()
    os.environ["RANDOM_FOREST_STATUS"] = "available"
    return model.perfs