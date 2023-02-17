from tbmods.market import Market
from tbmods.config import Config
from binance.spot import Spot
from tbmods.log import Log

config = Config()
log = Log(config['app'])

class MarketLive(Market):
    
    def __init__(self,stable,coin):
        self.binance_client = Spot(config['binance_api_key'],config['binance_api_secret'])
        super().__init__('live',stable,coin)
        self.wallet[self.coin] = self.get_balance(self.coin)
        self.wallet[self.stable] = self.get_balance(self.stable)
        
    def set_time(self,time):
        self.time = time
        
    def set_price(self,price):
        self.price = price

    def get_balance(self,asset):
        balance = [token['free'] for token in self.binance_client.account()['balances'] if token['asset'] == asset]
        if len(balance) > 0: return balance[0]
        else: log.error("Asset {} not found on binance".format(asset))

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