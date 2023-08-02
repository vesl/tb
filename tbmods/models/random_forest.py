from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from tbmods.dataset import Dataset
from tbmods.mongodb import MongoDB
from datetime import datetime
import joblib
import os

class ModelRandomForest:

    def __init__(self,dataset_name,symbol,_map):
        self.time_start = datetime.now()
        self.dataset_name = dataset_name
        self.symbol = symbol
        self._map = _map
        self.name = 'random_forest_{}_{}_{}'.format(self.dataset_name,self.symbol,self.time_start.strftime("%m%d%Y%H%M%S"))
        self.dataset = Dataset(self.dataset_name,None,None,self.symbol,'historical')
        self.y = self.dataset.labels
        self.X = self.dataset.features.loc[self.y.index]
        self.model = RandomForestClassifier(
            n_estimators=int(self._map['n_estimators']['value']),
            criterion=self._map['criterion']['value'],
            max_depth=None if self._map['max_depth']['value'] == 'None' else int(self._map['max_depth']['value']),
            min_samples_split=int(self._map['min_samples_split']['value']),
            min_samples_leaf=int(self._map['min_samples_leaf']['value']),
            min_weight_fraction_leaf=int(self._map['min_weight_fraction_leaf']['value']),
            max_features=None if self._map['max_features']['value'] == 'None' else self._map['max_features']['value'],
            max_leaf_nodes=None if self._map['max_leaf_nodes']['value'] == 'None' else int(self._map['max_leaf_nodes']['value']),
            min_impurity_decrease=float(self._map['min_impurity_decrease']['value']),
            bootstrap=self._map['bootstrap']['value'],
            oob_score=self._map['oob_score']['value'],
            warm_start=self._map['warm_start']['value'],
            class_weight=None if self._map['class_weight']['value'] == 'None' else self._map['class_weight']['value'],
            ccp_alpha=float(self._map['ccp_alpha']['value']),
            max_samples=None if self._map['max_samples']['value'] == 'None' else float(self._map['max_samples']['value']),
            random_state=9,
            verbose=True,
            n_jobs=-1
        )
    
    def train(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y)
        self.model.fit(self.X_train,self.y_train)
        self.get_perfs()

    def save(self):
        metadata = {
            "name": self.name,
            "date": self.time_start.strftime("%m/%d/%Y, %H:%M:%S"),
            "type": "random_forest",
            "dataset": self.dataset_name,
            "perfs": self.perfs,
            "parameters": self._map,
            "symbol": self.symbol
        }
        mongodb = MongoDB()
        mongodb.update("TB","models_metadatas",metadata,{"name":self.name},True)
        mongodb.close()
        joblib.dump(self.model,'/var/cache/models/{}'.format(self.name))
        
    def get_perfs(self):
        self.test_prediction = self.model.predict(self.X_test)
        self.perfs = {}
        self.perfs['score'] = self.model.score(self.X_test,self.y_test)
        self.perfs['confusion_matrix'] = confusion_matrix(self.y_test, self.test_prediction).tolist()
        self.perfs['accuracy'] = accuracy_score(self.y_test, self.test_prediction)
        self.perfs['f1_score'] = f1_score(self.y_test,self.test_prediction)
        self.perfs['training_time'] = str(datetime.now() - self.time_start)
        self.perfs['cross_val_score'] = cross_val_score(self.model,self.X,self.y).tolist()
        self.perfs['feature_importances'] = {
            "labels": [feature.split('!')[0] for feature in self.dataset.features.columns],
            "datasets": [{"data":self.model.feature_importances_.tolist()}]
        }