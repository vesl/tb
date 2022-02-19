import requests

class QuestDB:
    """
    Perform requests on questdb
    
    Object returned should be always query_response dict (never string or bool, int ..)
    query_response['error'] defined if error occured
    query_response['result'] defined if no error occured
    
    Processing error and result key outside this class
    """
    
    def __init__(self,config):
        self.host = config['questdb_host']
        self.table_historical_trades = 'historical_trades'

    def insert_binance_trade(self,values):
        """
        Instert 1 trade into questdb
        Return OK into result if trade was properly ingested
        """
        # values has to be transformed as string to allow ",".join() , can't concatenate different types
        values = ",".join(map(str,values))
        query = "insert into {} values({})".format(self.table_historical_trades,values)
        return self.query(query)
            
    def get_latest_binance_trade(self,symbol):
        """
        Return latest binance trade into result exists
        """
        query = "select id from {} where symbol = '{}' latest on trade_time partition by symbol".format(self.table_historical_trades,symbol)
        query_response = self.query(query)
        # Rework query_response['result'] to achieve method purpose => return last_trade_id
        if 'result' in query_response: 
            # When db is empty, before the first scrap
            if len(query_response['result']) == 0: query_response['result'] = 0
            else: query_response['result'] = max(query_response['result'][0])
        return query_response
            
    def query(self,query):
        """
        If query is select, result of query is in response['dataset']
        """
        query_response = {}
        params = {"query":query,"fmt":"json"}
        try:
            response = requests.get("http://{}/exec".format(self.host),params=params).json()
            if 'error' in response: query_response['error'] = response['error']
            if 'dataset' in response: query_response['result'] = response['dataset']
            else: query_response['result'] = 'OK'
        except requests.exceptions.RequestException as e:
            query_response['error'] = e
        return query_response
            