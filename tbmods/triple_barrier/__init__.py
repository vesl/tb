from tbmods.config import Config
import pandas as pd

config = Config()

class TripleBarrier:
    
    def __init__(self,close,events):
        self.close = close
        self.daily_vol = self.get_daily_vol(self.close)
        # sync indexes on daily_vol and events which has less rows
        index = events.index.intersection(self.daily_vol.index)
        # init barriers
        self.barriers = pd.DataFrame({
            "close":self.close.loc[index].values,
            "events":events.event.loc[index].values},
            index=index)
        self.apply_horizontal_barriers(config['tbm_up_thresh'],config['tbm_down_thresh'])
        self.apply_vertical_barrier()
        self.get_first_touch()
        self.get_sides()

    def get_daily_vol(self,close):
        days = close.index[:-1]
        next_days = close.index[1:]
        daily_rets = close.loc[days]/close.loc[next_days].values-1
        daily_vol=daily_rets.ewm(span=config['daily_vol_span']).std().dropna()
        return daily_vol
        
    def apply_horizontal_barriers(self,up_thresh,down_thresh):
        top = []
        bot = []
        for date,row in self.barriers.iterrows():
            price = row.close
            volat = self.daily_vol.loc[date]
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
            touchs = pd.DatetimeIndex([row.vertical])
            if price_range.max() >= row.top: touchs.append(price_range.index)
            if price_range.min() <= row.bot: touchs.append(price_range.index)
            first_touchs.append(min(touchs))
        self.barriers['first_touch'] = first_touchs
    
    def get_sides(self):
        sides = []
        self.barriers['close_touch'] = self.close.loc[self.barriers.first_touch].values
        self.barriers['ret'] = (self.barriers.close_touch - self.barriers.close)/self.barriers.close
        for date,row in self.barriers.iterrows():
            if (row.ret < float(config['tbm_min_ret'])) and (row.ret > -float(config['tbm_min_ret'])): sides.append(0)
            elif (row.ret > 0): sides.append(1)
            elif (row.ret < 0): sides.append(-1)
        self.barriers['side'] = sides