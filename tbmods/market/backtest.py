from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.cache import Cache
from datetime import datetime
from tbmods.log import Log
import joblib

config = Config()
log = Log(config['app'])

class MarketBacktest:
    
    def __init__(self,stable,stable_start,coin,coin_start,time_period,time_start,time_end):
        self.name = "backtest-{}".format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.stable = stable
        self.stable_start = stable_start
        self.coin = coin
        self.coin_start = coin_start
        self.time_period = time_period
        self.time_start = time_start
        self.time_end = time_end
        self.wallet = {
            stable : stable_start,
            coin : coin_start,
        }
        self.open_trades = {}
        self.close_trades = {}
        self.tech_model = joblib.load('/var/cache/models/{}'.format(config['tech_selected_model']))
        
    def set_time(self,time):
        self.time = time
        
    def set_price(self,price):
        self.price = price
        
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
            state = self.predict(event)
            switch = {
                "bearish": self.trigger_bearish,
                "rangish": self.trigger_rangish,
                "bullish": self.trigger_bullish
            }
            log.info("{} - Got event seems {} confidence {}".format(self.time,state[0],state[1]))
            switch[state[0]](state[1])
            
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

    def sell(self,time):
        qty = self.open_trades[time]['qty']
        offer = (qty * self.price)*0.99
        if offer > 50 and self.wallet[self.coin] - qty >= 0:
            self.wallet[self.stable] += offer
            self.wallet[self.coin] -= qty
            self.close_trades[time] = self.open_trades[time]
            self.close_trades[time].update({"sell_time": self.time, "sell_price": self.price, "offer": offer})
            self.open_trades.pop(time)
            log.info("Sell {} for {} price {} {} : {} {} : {}".format(qty,offer,self.price,self.stable,self.wallet[self.stable],self.coin,self.wallet[self.coin]))
            return True
        else: return False

    def buy(self,bid):
        qty = (bid / self.price)*0.99
        if bid > 50 and self.wallet[self.stable] - bid > 0:
            self.wallet[self.stable] -= bid
            self.wallet[self.coin] += qty
            self.open_trades[self.time] = { "qty": qty, "bid": bid, "buy_price": self.price, "buy_time": self.time, "jumps":0, "stop_loss": self.price*0.9 }
            log.info("Buy {} for {} price {} {} : {} {} : {}".format(qty,bid,self.price,self.stable,self.wallet[self.stable],self.coin,self.wallet[self.coin]))
            return True
        else: return False
        
    def exit(self):
        for time in self.open_trades.copy():
            self.sell(time)

    def update_status(self,update):
        cache = Cache(config['app'])
        if type(update) is bool: self.status = {}
        else: self.status.update(update)
        cache.data["backtest/status"] = self.status
        cache.write()
    
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
            "time_period": self.time_period,
            "time_start": self.time_start,
            "time_end": self.time_end
        }
        mongodb = MongoDB()
        mongodb.update('market','backtest',meta,{"name":self.name},True)
        mongodb.close()