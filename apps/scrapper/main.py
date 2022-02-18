from fastapi import FastAPI
from tbmods.config import Config

app = FastAPI(
    title="Scrapper",
    description="Scrap financial data from binance and store it in questdb",
    version="1.0.0"
)

config = Config()

@app.get("/scrap")
def scrap():
    return "scrap"
