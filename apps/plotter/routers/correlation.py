from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
import matplotlib.pyplot as plt
from tbmods.triple_barrier import TripleBarrier
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler
from tbmods.dataset import Dataset
from tbmods.filters import Filters
from tbmods.config import Config
import seaborn as sns
import pandas as pd
import json

router = APIRouter(
    prefix="/correlation",
    tags=["correlation"],
)

config = Config()
sns.set(font_scale=0.5,rc = {'figure.figsize':(11,5)})

@router.get('/chi2/{timescale}/{from_date}/{to_date}/chi2.png')
def graph_balance(timescale,from_date,to_date):
    config['features'] = json.loads(config['features'])
    features_avail = ",".join(config['features']['sources']['qdb']+config['features']['sources']['talib'])
    dataset = Dataset(timescale,from_date,to_date,features_avail).load()
    columns = dataset.columns
    cusum = Filters(dataset['close']).cusum_events(config['cusum_pct_threshold'])
    labels = TripleBarrier(dataset['close'],cusum).barriers['side']
    index = dataset.index.intersection(labels.index)
    dataset = dataset.loc[index]
    labels = labels.loc[index]
    # merge features and labels
    scaler = MinMaxScaler()
    dataset = scaler.fit_transform(dataset)
    chi2_test = pd.DataFrame([chi2(dataset,labels)[0]],columns=columns)
    # graph
    fig,ax = plt.subplots()
    sns.heatmap(chi2_test,ax=ax)
    fig.savefig('/tmp/chi2.png')
    fig.clf()
    return FileResponse('/tmp/chi2.png',media_type="image/png")