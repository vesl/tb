from fastapi import FastAPI
from plotter.routers import dataset

## init api
app = FastAPI(
    title="Plotter",
    description="Generate plots to analyze data",
    version="1.0.0"
)

## init routers
app.include_router(dataset.router)