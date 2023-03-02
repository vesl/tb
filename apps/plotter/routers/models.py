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

@router.get('/tech/results/list')
def get_tech_results_list():
    mongodb = MongoDB()
    tech_results_list = {}
    for tech_result in mongodb.find('models','tech'):
        tech_results_list[tech_result["name"]] = tech_result
    mongodb.close()
    return tech_results_list