from fastapi.middleware.cors import CORSMiddleware
from scrapper.routers import klines, talib
from fastapi import FastAPI

## init api
app = FastAPI(
    title="Scrapper",
    description="Scrap financial data from binance and store it in questdb",
    version="1.1.0"
)
## cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
## init routers
app.include_router(klines.router)
app.include_router(talib.router)