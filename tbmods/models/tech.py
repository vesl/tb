from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import confusion_matrix
from tbmods.dataset.tech import DatasetTech
from sklearn.feature_selection import chi2
from sklearn.metrics import f1_score
from tbmods.mongodb import MongoDB
from tbmods.config import Config
from tbmods.cache import Cache
from datetime import datetime
import pandas as pd
import joblib

config = Config()

class ModelTech:

    def __init__(self,symbol,period,start,end,features_list):
        self.symbol = symbol
        self.period = period
        self.start = start
        self.end = end
        self.features_list = features_list
        self.name = "TECH-{}-{}".format(self.symbol,datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.init_meta()

    def init_meta(self):
        self.meta = {"name": self.name}

    def update_status(self,update):
        cache = Cache(config['app'])
        if type(update) is bool: self.status = {}
        else: self.status.update(update)
        cache.data["models/tech/status"] = self.status
        cache.write()

    def load_dataset(self):
        self.dataset = DatasetTech(self.symbol,self.period,self.start,self.end,self.features_list)
        self.meta.update({
            "symbol":self.symbol,
            "period":self.period,
            "start":self.start,
            "end":self.end
        })

    def scale(self):
        self.scaler = RobustScaler()
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

    def fit(self,save=False):
        self.scale()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2)
        if save: self.clf.fit(self.X,self.y)
        else: self.clf.fit(self.X_train, self.y_train)
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

    def chi2_test(self):
        self.scale()
        return pd.DataFrame([chi2(self.X,self.y)[0]],columns=self.features_list)

    def save_meta(self):
        mongodb = MongoDB()
        mongodb.insert('models','tech',self.meta)
        mongodb.close()

    def save_model(self):
        joblib.dump(self.clf,'/var/cache/models/{}'.format(self.name))