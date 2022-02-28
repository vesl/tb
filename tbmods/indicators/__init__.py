from tbmods.candles import Candles

class Indicators:
    
    def __init__(self,candles=None):
        self.candles=candles 
        
    def candles_from_questdb(self,timescale,from_date,to_date):
        candles = Candles()
        qdbr = candles.from_questdb(timescale,from_date,to_date)
        if 'error' in qdbr: return qdbr
        self.candles = candles.candles
        return qdbr
    
    
    