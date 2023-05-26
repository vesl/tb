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

@router.get('/get/maps')
def get_maps():
    mongodb = MongoDB()
    maps = [doc for doc in mongodb.find("TB","features_maps")]
    mongodb.close()
    return maps