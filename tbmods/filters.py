import pandas as pd
import json

class Filters:
    
    def __init__(self,close):
        self.close = close

    def cusum_events(self,threshold):
        threshold = float(threshold)/100
        cusum_events = pd.DataFrame(columns=['event'])
        close_diff = self.close.pct_change().dropna()
        for date in close_diff.index:
            if close_diff.loc[date] < -threshold: cusum_events = pd.concat([cusum_events,pd.DataFrame({'event':close_diff.loc[date]},index=[date])])
            elif close_diff.loc[date] > threshold: cusum_events = pd.concat([cusum_events,pd.DataFrame({'event':close_diff.loc[date]},index=[date])])
        return cusum_events