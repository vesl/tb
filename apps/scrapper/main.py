from fastapi import FastAPI, HTTPException
from tbmods.config import Config
from scrapper import Scrapper

## init api
app = FastAPI(
    title="Scrapper",
    description="Scrap financial data from binance and store it in questdb",
    version="1.0.0"
)

## init dependencies
config = Config()
scrapper = Scrapper(config)

## scrap
@app.get("/scrap")
def scrap():
    """
    Scrap trades from last inserted into questdb to binance_hist_limit and insert result into questdb table trades_symbol
    This is not async because we check on database last inserted row, so we have to wait db write
    """
    # Getting last id ingested
    if scrapper.get_last_id() is False: HTTPException(status_code=500, detail="Unable to get last_id")
    # Getting 1000 following last id trades
    if scrapper.get_trades() is False: HTTPException(status_code=500, detail="Unable to get trades")
    # Insert them all into questDB
    if scrapper.ingest_trades() is False: HTTPException(status_code=500, detail="Unable to ingest trades")
    # Return number ingested counts
    return {"scrapping":"Done"}