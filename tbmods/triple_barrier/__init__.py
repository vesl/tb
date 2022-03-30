from tbmods.config import Config
import pandas as pd

config = Config()

class TripleBarrier:
    
    def __init__(self,candles,events):
        self.close = candles.close
        self.events = events
        self.get_daily_vol()
        # sync indexes on daily_vol which has less rows
        self.close = self.close.loc[self.close.index.intersection(self.daily_vol.index)]
        self.events = self.events.loc[self.events.index.intersection(self.daily_vol.index)]

    def get_daily_vol(self):
        df0=self.close.index.searchsorted(self.close.index-pd.Timedelta(days=1))
        df0=df0[df0>0]
        df0=pd.Series(self.close.index[(df0-1)], index=self.close.index[self.close.shape[0]-df0.shape[0]:])
        df0=self.close.loc[df0.index]/self.close.loc[df0.values].values-1 # daily returns 
        df0=df0.ewm(span=config['daily_vol_span']).std()
        self.daily_vol = df0
        
    def apply_horizontal_barriers(self,up_thresh,down_thresh):
        horizontal_barriers = []
        for date,row in self.events.iterrows():
            price = self.close.loc[date]
            volat = self.daily_vol.loc[date]
            up = price+(price*volat*float(up_thresh))
            down = price+(price*volat*float(down_thresh))
            horizontal_barriers.append({'up':up,'down':down})
        self.horizontal_barriers = pd.DataFrame(horizontal_barriers,index=self.events.index)
        
    def apply_vertical_barrier(self):
        vertical = list(self.events.index)
        vertical.pop(0)
        vertical.append(None)
        self.events['vertical'] = vertical
        
    def to_json(self):
        df = pd.concat([self.events,self.horizontal_barriers],axis=1)
        df.dropna(inplace=True)
        return df.to_json()