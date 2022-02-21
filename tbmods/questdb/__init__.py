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
        except requests.exceptions.RequestException as e:
            query_response['error'] = e
        return query_response
            