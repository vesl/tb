from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from tbmods.mongodb import MongoDB
from tbmods.config import Config
import matplotlib.pyplot as plt
from tbmods.log import Log
from io import BytesIO
import seaborn as sns
import base64
import json

router = APIRouter(
    prefix="/models",
    tags=["models"],
)

config = Config()
log = Log(config['app'])
mongodb = MongoDB()

@router.get('/tech/results/list')
def get_tech_results_list():
    tech_results_list = {}
    for tech_result in mongodb.find('models','tech'):
        tech_results_list[tech_result["name"]] = tech_result
    return tech_results_list