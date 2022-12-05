from fastapi import APIRouter, HTTPException
from tbmods.dataset import Dataset
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd
import requests
import json

router = APIRouter(
    prefix="/dataset",
    tags=["dataset"],
)

config = Config()
log = Log(config['app'])



# Format dataframe to lightwieght chart
def df_to_lc(df):
    df['time'] = df.index.astype(int)/1000000000
    return df.to_json(orient="records")

# Routes
@router.get('/tech/features')
async def tech_features():
    return config['tech_features']