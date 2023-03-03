from tbmods.filters import Filters
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.klines import Klines
from tbmods.cache import Cache
from datetime import datetime
from tbmods.log import Log
import pandas as pd
import joblib

config = Config()
log = Log(config['app'])

class Market:
    
    def __init__(self,prefix,symbol,period,stable,coin):
        self.wallet = {}
        self.status = {}
        self.coin = coin
        self.stable = stable
        self.prefix = prefix
        self.symbol = symbol
        self.period = period
        self.open_trades = {}
        self.close_trades = {}
        self.klines = Klines(symbol,period)
        self.name = "{}-{}".format(prefix.upper(),datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.tech_model = joblib.load('/var/cache/models/{}'.format(config['tech_selected_model']))
        self.scaler = joblib.load('/var/cache/models/{}.scaler'.format(config['tech_selected_model']))

    def set_time(self,time):
        self.time = time

    def get_price(self):
        try:
            self.price = self.klines.df.loc[self.time].close
            log.info("{} - Price is {}".format(self.time,self.price))
            return True
        except KeyError:
            log.info("{} - Unable to get price".format(self.time))
            return False

    def get_klines(self):
        try:
            start = self.time - pd.Timedelta(hours=2)
            end = self.time + pd.Timedelta(hours=2)
            print(start)
            print(end)
            self.klines.load_df(start,end)
            return True
        except KeyError:
            log.info("{} - Unable to get klines".format(self.time))
            return False

    def get_event(self):
        self.events = Filters(self.klines.df.close).cusum_events()
        return True if self.time in self.events else False
        
    def predict(self,event):
        prediction = self.tech_model.predict_proba(event)[0]
        switch = {
            0: "bearish",
            1: "rangish",
            2: "bullish"
        }
        return switch[list(prediction).index(max(prediction))],max(prediction)
        
    def trigger(self,event=False):
        if event is not False:
            state = self.predict( event)
            switch = {
                "bearish": self.trigger_bearish,
                "rangish": self.trigger_rangish,
                "bullish": self.trigger_bullish
            }
            log.info("{} - Got event seems {} confidence {}".format(self.time,state[0],state[1]))
            switch[state[0]](state[1])
        else: self.cut_stop_loss()

    def up_stop_loss(self,confidence):
        for time in self.open_trades:
            self.open_trades[time]['jumps'] += 1
            self.open_trades[time]['stop_loss'] += self.price*((1-confidence)*self.open_trades[time]['jumps']*3)

    def cut_stop_loss(self):
        for time in self.open_trades.copy():
            if self.price < self.open_trades[time]['stop_loss']: self.sell(time)

    def trigger_bearish(self,confidence):
        self.up_stop_loss(confidence)
        self.cut_stop_loss()
        
    def trigger_rangish(self,confidence):
        self.cut_stop_loss()
        
    def trigger_bullish(self,confidence):
        self.buy(confidence * self.wallet[self.stable])
        
    def exit(self):
        for time in self.open_trades.copy():
            self.sell(time)

    def update_status(self,update):
        cache = Cache(config['app'])
        if type(update) is bool: self.status = {}
        else: self.status.update(update)
        cache.data["{}/status".format(self.prefix)] = self.status
        cache.write()
        
    def load_meta(self):
        mongodb = MongoDB()
        meta = mongodb.find_one('market','paper')
        mongodb.close()
        if meta is None: meta = {}
        if 'name' in meta: self.name = meta['name']
        if 'stable' in meta: self.stable = meta['stable']
        if 'stable_start' in meta: self.stable_start = meta['stable_start']
        if 'coin' in meta: self.coin = meta['coin']
        if 'coin_start' in meta: self.coin_start = meta['coin_start']
        if 'wallet' in meta: self.wallet = meta['wallet']
        if 'open_trades' in meta: self.open_trades = meta['open_trades']
        if 'close_trades' in meta: self.close_trades = meta['close_trades']
    
    def save_meta(self):
        meta = {
            "name": self.name,
            "stable": self.stable,
            "stable_start": self.stable_start,
            "coin": self.coin,
            "coin_start": self.coin_start,
            "wallet": self.wallet,
            "close_trades": {str(time): trade for time, trade in self.close_trades.items()},
            "open_trades": {str(time): trade for time, trade in self.open_trades.items()},
        }
        mongodb = MongoDB()
        mongodb.update('market',self.prefix,meta,{"name":self.name},True)
        mongodb.close()