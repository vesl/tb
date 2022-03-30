from tbmods.candles import Candles
import pandas as pd
import json

class Filters:
    
    def __init__(self,close):
        self.close = close

    def cusum_events(self,threshold):
        threshold = threshold/100
        cusum_events = pd.DataFrame(columns=['event'])
        candles = Candles()
        candles.from_json(json.loads(self.close))
        close_diff = candles.candles['close'].pct_change().dropna()
        for date in close_diff.index:
            spos,sneg = 0,0
            spos,sneg = max(0,spos+close_diff.loc[date]),min(0,sneg+close_diff.loc[date])
            if sneg < -threshold: cusum_events = pd.concat([cusum_events,pd.DataFrame({'event':sneg},index=[date])])
            elif spos > threshold: cusum_events = pd.concat([cusum_events,pd.DataFrame({'event':spos},index=[date])])
        return cusum_events