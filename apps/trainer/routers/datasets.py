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