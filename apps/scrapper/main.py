from fastapi import FastAPI
from scrapper.routers import klines

## init api
app = FastAPI(
    title="Scrapper",
    description="Scrap financial data from binance and store it in questdb",
    version="1.1.0"
)
## init routers
app.include_router(klines.router)