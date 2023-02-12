from fastapi import APIRouter, HTTPException
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.log import Log
import json

router = APIRouter(
    prefix="/market",
    tags=["market"],
)

config = Config()
log = Log(config['app'])
mongodb = MongoDB()

@router.get('/backtest/results/list')
def get_backtest_results_list():
    backtest_results_list = {}
    for backtest_result in mongodb.find('market','backtest'):
        backtest_results_list[backtest_result["name"]] = backtest_result
    return backtest_results_list
    
@router.get('/paper/results')
def get_paper_results():
    return mongodb.find_one('market','paper')