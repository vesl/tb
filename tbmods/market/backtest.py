from tbmods.market import Market
from tbmods.config import Config
from tbmods.log import Log

config = Config()
log = Log(config['app'])

class MarketBacktest(Market):
    
    def __init__(self,stable,stable_start,coin,coin_start):
        super().__init__('backtest',stable,coin)
        self.coin_start = coin_start
        self.stable_start = stable_start
        self.wallet[self.coin] = coin_start
        self.wallet[self.stable] = stable_start

    def sell(self,time):
        qty = self.open_trades[time]['qty']
        offer = (qty * self.price)*0.99
        if offer > 20:
            self.wallet[self.stable] += offer
            self.wallet[self.coin] -= qty
            if self.wallet[self.coin] < 0: self.wallet[self.coin] = 0
            self.close_trades[time] = self.open_trades[time]
            self.close_trades[time].update({"sell_time": self.time, "sell_price": self.price, "offer": offer})
            self.open_trades.pop(time)
            log.info("Sell {} for {} price {} {} : {} {} : {}".format(qty,offer,self.price,self.stable,self.wallet[self.stable],self.coin,self.wallet[self.coin]))
        else: log.info("Unable to sell {} wallet {}".format(qty,self.wallet[self.coin]))

    def buy(self,bid):
        qty = (bid / self.price)*0.99
        if bid > 50 and self.wallet[self.stable] - bid >= 0:
            self.wallet[self.stable] -= bid
            self.wallet[self.coin] += qty
            self.open_trades[self.time] = { "qty": qty, "bid": bid, "buy_price": self.price, "buy_time": self.time, "jumps":0, "stop_loss": self.price*0.9 }
            log.info("Buy {} for {} price {} {} : {} {} : {}".format(qty,bid,self.price,self.stable,self.wallet[self.stable],self.coin,self.wallet[self.coin]))
            return True
        else: log.info("Unable to buy {} wallet {}".format(bid,self.wallet[self.stable]))