from fastapi import FastAPI
from dataset.routers import status,features

## init api
app = FastAPI(
    title="Dataset",
    description="Build dataset from questdb data and indicators",
    version="1.0.0"
)

## init routers
app.include_router(features.router)
app.include_router(status.router)
