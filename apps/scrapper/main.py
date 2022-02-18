from fastapi import FastAPI
from binance.spot import Spot
from tbmods.config import Config

app = FastAPI(
    title="Scrapper",
    description="Scrap financial data from binance and store it in questdb",
    version="1.0.0"
)

config = Config()
binance_client = Spot(key=config['binance_api_key'], secret=config['binance_api_secret'])

@app.get("/scrap")
async def scrap():
    trades = binance_client.historical_trades(config['symbol'],limit=config['binance_hist_limit'],fromId=0)
    return "scrap"
