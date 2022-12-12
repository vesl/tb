from fastapi import APIRouter, HTTPException
from tbmods.dataset.tech import DatasetTech
from tbmods.models.tech import ModelTech
from tbmods.config import Config
import matplotlib.pyplot as plt
from tbmods.log import Log
from io import BytesIO
import seaborn as sns
import base64

router = APIRouter(
    prefix="/dataset",
    tags=["dataset"],
)

config = Config()
log = Log(config['app'])

# Routes
@router.get('/tech/features/map')
async def tech_features_map():
    return config['tech_features']
    
@router.get('/tech/feature/{features}/{period}/{start}/{end}')
async def tech_features(features,period,start,end):
    dataset = DatasetTech(period,start,end,features.split(','))
    dataset.features["time"] = dataset.features.index.astype(int)/1000000000 #format data to LC
    return dataset.features.to_json(orient="records")

@router.get('/tech/correlation/{features}/{period}/{start}/{end}')
def graph_correlation(features,period,start,end):
    model = ModelTech(period,start,end,features.split(','))
    chi2_test = model.chi2_test()
    image = BytesIO()
    fig,ax = plt.subplots()
    sns.heatmap(chi2_test,ax=ax,annot=True,annot_kws={"fontsize":7},fmt=".0f")
    ax.set_ylabel("Correlation")
    ax.set_xlabel("Features")
    ax.set_xticklabels(model.dataset.features.columns,fontsize=8)
    fig.set_size_inches(15,10)
    fig.savefig(image, format='png')
    image_base64 = base64.b64encode(image.getvalue())
    return {"image_base64": image_base64}