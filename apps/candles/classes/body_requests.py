from pydantic import BaseModel
from typing import List

class Trade(BaseModel):
    id: str
    price: float
    qty: float
    isBuyerMaker: bool
    isBestMatch: bool
    time: int

class Trades(BaseModel):
    trades: List[Trade]