from fastapi import FastAPI
from plotter.routers import status,finance,labels,correlation

## init api
app = FastAPI(
    title="Plotter",
    description="Generate plots to analyze data",
    version="1.0.0"
)

## init routers
app.include_router(labels.router)
app.include_router(finance.router)
app.include_router(correlation.router)
app.include_router(status.router)