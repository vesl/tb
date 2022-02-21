from fastapi import APIRouter, HTTPException
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import pandas as pd

router = APIRouter(
    prefix="/trades",
    tags=["trades"],
)

config = Config()
log = Log(config['app'])
cache = Cache(config['app'])

#@router.get('/store')
#def 
    