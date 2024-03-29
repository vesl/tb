from tbmods.questdb import QuestDB
from tbmods.config import Config
from tbmods.log import Log
import pandas as pd

config = Config()
log = Log(config['app'])

class Klines:
    
    def __init__(self,symbol,period):
        self.symbol = symbol
        self.period = period
        self.questdb = QuestDB()
        self.table = "{}_{}".format(self.period,self.symbol)
        self.columns = ['open_time','open','high','low','close','volume','close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore']

    def qdb_to_df(self,result):
        df = pd.DataFrame(result,columns=self.columns)
        df.open_time = pd.to_datetime(df.open_time,utc=True)
        df.close_time = pd.to_datetime(df.close_time,utc=True)
        df.set_index('open_time',inplace=True)
        return df
        
    def get_last_stored(self):
        avoid_cache = str(int(pd.Timestamp.utcnow().timestamp()*1000000))
        qdbr = self.questdb.query("SELECT * AS {} FROM {} ORDER BY open_time DESC LIMIT 1".format(avoid_cache,self.table))
        self.last_stored = self.qdb_to_df(qdbr['result'])
        
    def get_first_stored(self):
        qdbr = self.questdb.query("SELECT * FROM {} ORDER BY open_time ASC LIMIT 1".format(self.table))
        self.first_stored = self.qdb_to_df(qdbr['result'])
        
    def ingest(self,kline):
        kline[0] *= 1000
        kline[6] *= 1000
        qdbr = self.questdb.query("INSERT INTO {} VALUES ({})".format(self.table,",".join([str(v) for v in kline])))
        
    def load_df(self,start,end):
        qdbr = self.questdb.query("SELECT * FROM {} where open_time between '{}' and '{}'".format(self.table,start,end)) if start and end else self.questdb.query("SELECT * FROM {}".format(self.table))
        self.df = self.qdb_to_df(qdbr['result'])