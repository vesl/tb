from tbmods.models.random_forest import ModelRandomForest

class Id:
    
    def __init__(self,genom,dataset_type,model_type,symbol):
        self.genom = genom
        self.dataset_type = dataset_type
        self.model_type = model_type
        self.symbol = symbol

    def train(self):
        if self.model_type == 'random_forest': 
            self.model = ModelRandomForest(self.dataset_type,self.symbol,self.genom['model_map'])
            self.model.train()