from fastapi import APIRouter, HTTPException
from tbmods.config import Config
from pydantic import BaseModel
from tbmods.log import Log
from typing import List
import pandas as pd

router = APIRouter(
    prefix="/trades",
    tags=["trades"],
)

config = Config()
log = Log(config['app'])

class Trade(BaseModel):
    id: str
    price: float
    qty: float
    isBuyerMaker: bool
    isBestMatch: bool
    time: int

class Trades(BaseModel):
    trades: List[Trade]

@router.put('/store')
def store_trades(trades: Trades):
    print(trades)
    return "OK"
    