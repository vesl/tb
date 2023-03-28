from tbmods.indicators.financial import Financial
import pandas as pd
import json

class Events:
    
    def __init__(self,klines):
        self.klines = klines

    def cusum_events(self,threshold):
        threshold = float(threshold)/100
        self.df = pd.DataFrame(columns=['event'])
        close_diff = self.klines.close.pct_change().dropna()
        for date in close_diff.index:
            if close_diff.loc[date] < -threshold: self.df = pd.concat([self.df,pd.DataFrame({'event':close_diff.loc[date]},index=[date])])
            elif close_diff.loc[date] > threshold: self.df = pd.concat([self.df,pd.DataFrame({'event':close_diff.loc[date]},index=[date])])
        return self.df

    def get_chartist_events(self,chartist_features):
        financial = Financial(self.klines)
        self.df = pd.DataFrame(index=self.klines.index)
        for chartist_feature in chartist_features:
            self.df = self.df.join(financial.compute(chartist_feature).rename(chartist_feature))
        self.df = self.df[(self.df!=0).any(axis=1)]