from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import pandas as pd

class Classifier:
    
    def __init__(self,model,X,y,features):
        self.X = X
        self.y = y
        self.features = features
        self.scaler = MinMaxScaler()
        self.s_X = self.scaler.fit_transform(X)
        self.model = model
        
    def fit(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.s_X, self.y, test_size=0.2)
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def cv(self):
        return cross_val_score(self.model,self.s_X,self.y,cv=5)

    def f1_score(self):
        return f1_score(self.y_test,self.y_pred,average=None)
    
    def confusion_matrix(self):
        return confusion_matrix(self.y_test,self.y_pred)
        
    def feature_importances(self):
        return pd.Series(self.model.feature_importances_,index=self.features)

"""
Todo : 
* graph PCA : https://www.icloud.com/notes/0feDxNcxa1ZDwdwiLC-LyZelw
"""