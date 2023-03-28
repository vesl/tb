from fastapi import APIRouter, HTTPException
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.log import Log
import json

router = APIRouter(
    prefix="/models",
    tags=["models"],
)

config = Config()
log = Log(config['app'])
    
@router.get('/{prefix}/results/list')
def get_results_list(prefix):
    mongodb = MongoDB()
    results_list = {}
    for result in mongodb.find('models',prefix):
        results_list[result["name"]] = result
    mongodb.close()
    return results_list