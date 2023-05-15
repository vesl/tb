from tbmods.mongodb import MongoDB
from tbmods.config import Config
from bs4 import BeautifulSoup
from fastapi import APIRouter
from tbmods.log import Log
import requests
import re

router = APIRouter(
    prefix="/talib",
    tags=["talib"],
)

config = Config()
log = Log(config['app'])

@router.get('/get/functions_groups')
def get_functions_groups():
    return ["overlap_studies","momentum_indicators","volume_indicators","volatility_indicators","price_transform","cycle_indicators","pattern_recognition","statistic_functions","math_transform"]

@router.get('/get/features_maps')
def get_features_maps():
    mongodb = MongoDB()
    features_maps = []
    for doc in mongodb.find("TB_CONFIG","talib_features_maps"):
        features_maps.append(doc)
    mongodb.close()
    return features_maps
    
@router.get('/scrap')
def scrap_features_maps():
    mongodb = MongoDB()
    functions_groups = get_functions_groups()
    for functions_group in functions_groups:
        feature_map = { "function_group": functions_group, "features": {} }
        url = "https://ta-lib.github.io/ta-lib-python/func_groups/{}.html".format(functions_group)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for function in  soup.select('pre'):
            rets = re.findall(r'(.*) = ',function.text)[0].replace(' ','').split(',')
            for ret in rets:
                function_name = re.findall(r'(\w+)\(',function.text)[0]
                if function_name == "MAVP": continue
                feature_name = function_name if len(rets) == 1 else "{}_{}".format(function_name,ret)
                feature_map["features"][feature_name] = {}
                args = re.findall(r'\((.*)\)',function.text)[0].replace(' ','').split(',')
                feature_map["features"][feature_name]["kline_args"] = [arg for arg in args if not "=" in arg]
                feature_map["features"][feature_name]["args"] = { arg.split('=')[0]: arg.split('=')[1] for arg in args if "=" in arg }
        mongodb.update("TB_CONFIG","talib_features_maps",feature_map,{"function_group":functions_group},True)
    mongodb.close()
    return "done"