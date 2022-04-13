from fastapi import FastAPI
from trainer.routers import status, models

## init api
app = FastAPI(
    title="Trainer",
    description="Train models from dataset",
    version="1.0.0"
)
## init routers
app.include_router(models.router)
app.include_router(status.router)