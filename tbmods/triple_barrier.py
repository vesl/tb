from tbmods.config import Config
import pandas as pd
import numpy as np

config = Config()

class TripleBarrier:
    
    def __init__(self,close,events):
        self.close = close
        self.barriers = pd.DataFrame({"close":self.close.loc[events.index].values},index=events.index)
        self.get_horizontal_barriers(config['tbm_up_thresh'],config['tbm_down_thresh'])
        self.get_vertical_barrier()
        self.get_first_touch()
        self.get_sides()
        
    def get_horizontal_barriers(self,up_thresh,down_thresh):
        top = []
        bot = []
        for date,row in self.barriers.iterrows():
            price = row.close
            top.append(price+(price*float(up_thresh)))
            bot.append(price-(price*float(down_thresh)))
        self.barriers['top'] = top
        self.barriers['bot'] = bot
        self.barriers.dropna(inplace=True)
        
    def get_vertical_barrier(self):
        vertical = self.barriers.index + pd.Timedelta(hours=3)
        # drop last row because cant guess future event time
        self.barriers['vertical'] = vertical
        self.barriers.drop(self.barriers.tail(3).index,inplace=True)
        
    def get_first_touch(self):
        first_touchs = []
        for date,row in self.barriers.iterrows():
            price_range = self.close.loc[date:row.vertical]
            touchs = [row.vertical]
            if price_range.max() >= row.top: touchs.append(price_range.idxmax())
            elif price_range.min() <= row.bot: touchs.append(price_range.idxmin())
            first_touchs.append(min(pd.DatetimeIndex(touchs)))
        self.barriers['first_touch'] = first_touchs
    
    def get_sides(self):
        sides = []
        self.barriers['close_touch'] = self.close.loc[self.barriers.first_touch].values
        self.barriers['ret'] = (self.barriers.close_touch - self.barriers.close)/self.barriers.close
        for date,row in self.barriers.iterrows():
            if row['close_touch'] >= row.top: sides.append(1)
            elif row['close_touch'] <= row.bot: sides.append(-1)
            else: sides.append(np.nan)
        self.barriers['side'] = sides
        self.barriers.dropna(inplace=True)