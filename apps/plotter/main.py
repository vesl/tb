from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plotter.routers import finance

## init api
app = FastAPI(
    title="Plotter",
    description="Generate plots to analyze data",
    version="1.0.0"
)

## init routers
app.include_router(finance.router)
