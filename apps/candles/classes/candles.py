from tbmods.questdb import QuestDB
from tbmods.config import Config
from tbmods.log import Log

config = Config()
log = Log(config['app'])
qdb = QuestDB(config)

class Candles:
    
    def __init__(self,df,**kwargs):
        self.df = df
        self.timescale = kwargs['timescale']
        self.table = 'candles_{}'.format(self.timescale)
        
    def ingest(self):
        # create table candles_minute (open double, high double, low double, close double, volume double , candle_time timestamp)
        for i,candle in self.df.iterrows():
            qdbq = 'insert into {} values ({},{},{},{},{},{})'.format(
                self.table,
                candle.open,
                candle.high,
                candle.low,
                candle.close,
                candle.volume,
                int(candle.candle_time*1000*1000)
            )
            qdbr = qdb.query(qdbq)
            if 'error' in qdbr: 
                log.error('Failed to insert candle into questdb {}'.format(qdbr['error']))
                return False
        return True
        