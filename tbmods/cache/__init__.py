import json
import os

class Cache:
    
    def __init__(self,app):
        self.app = app
        self.data = {}
        self.path = "/var/cache/{}/cache.json".format(self.app)
        self.load()
        
    def load(self):
        if not os.path.exists(self.path): return {}
        with open(self.path) as cache:
            self.data = json.load(cache)
        
    def write(self):
        with open(self.path, 'w') as cache:
            json.dump(self.data, cache)
        