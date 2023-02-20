from tbmods.config import Config
from tbmods.log import Log
import requests
import socket

config = Config()
log = Log(config['app'])

class QuestDB:
    """
    Perform requests on questdb
    
    Object returned should be always query_response dict (never string or bool, int ..)
    query_response['error'] defined if error occured
    query_response['result'] defined if no error occured
    
    Processing error and result key outside this class
    """
    
    def __init__(self):
        self.host = config['questdb_host']
        self.table_historical_trades = 'historical_trades'
            
    def query(self,query):
        """
        If query is select, result of query is in response['dataset']
        """
        query_response = {}
        params = {"query":query,"fmt":"json"}
        try:
            response = requests.get("http://{}:9000/exec".format(self.host),params=params).json()
            if 'error' in response: log.error("QuestDB : {}".format(response['error']))
            if 'dataset' in response: query_response['result'] = response['dataset']
        except requests.exceptions.RequestException as e:
            query_response['error'] = e
        return query_response
        
    def ingest(self,data):
        """
        Ingest using influxdb protocol
        """
        query_response = {}
        data = "\n".join(data)+"\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, 9009))
            sock.sendall(data.encode())
        except socket.error as e:
            query_response['error'] = e
        sock.close()
        return query_response
            