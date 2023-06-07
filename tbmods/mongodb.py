from tbmods.config import Config
from pymongo import MongoClient

config = Config()

class MongoDB:
    
    def __init__(self):
        self.client = MongoClient(config['mongodb_host'])

    def insert(self,db,collection,doc):
        self.client[db][collection].insert_one(doc)
        
    def find(self,db,collection,search={}):
        return self.client[db][collection].find(search,{"_id":0})
    
    def find_one(self,db,collection,search={}):
        return self.client[db][collection].find_one(search,{"_id":0})

    def groupby(self,db,collection,field):
        return self.client[db][collection].aggregate([{"$group":{"_id":"${}".format(field)}}])

    def update(self,db,collection,doc,match,upsert=False):
        self.client[db][collection].replace_one(match,doc,upsert)
    
    def close(self):
        self.client.close()