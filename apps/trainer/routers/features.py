from fastapi import APIRouter, HTTPException
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.log import Log

router = APIRouter(
    prefix="/features",
    tags=["features"],
)

config = Config()
log = Log(config['app'])

@router.get('/get/features_maps/names')
def get_features_maps_names():
    mongodb = MongoDB()
    features_maps_names = []
    for doc in mongodb.find("TB","features_maps"):
        features_maps_names.append(doc["name"])
    mongodb.close()
    return features_maps_names