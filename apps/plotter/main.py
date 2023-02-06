from fastapi import FastAPI
from plotter.routers import dataset,labels,models,market

## init api
app = FastAPI(
    title="Plotter",
    description="Generate plots to analyze data",
    version="1.0.0"
)

## init routers
app.include_router(dataset.router)
app.include_router(labels.router)
app.include_router(models.router)
app.include_router(market.router)