from tbmods.dataset.ichimoku import DatasetIchimoku
from tbmods.models import Model
from tbmods.config import Config
from tbmods.cache import Cache
from datetime import datetime
import pandas as pd
import joblib

config = Config()

class ModelIchimoku(Model):

    def __init__(self,symbol,period,start,end,features_list):
        super().__init__('ichimoku',symbol,period,start,end,features_list)

    def load_dataset(self):
        self.dataset = DatasetIchimoku(self.symbol,self.period,self.start,self.end,self.features_list)
        self.dataset.load_features()
        self.features_list = list(self.dataset.features.columns)
        self.dataset.load_labels()
        self.meta.update({
            "symbol":self.symbol,
            "period":self.period,
            "start":self.start,
            "end":self.end
        })