from fastapi import FastAPI
from trader.routers import status, backtest

## init api
app = FastAPI(
    title="Trader",
    description="Trade",
    version="1.0.0"
)
## init routers
app.include_router(status.router)
app.include_router(backtest.router)