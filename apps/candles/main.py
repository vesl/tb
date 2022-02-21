from fastapi import FastAPI
from .routers import trades

## init api
app = FastAPI(
    title="Candles",
    description="Store list of trades as minute candles, compile those ones as hourly, daily, weekly etc. candles",
    version="1.0.0"
)
## init routers
app.include_router(trades.router)