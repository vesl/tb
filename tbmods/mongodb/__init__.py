from tbmods.config import Config
from pymongo import MongoClient

config = Config()

class MongoDB:
    
    def __init__(self):
        self.client = MongoClient(config['mongodb_host'])

    def insert(self,db,collection,doc):
        self.client[db][collection].insert_one(doc)