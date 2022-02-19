from tbmods.questdb import QuestDB
from binance.spot import Spot
from tbmods.log import Log

class Scrapper:
    """
    historical_trades schema:
    create table historical_trades (
        id int,
        symbol symbol,
        price double,
        qty double,
        isBuyerMaker boolean,
        isBestMatch boolean,
        trade_time timestamp
    )
    """

    def __init__(self,config):
        self.symbol = config['symbol']
        self.last_id = 0
        self.trades = []
        self.questdb = QuestDB(config)
        self.log = Log(config['app'])
        self.binance_client = Spot(key=config['binance_api_key'], secret=config['binance_api_secret'])
        self.binance_hist_limit = config['binance_hist_limit']

    def get_last_id(self):
        questdb_response = self.questdb.get_latest_binance_trade(self.symbol)
        if 'error' in questdb_response: self.log.error("Unable to get last_id {}".format(questdb_response['error']))
        else: self.log.info("Last id ingested is {}".format(questdb_response['result']))
        if 'result' in questdb_response: self.last_id = questdb_response['result']
        return ('result' in questdb_response)

    def get_trades(self):
        self.trades = self.binance_client.historical_trades(self.symbol,limit=self.binance_hist_limit,fromId=self.last_id+1)
        self.log.info("Got {} trades from binance".format(len(self.trades)))
        return ((type(self.trades) == list) and (len(self.trades) > 0))

    def ingest_trades(self):
        ingest_count = 0
        for trade in self.trades:
            questdb_response = self.questdb.insert_binance_trade([
                trade['id'],
                # symbol has to be quoted
                "'{}'".format(self.symbol),
                trade['price'],
                trade['qty'],
                trade['isBuyerMaker'],
                trade['isBestMatch'],
                trade['time']*1000
            ])
            if 'error' in questdb_response:
                self.log.error("Unable to ingest trade {} {}".format(trade,questdb_response['error']))
                return False
            else: ingest_count+=1
        self.log.info("Ingested {} trades".format(ingest_count))
        return True