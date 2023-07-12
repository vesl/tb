from sklearn.ensemble import RandomForestClassifier
from tbmods.mongodb import MongoDB

class ModelRandomForest:
    
    def __init__(self,dataset):
        self.dataset = dataset
    
    def load_map(self):
        mongodb = MongoDB()
        self._map = mongodb.find('TB','models_map',{'name':'random_forest'})[0]
        print(self._map)
