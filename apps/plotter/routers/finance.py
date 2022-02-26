from fastapi import APIRouter, HTTPException
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

config = Config()
log = Log(config['app'])

@router.get('/price')
async def graph_price():
    return "ok"