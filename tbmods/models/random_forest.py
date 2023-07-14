from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from tbmods.dataset import Dataset
from tbmods.mongodb import MongoDB
import joblib

class ModelRandomForest:
    
    def __init__(self,dataset_name,symbol,_map=None):
        self.symbol = symbol
        self.dataset_name = dataset_name
        self.dataset = Dataset(self.dataset_name,None,None,self.symbol,'historical')
        self.y = self.dataset.labels
        self.X = self.dataset.features.loc[self.y.index]
        self.model = RandomForestClassifier(verbose=True)
    
    def train(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y)
        self.model.fit(self.X_train,self.y_train)
        self.get_perfs()
        
    def save(self):
        joblib.dump(self.model,'/var/cache/models/random_forest_{}_{}'.format(self.dataset_name,self.symbol))
        
    def get_perfs(self):
        self.test_prediction = self.model.predict(self.X_test)
        self.perfs = {}
        self.perfs['score'] = self.model.score(self.X_test,self.y_test)
        self.perfs['confusion_matrix'] = confusion_matrix(self.y_test, self.test_prediction)
        self.perfs['accuracy'] = accuracy_score(self.y_test, self.test_prediction)
        self.perfs['f1_score'] = f1_score(self.y_test,self.test_prediction)