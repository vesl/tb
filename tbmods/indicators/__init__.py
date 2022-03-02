from tbmods.candles import Candles
import pandas as pd
import talib

class Indicators:
    
    def __init__(self,candles=None):
        self.candles=candles 
        
    def candles_from_questdb(self,timescale,from_date,to_date):
        candles = Candles()
        qdbr = candles.from_questdb(timescale,from_date,to_date)
        if 'error' in qdbr: return qdbr
        self.candles = candles.candles
        return qdbr
    
    def load_indicator(self,feature):
        switch = {
            'rsi':self.compute_rsi
        }
        return switch[feature]()

    def compute_rsi(self):
        rsi = talib.RSI(self.candles['close'], timeperiod=14)
        self.candles = self.candles.join(rsi.rename('rsi'))
        return ('rsi' in self.candles.columns)