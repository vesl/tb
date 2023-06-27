from trainer.routers.features import get_features_map_by_name
from fastapi import APIRouter, HTTPException
from tbmods.dataset import Dataset
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
def get_dataset_maps():
    mongodb = MongoDB()
    maps = [doc for doc in mongodb.find("TB","datasets_maps")]
    mongodb.close()
    return maps

@router.get('/get/maps/{_type}')
def get_dataset_maps_by_type(_type):
    mongodb = MongoDB()
    maps = [doc for doc in mongodb.find("TB","datasets_maps",{"type":_type})]
    mongodb.close()
    return maps

@router.get('/get/names/{_type}')
def get_dataset_names_by_type(_type):
    mongodb = MongoDB()
    maps = [doc['name'] for doc in mongodb.find("TB","datasets_maps",{"type":_type})]
    mongodb.close()
    return maps

@router.get('/get/types')
def get_dataset_types():
    mongodb = MongoDB()
    types = []
    for doc in mongodb.groupby("TB","datasets_maps","type"):
        types.append(doc["_id"])
    mongodb.close()
    return types
    
@router.get('/get/features_maps/{name}')
def get_dataset_features_maps_by_name(name):
    mongodb = MongoDB()
    features_maps_names = [doc['features_maps'] for doc in mongodb.find("TB","datasets_maps",{"name":name})][0]
    mongodb.close()
    features_maps = []
    for features_map_name in features_maps_names:
        features_maps.append(get_features_map_by_name(features_map_name))
    return features_maps

@router.get('/get/stats/events/{name}/{start}/{end}/{symbol}/{period}')
def get_dataset_labels_stats(name,start,end,symbol,period):
    dataset = Dataset(name,start,end,symbol,period)
    events_count = len(dataset.events)
    events_repartition = dataset.events.ne(0).sum(axis=0)
    return {
        "events_count": events_count,
        "events_repartition": events_repartition.to_json(orient='index'),
        "events_times": list(dataset.events.index.astype(int)/1000000000)
    }