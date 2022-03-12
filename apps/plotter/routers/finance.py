from fastapi import APIRouter, HTTPException
from tbmods.candles import Candles
from tbmods.config import Config
from tbmods.cache import Cache
from tbmods.log import Log
import requests
import json

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)

config = Config()
log = Log(config['app'])

def lightweight_chart(candles):
    """
    Format candles for lightweight chart
    """
    candles.candles['time'] = candles.candles.index.astype(int)/1000000000
    return candles.candles.to_json(orient="records")

def get_features(features,timescale,from_date,to_date):
    """
    Pull features json data from dataset
    """
    r = requests.get('http://dataset/features/{}/{}/{}/{}'.format(features,timescale,from_date,to_date))
    if r.status_code != 200: features = {'error':'Unable to get dataset data'}
    else: features = json.loads(r.json())
    return features

@router.get('/candles/{timescale}/{from_date}/{to_date}')
async def graph_candles(timescale,from_date,to_date):
    """
    Get candles olhc from dataset and return it as json for lightweight-chart
    """
    features = get_features('open,high,low,close',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/volume/{timescale}/{from_date}/{to_date}')
async def graph_volume(timescale,from_date,to_date):
    """
    Get volume from dataset and return it as json for lightweight-chart
    """
    features = get_features('volume',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/rsi/{timescale}/{from_date}/{to_date}')
async def graph_rsi(timescale,from_date,to_date):
    """
    Get rsi from dataset and return it as json
    """
    features = get_features('rsi',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/macd/{timescale}/{from_date}/{to_date}')
async def graph_macd(timescale,from_date,to_date):
    """
    Get macd from dataset and return it as json
    """
    features = get_features('macd',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/macdsignal/{timescale}/{from_date}/{to_date}')
async def graph_macdsignal(timescale,from_date,to_date):
    """
    Get macd from dataset and return it as json
    """
    features = get_features('macdsignal',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/macdhist/{timescale}/{from_date}/{to_date}')
async def graph_macdhist(timescale,from_date,to_date):
    """
    Get macdhist from dataset and return it as json
    """
    features = get_features('macdhist',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/adx/{timescale}/{from_date}/{to_date}')
async def graph_adx(timescale,from_date,to_date):
    """
    Get adx from dataset and return it as json
    """
    features = get_features('adx',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/adxr/{timescale}/{from_date}/{to_date}')
async def graph_adxr(timescale,from_date,to_date):
    """
    Get adxr from dataset and return it as json
    """
    features = get_features('adxr',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/apo/{timescale}/{from_date}/{to_date}')
async def graph_apo(timescale,from_date,to_date):
    """
    Get apo from dataset and return it as json
    """
    features = get_features('apo',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/aroonup/{timescale}/{from_date}/{to_date}')
async def graph_aroonup(timescale,from_date,to_date):
    """
    Get aroonup from dataset and return it as json
    """
    features = get_features('aroonup',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/aroondown/{timescale}/{from_date}/{to_date}')
async def graph_aroondown(timescale,from_date,to_date):
    """
    Get aroondown from dataset and return it as json
    """
    features = get_features('aroondown',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/aroonosc/{timescale}/{from_date}/{to_date}')
async def graph_aroonsc(timescale,from_date,to_date):
    """
    Get aroonosc from dataset and return it as json
    """
    features = get_features('aroonosc',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/bop/{timescale}/{from_date}/{to_date}')
async def graph_bop(timescale,from_date,to_date):
    """
    Get bop from dataset and return it as json
    """
    features = get_features('bop',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/cci/{timescale}/{from_date}/{to_date}')
async def graph_cci(timescale,from_date,to_date):
    """
    Get cci from dataset and return it as json
    """
    features = get_features('cci',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/cmo/{timescale}/{from_date}/{to_date}')
async def graph_cmo(timescale,from_date,to_date):
    """
    Get cmo from dataset and return it as json
    """
    features = get_features('cmo',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/dx/{timescale}/{from_date}/{to_date}')
async def graph_dx(timescale,from_date,to_date):
    """
    Get dx from dataset and return it as json
    """
    features = get_features('dx',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/mfi/{timescale}/{from_date}/{to_date}')
async def graph_mfi(timescale,from_date,to_date):
    """
    Get mfi from dataset and return it as json
    """
    features = get_features('mfi',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/minusdi/{timescale}/{from_date}/{to_date}')
async def graph_minusdi(timescale,from_date,to_date):
    """
    Get minusdi from dataset and return it as json
    """
    features = get_features('minusdi',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/minusdm/{timescale}/{from_date}/{to_date}')
async def graph_minusdm(timescale,from_date,to_date):
    """
    Get minusdm from dataset and return it as json
    """
    features = get_features('minusdm',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/mom/{timescale}/{from_date}/{to_date}')
async def graph_mom(timescale,from_date,to_date):
    """
    Get mom from dataset and return it as json
    """
    features = get_features('mom',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/plusdi/{timescale}/{from_date}/{to_date}')
async def graph_plusdi(timescale,from_date,to_date):
    """
    Get plusdi from dataset and return it as json
    """
    features = get_features('plusdi',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/plusdm/{timescale}/{from_date}/{to_date}')
async def graph_plusdi(timescale,from_date,to_date):
    """
    Get plusdm from dataset and return it as json
    """
    features = get_features('plusdm',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/ppo/{timescale}/{from_date}/{to_date}')
async def graph_ppo(timescale,from_date,to_date):
    """
    Get ppo from dataset and return it as json
    """
    features = get_features('ppo',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/roc/{timescale}/{from_date}/{to_date}')
async def graph_roc(timescale,from_date,to_date):
    """
    Get roc from dataset and return it as json
    """
    features = get_features('roc',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/rocp/{timescale}/{from_date}/{to_date}')
async def graph_rocp(timescale,from_date,to_date):
    """
    Get rocp from dataset and return it as json
    """
    features = get_features('rocp',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/rocr/{timescale}/{from_date}/{to_date}')
async def graph_rocr(timescale,from_date,to_date):
    """
    Get rocr from dataset and return it as json
    """
    features = get_features('rocr',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/slowk/{timescale}/{from_date}/{to_date}')
async def graph_slowk(timescale,from_date,to_date):
    """
    Get slowk from dataset and return it as json
    """
    features = get_features('slowk',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/slowd/{timescale}/{from_date}/{to_date}')
async def graph_slowd(timescale,from_date,to_date):
    """
    Get slowk from dataset and return it as json
    """
    features = get_features('slowd',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/fastk/{timescale}/{from_date}/{to_date}')
async def graph_fastk(timescale,from_date,to_date):
    """
    Get fastk from dataset and return it as json
    """
    features = get_features('fastk',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/fastd/{timescale}/{from_date}/{to_date}')
async def graph_fastd(timescale,from_date,to_date):
    """
    Get fastd from dataset and return it as json
    """
    features = get_features('fastd',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/fastkrsi/{timescale}/{from_date}/{to_date}')
async def graph_fastkrsi(timescale,from_date,to_date):
    """
    Get fastkrsi from dataset and return it as json
    """
    features = get_features('fastkrsi',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/fastdrsi/{timescale}/{from_date}/{to_date}')
async def graph_fastdrsi(timescale,from_date,to_date):
    """
    Get fastdrsi from dataset and return it as json
    """
    features = get_features('fastdrsi',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/ultosc/{timescale}/{from_date}/{to_date}')
async def graph_ultosc(timescale,from_date,to_date):
    """
    Get ultosc from dataset and return it as json
    """
    features = get_features('ultosc',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/willr/{timescale}/{from_date}/{to_date}')
async def graph_ultosc(timescale,from_date,to_date):
    """
    Get willr from dataset and return it as json
    """
    features = get_features('willr',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/ichtenkan/{timescale}/{from_date}/{to_date}')
async def graph_tenkan(timescale,from_date,to_date):
    """
    Get tenkan from dataset and return it as json
    """
    features = get_features('ichtenkan',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/ichkijun/{timescale}/{from_date}/{to_date}')
async def graph_kijun(timescale,from_date,to_date):
    """
    Get kijun from dataset and return it as json
    """
    features = get_features('ichkijun',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/ichssa/{timescale}/{from_date}/{to_date}')
async def graph_ssa(timescale,from_date,to_date):
    """
    Get ssa from dataset and return it as json
    """
    features = get_features('ichssa',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/ichssb/{timescale}/{from_date}/{to_date}')
async def graph_ssb(timescale,from_date,to_date):
    """
    Get ssb from dataset and return it as json
    """
    features = get_features('ichssb',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)

@router.get('/ichlag/{timescale}/{from_date}/{to_date}')
async def graph_lagging_span(timescale,from_date,to_date):
    """
    Get lagging span from dataset and return it as json
    """
    features = get_features('ichlag',timescale,from_date,to_date)
    if 'error' in features: raise HTTPException(status_code=500,detail=features['error'])
    candles = Candles()
    candles.from_json(features)
    return lightweight_chart(candles)