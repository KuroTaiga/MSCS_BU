"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Answers for Q4 dropping features for knn
"""
import helper
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
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
    best_k = 5
    for i in range(0,4):
        curr_X_train = np.delete(X_train,i,axis=1)
        curr_X_test = np.delete(X_test,i,axis=1)
        knn_classifier = KNeighborsClassifier(n_neighbors=best_k)
        knn_classifier.fit(curr_X_train,Y_train.ravel()) #just flattens the Y to get rid of warrings
        pred_k = knn_classifier.predict(curr_X_test)
        #tp,tn,fp,fn,tpr,tnr = helper.getResultTable(np.array(Y_test),np.array(pred_k))
        accuracy=accuracy_score(Y_test,pred_k)
        print("For dropping f",i+1,"Accuracy is: " ,accuracy)
    