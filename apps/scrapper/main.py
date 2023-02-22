from scrapper.routers import klines
from fastapi import FastAPI

## init api
app = FastAPI(
    title="Scrapper",
    description="Scrap financial data from binance and store it in questdb",
    version="1.1.0"
)
## init routers
app.include_router(klines.router)