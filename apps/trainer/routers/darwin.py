from fastapi import APIRouter, HTTPException
from tbmods.pydantic_models import DarwinMap
from tbmods.mongodb import MongoDB
from tbmods.darwin import Darwin
from tbmods.config import Config
from tbmods.log import Log
import os

router = APIRouter(
    prefix="/darwin",
    tags=["darwin"],
)

config = Config()
log = Log(config['app'])

@router.get("/get/parameters_map")
def get_darwin_map():
    mongodb = MongoDB()
    parameters_map = mongodb.find("TB","darwin_maps",{})[0]["parameters"]
    return parameters_map

@router.post("/run/{symbol}")
def run_darwin(darwin_map: DarwinMap,symbol):
    darwin = Darwin(darwin_map.dataset_type,darwin_map.model_type,symbol,darwin_map.parameters_map)
    darwin.evolve()

