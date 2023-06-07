from fastapi import APIRouter, HTTPException
#from tbmods.dataset import Dataset
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.log import Log

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
)

config = Config()
log = Log(config['app'])

@router.get('/get/maps')
def get_maps():
    mongodb = MongoDB()
    maps = [doc for doc in mongodb.find("TB","datasets_maps")]
    mongodb.close()
    return maps

@router.get('/get/maps/{_type}')
def get_maps_by_type(_type):
    mongodb = MongoDB()
    maps = [doc for doc in mongodb.find("TB","datasets_maps",{"type":_type})]
    mongodb.close()
    return maps

@router.get('/get/names/{_type}')
def get_names_by_type(_type):
    mongodb = MongoDB()
    maps = [doc['name'] for doc in mongodb.find("TB","datasets_maps",{"type":_type})]
    mongodb.close()
    return maps

@router.get('/get/types')
def get_types():
    mongodb = MongoDB()
    types = []
    for doc in mongodb.groupby("TB","datasets_maps","type"):
        types.append(doc["_id"])
    return types