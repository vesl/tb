from tbmods.questdb import QuestDB
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd

config = Config()
log = Log(config['app'])

class Klines:
    
    def __init__(self,symbol):
        self.symbol = symbol
        self.questdb = QuestDB()
        self.table = "live_{}".format(self.symbol)
        self.columns = ['open_time','open','high','close','low','volume','close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore']

    def qdb_to_df(self,result):
        df = pd.DataFrame(result,columns=self.columns)
        df.open_time = pd.to_datetime(df.open_time,utc=True)
        df.close_time = pd.to_datetime(df.close_time,utc=True)
        df.set_index('open_time',inplace=True)
        return df
        
    def binance_to_df(self,result):
        df = pd.DataFrame(result,columns=self.columns)
        df.open_time = pd.to_datetime(df.open_time,utc=True,unit='ms')
        df.close_time = pd.to_datetime(df.close_time,utc=True,unit='ms')
        df.set_index('open_time',inplace=True)
        return df
        
    def get_last_stored(self):
        qdbr = self.questdb.query("SELECT * FROM {} ORDER BY open_time DESC LIMIT 1".format(self.table))
        self.last_stored = self.qdb_to_df(qdbr['result'])
        
    def ingest(self):
        self.df.index = self.df.index.astype(int)
        self.df.close_time = self.df.close_time.astype(int)
        rows = ["{}, open={},high={},low={},close={},volume={},close_time={}t,quote_asset_volume={},number_of_trades={}i,taker_buy_base_asset_volume={},taker_buy_quote_asset_volume={},ignore={} {}".format(
            self.table,
            row.open,
            row.high,
            row.low,
            row.close,
            row.volume,
            int(row.close_time/1000),
            row.quote_asset_volume,
            row.number_of_trades,
            row.taker_buy_base_asset_volume,
            row.taker_buy_quote_asset_volume,
            row.ignore,
            row.Index,
        ) for row in self.df.itertuples()]
        return self.questdb.ingest(rows)
        
    def load_df(self,table,start,end):
        qdbr = self.questdb.query("SELECT * FROM {}_{} where open_time between '{}' and '{}'".format(table,self.symbol,start,end))
        self.df = self.qdb_to_df(qdbr['result'])
