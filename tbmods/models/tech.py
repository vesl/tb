from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from tbmods.dataset.tech import DatasetTech
from sklearn.feature_selection import chi2
from sklearn.metrics import f1_score
from tbmods.mongodb import MongoDB
from datetime import datetime
import pandas as pd

class ModelTech:
    
    def __init__(self,period,start,end,features_list):
        self.mongodb = MongoDB()
        self.name = "tech-{}".format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.scaler = MinMaxScaler()
        self.features_list = features_list
        self.dataset = DatasetTech(period,start,end,self.features_list)
        self.meta = {"name": self.name, "features": self.features_list}
        self.X = self.scaler.fit_transform(self.dataset.features)
        self.y = self.dataset.labels
    
    def clf_init(self,config):
        self.clf = RandomForestClassifier(
            n_estimators=int(config['n_estimators']),
            oob_score=bool(config['oob_score']),
            n_jobs=int(config['n_jobs']),
            verbose=int(config['verbose']),
            class_weight=config['class_weight'],
            random_state=int(config['random_state']),
        )
        self.meta.update({"clf_config":config})

    def chi2_test(self):
        return pd.DataFrame([chi2(self.X,self.y)[0]],columns=self.features_list)

    def fit(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2)
        self.clf.fit(self.X_train, self.y_train)
        self.y_pred = self.clf.predict(self.X_test)
        self.meta.update({
            "score": {
                "cross_val_score": self.cross_val_score().tolist(),
                "f1_score": self.f1_score().tolist(),
                "confusion_matrix": self.confusion_matrix().tolist(),
                "feature_importances": self.feature_importances().to_json(),
            }
        })

    def cross_val_score(self):
        return cross_val_score(self.clf,self.X,self.y,cv=5)

    def f1_score(self):
        return f1_score(self.y_test,self.y_pred,average=None)
    
    def confusion_matrix(self):
        return confusion_matrix(self.y_test,self.y_pred)
        
    def feature_importances(self):
        return pd.Series(self.clf.feature_importances_,index=self.features_list)
        
    def save_meta(self):
        self.mongodb.insert('models','tech',self.meta)
        