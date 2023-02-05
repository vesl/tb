from tbmods.config import Config
from tbmods.log import Log
import joblib

config = Config()
log = Log(config['app'])

class MarketBacktest:
    
    def __init__(self,stable,stable_start,coin,coin_start):
        self.stable = stable
        self.stable_start = stable_start
        self.coin = coin
        self.coin_start = coin_start
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
            self.open_trades[time]['stop_loss'] += self.price*(1-confidence)
            self.open_trades[time]['jumps'] += 1

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
        offer = qty * self.price
        if offer > 50 and self.wallet[self.coin] - qty >= 0:
            self.wallet[self.stable] += offer
            self.wallet[self.coin] -= (qty * 0.99)
            self.close_trades[time] = self.open_trades[time]
            self.close_trades.update({"sell_time": time, "sell_price": self.price, "offer": offer})
            self.open_trades.pop(time)
            log.info("Sell {} for {} price {} {} : {} {} : {}".format(qty,offer,self.price,self.stable,self.wallet[self.stable],self.coin,self.wallet[self.coin]))
            return True
        else: return False

    def buy(self,bid):
        qty = bid / self.price
        if bid > 50 and self.wallet[self.stable] - bid > 0:
            self.wallet[self.stable] -= (bid * 0.99)
            self.wallet[self.coin] += qty
            self.open_trades[self.time] = { "qty": qty, "bid": bid, "buy_price": self.price, "buy_time": self.time, "jumps":0, "stop_loss": self.price*0.9 }
            log.info("Buy {} for {} price {} {} : {} {} : {}".format(qty,bid,self.price,self.stable,self.wallet[self.stable],self.coin,self.wallet[self.coin]))
            return True
        else: return False