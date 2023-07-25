from trainer.routers.datasets import get_dataset_features_maps_by_name
from tbmods.models.random_forest import ModelRandomForest
from tbmods.pydantic_models import ModelMap
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

@router.get('/get/names/{_type}')
def get_models_names_by_type(_type):
    mongodb = MongoDB()
    maps = [doc['name'] for doc in mongodb.find("TB","models_maps",{"type":_type})]
    mongodb.close()
    return maps

@router.get('/get/parameters_map/{_type}')
def get_models_parameters_map_by_type(_type):
    mongodb = MongoDB()
    parameters_map = [doc['parameters'] for doc in mongodb.find("TB","models_maps",{"name":_type})][0]
    mongodb.close()
    return parameters_map

@router.get('/get/types')
def get_models_types():
    mongodb = MongoDB()
    types = []
    for doc in mongodb.groupby("TB","models_maps","type"):
        types.append(doc["_id"])
    mongodb.close()
    return types

@router.get('/train/status')
def get_model_status():
    return int(os.environ["STATUS"])

@router.post('/train/random_forest/{symbol}')
def train_random_forest(model_map: ModelMap, symbol):
    os.environ["STATUS"] = "1"
    try:
        model = ModelRandomForest(model_map.dataset_name,symbol,model_map.parameters_map)
        model.train()
        if model_map.save: model.save()
        os.environ["STATUS"] = "0"
        return { "perfs": model.perfs, "name": model.name }
    except Exception as e:
        os.environ["STATUS"] = "0"
        log.warning(e)
        raise HTTPException(status_code=500, detail="Training failed")