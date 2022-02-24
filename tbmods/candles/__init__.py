from tbmods.questdb import QuestDB
import pandas as pd

questdb = QuestDB()

class Candles:
    
    def __init__(self,candles=None):
        self.candles = candles
    
    def from_trades(self,trades):
        # care of index and manage types
        df = pd.DataFrame(trades)
        df = df.set_index('time').sort_index()
        df.index = pd.to_datetime(df.index,unit='ms')
        df.qty = df.qty.astype(float)
        # create candles agregation
        df = df.resample('1Min').agg({'price':['first','max','min','last'],'qty':'sum','id':'last'})
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
        # rename cols ohlc compliant
        df = df.rename({'price_first':'open','price_max':'high','price_min':'low','price_last':'close','qty_sum':'volume'},axis=1)
        # maybe the last minute is not finished, do drop last candle
        if df.shape[0] == 1: return False
        df.drop(df.tail(1).index,inplace=True)
        df.dropna(inplace=True)
        # get last_id and return it
        last_id = int(df.iloc[-1:].id_last.values)
        df.drop('id_last',axis=1,inplace=True)
        self.candles = df
        return last_id
        
    def from_questdb(self,timescale,since,to):
        qdbq = """select first(open),max(high),min(low),last(close),sum(volume),timestamp 
              from candles_minute where timestamp between '{}' and '{}' sample by {}""".format(since,to,timescale)
        qdbr = questdb.query(qdbq)
        if 'error' in qdbr: return qdbr
        elif len(qdbr['result']) == 0: qdbr['error'] = '0 candle in this period'
        else:
            df = pd.DataFrame(qdbr['result'],columns=['open','high','low','close','volume','timestamp'])
            df = df.set_index('timestamp').sort_index()
            self.candles = df
        # we return qdbr to know if there is error
        return qdbr
        
    def ingest(self):
        self.candles.index = self.candles.index.astype(int)
        data = ["candles_minute, open={},high={},low={},close={},volume={} {}".format(
            candle.open,
            candle.high,
            candle.low,
            candle.close,
            candle.volume,
            candle.Index
        ) for candle in self.candles.itertuples()]
        return questdb.ingest(data)
        
        