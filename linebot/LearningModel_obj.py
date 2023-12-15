#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import f1_score

class Model():
    def __init__(self, X_train, Y_train):
        self.knn = None
        self.svm_rbf = None
        self.dt = None
        self.rf = None
        self.mlp = None
        self.stack_model = None
        self.X_train = X_train
        self.Y_train = Y_train
    
    def BaseLearner(self):
        
        """initializa all base learners"""
        
        X_train = self.X_train
        Y_train = self.Y_train
        
        #init KNN classifier
        self.knn = KNeighborsClassifier(5) # Define classifier
        self.knn.fit(X_train, Y_train) # Train model
        
        #init SVM classifier
        self.svm_rbf = SVC()
        self.svm_rbf.fit(X_train, Y_train)
        
        #init dicision tree classifier
        self.dt = DecisionTreeClassifier(max_depth=1) # Define classifier
        self.dt.fit(X_train, Y_train) # Train model
        
        #init random forest classifier
        self.rf = RandomForestClassifier(n_estimators=3) # Define classifier
        self.rf.fit(X_train, Y_train) # Train model
        
        #init NN classifier
        self.mlp = MLPClassifier(alpha=0.01, max_iter=10000)
        self.mlp.fit(X_train, Y_train)
        
    def StackModel(self):
        
        """merge all base learners into single stackmodel"""
        
        estimator_list = [
            ('knn', self.knn),
            ('svm_rbf', self.svm_rbf),
            ('dt', self.dt),
            ('rf', self.rf),
            ('mlp', self.mlp) ]

        # Build stack model
        self.stack_model = StackingClassifier(
            estimators = estimator_list, 
            final_estimator = LogisticRegression()
        )

        # Train stacked model
        self.stack_model.fit(self.X_train, self.Y_train)
    
def predict(x, y_true, model):
    
    """make prediction and calculate accuracy"""
    
    # make prediction
    y_pred = model.predict(x)
    
    # calculate accuracy
    accuracy = accuracy_score(y_true, y_pred) # Calculate Accuracy
    mcc = matthews_corrcoef(y_true, y_pred) # Calculate MCC
    f1 = f1_score(y_true, y_pred, average='weighted') # Calculate F1-score
    
    print('- Accuracy: %s' % accuracy)
    print('- MCC: %s' % mcc)
    print('- F1 score: %s' % f1)
    
    
if __name__ == "__main__":
    
    MCI_AD = "MCI_patient.csv"

    training_df = pd.read_csv(MCI_AD)

    X = training_df.drop(['name', 'AD_diagnose'] , axis=1)
    y = training_df['AD_diagnose']

    X_train, X_val, y_train, y_val = train_test_split(X, y, train_size = 0.8, random_state=34)
    print(X_train.shape)
    print(X_val.shape)

    model = Model(X_train, y_train)
    model.BaseLearner()
    model.StackModel()
    
    #make prediction(training set)
    print("--------for training data set--------")
    
    print('Model performance for KNN classifier:')
    predict(X_train, y_train, model.knn)
    
    print('Model performance for SVM classifier:')
    predict(X_train, y_train, model.svm_rbf)
    
    print('Model performance for Decision tree classifier:')
    predict(X_train, y_train, model.dt)
    
    print('Model performance for random forest classifier:')
    predict(X_train, y_train, model.rf)
    
    print('Model performance for neural network classifier:')
    predict(X_train, y_train, model.mlp)
    
    print('Model performance for stack model classifier:')
    predict(X_train, y_train, model.stack_model)
    
    #make prediction(validation set)
    print("--------for validation set--------")
    
    print('Model performance for KNN classifier:')
    predict(X_val, y_val, model.knn)
    
    print('Model performance for SVM classifier:')
    predict(X_val, y_val, model.svm_rbf)
    
    print('Model performance for Decision tree classifier:')
    predict(X_val, y_val, model.dt)
    
    print('Model performance for random forest classifier:')
    predict(X_val, y_val, model.rf)
    
    print('Model performance for neural network classifier:')
    predict(X_val, y_val, model.mlp)
    
    print('Model performance for stack model classifier:')
    predict(X_val, y_val, model.stack_model)
    


# In[ ]:




