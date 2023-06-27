from tbmods.config import Config
import pandas as pd
import numpy as np

config = Config()

class TripleBarrier:

    def __init__(self,close,events):
        self.close = close
        self.barriers = pd.DataFrame(self.close.loc[events.index].values,columns=['close'],index=events.index)
        self.get_horizontal_barriers(config['tbm_up_thresh'],config['tbm_down_thresh'])
        self.get_vertical_barrier()
        self.get_first_touch()
        self.get_side()
        
    def get_horizontal_barriers(self,up_thresh,down_thresh):
        self.barriers['top'] = (self.barriers.close+(self.barriers.close*(float(up_thresh))))
        self.barriers['bot'] = (self.barriers.close-(self.barriers.close*(float(up_thresh))))

    def get_vertical_barrier(self):
        self.barriers['vertical'] = self.barriers.index + pd.Timedelta(hours=9)
        # create new index to remove missing vertical rows due to binance outage and last row because last vertical not exists yet
        index = pd.DatetimeIndex(self.barriers.vertical).intersection(self.barriers.index)[:-1]
        self.barriers = self.barriers.loc[index]
        
    def get_first_touch(self):
        def get_row_first_touch(row):
            touchs = []
            price_range = self.close.loc[row.name:row.vertical]
            touchs.append(row.vertical)
            if row.top <= price_range.max(): touchs.append(price_range.idxmax())
            if row.bot >= price_range.min(): touchs.append(price_range.idxmin())
            return min(pd.DatetimeIndex(touchs))
        self.barriers['first_touch'] = self.barriers.apply(get_row_first_touch,axis=1)
        self.barriers['close_touch'] = self.close.loc[self.barriers.first_touch].values
    
    def get_side(self):
        def get_row_side(row):
            if row.close_touch >= row.top: return 1
            elif row.close_touch <= row.bot: return -1
            else: return np.nan
        self.barriers['side'] = self.barriers.apply(get_row_side,axis=1)
        self.barriers.dropna(inplace=True)