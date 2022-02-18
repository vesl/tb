import requests

class QuestDB:
    
    def __init__(self,config):
        self.host = config['questdb_host']
        
    def insert(self,table,values):
        # values has to be transformed as string to allow ",".join() , can't concatenate different types
        values = ",".join(map(str,values))
        params = {"query":"insert into {} values({})".format(table,values),'fmt':'json'}
        try:
            response = requests.get("http://{}/exec".format(self.host),params=params).json()
            if 'ddl' in response and response['ddl'] == 'OK': return True
            elif 'error' in response: return response['error']
            else: return response
        except requests.exceptions.RequestException as e:
            return e
            