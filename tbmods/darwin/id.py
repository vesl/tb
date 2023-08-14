from tbmods.models.random_forest import ModelRandomForest
from tbmods.mongodb import MongoDB
import hashlib

class Id:
    
    def __init__(self,genom,dataset_type,model_type,symbol):
        self.genom = genom
        self.symbol = symbol
        self.model_type = model_type
        self.dataset_type = dataset_type
        self.uid = hashlib.md5(str(self.genom).encode()).hexdigest()
        self.dataset_name = f"{ self.dataset_type }-{ self.uid }"
        self.save_dataset()

    def train(self):
        if self.model_type == 'random_forest':
            self.model = ModelRandomForest(self.dataset_name,self.symbol,self.genom['model_map'])
            self.model.train()
            self.model.save()
  
    def save_dataset(self):
        mongodb = MongoDB()
        features_map_names = []
        for features_map in self.genom['features_maps']:
            features_map_names.append(f"{ features_map }-{ self.uid }")
            doc = {
                "name": features_map_names[-1],
                "features": self.genom['features_maps'][features_map]["features"],
                "source": self.genom['features_maps'][features_map]["source"],
                "darwin": True
            }
            mongodb.insert('TB','features_maps',doc)
        doc = {
            "name": self.dataset_name,
            "type": self.dataset_type,
            "features_maps": features_map_names,
            "darwin": True
        }
        mongodb.insert('TB','datasets_maps',doc)
        mongodb.close()