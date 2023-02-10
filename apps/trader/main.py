from fastapi import FastAPI
from trader.routers import status, market

## init api
app = FastAPI(
    title="Trader",
    description="Trade",
    version="1.0.0"
)
## init routers
app.include_router(status.router)
app.include_router(market.router)