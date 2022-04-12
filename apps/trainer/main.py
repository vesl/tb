from fastapi import FastAPI
from trainer.routers import status

## init api
app = FastAPI(
    title="Trainer",
    description="Train models from dataset",
    version="1.0.0"
)
## init routers
app.include_router(status.router)