from tbmods.config import Config
import pandas as pd

config = Config()

class TripleBarrier:
    
    def __init__(self,close,events):
        self.close = close
        self.vol = self.get_vol(self.close)
        # init barriers
        self.barriers = pd.DataFrame({
            "close":self.close.loc[events.index].values,
            "events":events.event.loc[events.index].values},
            index=events.index)
        self.apply_horizontal_barriers(config['tbm_up_thresh'],config['tbm_down_thresh'])
        self.apply_vertical_barrier()
        self.get_first_touch()
        self.get_sides()

    def get_vol(self,close):
        periods = close.index[:-1]
        next_periods = close.index[1:]
        rets = close.loc[periods]/close.loc[next_periods].values-1
        vol =  rets.ewm(span=config['period_vol_span']).std().dropna()
        return vol
        
    def apply_horizontal_barriers(self,up_thresh,down_thresh):
        top = []
        bot = []
        for date,row in self.barriers.iterrows():
            price = row.close
            volat = self.vol.loc[date]
            top.append(price+(price*volat*float(up_thresh)))
            bot.append(price-(price*volat*float(down_thresh)))
        self.barriers['top'] = top
        self.barriers['bot'] = bot
        self.barriers.dropna(inplace=True)
        
    def apply_vertical_barrier(self):
        vertical = self.barriers.index[1:]
        # drop last row because cant guess future event time
        self.barriers.drop(self.barriers.tail(1).index,inplace=True)
        self.barriers['vertical'] = vertical
        
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
            if row['close_touch'] <= row.bot: sides.append(-1)
            if row['close_touch'] < row.top and row['close_touch'] > row.bot: sides.append(0)
        self.barriers['side'] = sides