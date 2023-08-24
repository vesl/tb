from tbmods.pydantic_models import FeaturesMap
from fastapi import APIRouter, HTTPException
from tbmods.features import Features
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.log import Log

router = APIRouter(
    prefix="/features",
    tags=["features"],
)

config = Config()
log = Log(config['app'])

@router.get('/get/maps')
def get_features_maps():
    mongodb = MongoDB()
    maps = [doc for doc in mongodb.find("TB","features_maps")]
    mongodb.close()
    return maps

@router.get('/get/map/{name}')
def get_features_map_by_name(name):
    mongodb = MongoDB()
    features_map = mongodb.find("TB","features_maps",{"name":name})[0]
    mongodb.close()
    return features_map

@router.post('/plot/{start}/{end}/{symbol}/{period}')
def plot_features_maps(features_map: FeaturesMap,start,end,symbol,period):
    features = Features(features_map.dict(),start,end,symbol,period)
    features.df["time"] = features.df.index.astype(int)/1000000000 
    return features.df.to_json(orient='records')