"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Answers for Q6, logistic with dropping features
"""
import helper
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
if __name__ == "__main__":
    DataSet = helper.constructDF("data_banknote_authentication.txt")
    featureList = ["f1","f2","f3","f4"]
    resultList = ['class']
    X = DataSet[featureList].values
    Y = DataSet[resultList].values
    scaler = StandardScaler()
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,train_size=.5,random_state=0)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    for i in range(0,4):
        curr_X_train = np.delete(X_train,i,axis=1)
        curr_X_test = np.delete(X_test,i,axis=1)
        log_reg_classifier = LogisticRegression()
        log_reg_classifier.fit(curr_X_train,Y_train.ravel())
        pred_log = log_reg_classifier.predict(curr_X_test)
        tp,tn,fp,fn,tpr,tnr = helper.getResultTable(np.array(Y_test[:,0]),np.array(pred_log))
        accuracy = accuracy_score(Y_test,pred_log)
        #print("TP: ",tp)
        #print("TN: ",tn)
        #print("FP: ",fp)
        #print("FN: ",fn)
        #print("TPR: ",tpr)
        #print("TNR: ",tnr)
        print("Accuracy for removing f",i+1,"is: ",accuracy)
    