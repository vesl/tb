from trainer.routers import features, datasets, models
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os

## init env vars
os.environ["STATUS"] = "0"

## init api
app = FastAPI(
    title="Trainer",
    description="Train models from dataset",
    version="1.0.0"
)
## cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
## init routers
app.include_router(features.router)
app.include_router(datasets.router)
app.include_router(models.router)