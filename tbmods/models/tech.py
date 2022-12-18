from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from tbmods.dataset.tech import DatasetTech
from sklearn.feature_selection import chi2
from sklearn.metrics import f1_score
import pandas as pd

class ModelTech:
    
    def __init__(self,period,start,end,features_list):
        self.scaler = MinMaxScaler()
        self.features_list = features_list
        self.dataset = DatasetTech(period,start,end,self.features_list)
        self.X = self.scaler.fit_transform(self.dataset.features)
        self.y = self.labels

    def chi2_test(self):
        return pd.DataFrame([chi2(self.X,self.y)[0]],columns=self.features_list)

    def fit(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2)
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def cv(self):
        return cross_val_score(self.model,self.X,self.y,cv=5)

    def f1_score(self):
        return f1_score(self.y_test,self.y_pred,average=None)
    
    def confusion_matrix(self):
        return confusion_matrix(self.y_test,self.y_pred)
        
    def feature_importances(self):
        return pd.Series(self.model.feature_importances_,index=self.features_list)