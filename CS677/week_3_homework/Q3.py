"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Answers for Q3 knn
"""
import helper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

if __name__ == "__main__":
    DataSet = helper.constructDF("./data_banknote_authentication.txt")
    featureList = ["f1","f2","f3","f4"]
    resultList = ['class']
    X = DataSet[featureList].values
    Y = DataSet[resultList].values
    scaler = StandardScaler()
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,train_size=.5,random_state=0)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    acc = []
    kLs = [3,5,7,9,11]
    for k in kLs:
        knn_classifier = KNeighborsClassifier(n_neighbors=k)
        knn_classifier.fit(X_train,Y_train.ravel())#just flattens the Y to get rid of warrings
        pred_k = knn_classifier.predict(X_test)
        tp,tn,fp,fn,tpr,tnr = helper.getResultTable(np.array(Y_test[:,0]),np.array(pred_k))
        print("For k",k,":")
        print("TP is:",tp)
        print("TN is:",tn)
        print("FP is:",fp)
        print("FN is:",fn)
        print("TPR is:",tpr)
        print("TNR is:",tnr)
        accuracy = accuracy_score(Y_test,pred_k)
        acc.append(accuracy)
        print("Accuracy is:",accuracy)
    plt.xticks(kLs)
    plt.plot(kLs,acc)
    
    plt.title("Accuracy vs K value")
    plt.xlabel("K")
    plt.ylabel("Accuracy")
    plt.show()
    BUID = scaler.transform([[8,9,1,6]])
    BUID_df = {'f1':8,'f2':9,'f3':1,'f4':6}
    #k=5 and 7 yield the same results
    best_k = 5
    knn_classifier = KNeighborsClassifier(n_neighbors=best_k)
    knn_classifier.fit(np.array(X_train),np.array(Y_train).ravel())#just flattens the Y to get rid of warrings
    IDPredic = knn_classifier.predict(BUID)[0]
    IDPredicColor = 'green'
    if IDPredic == 1:
        IDPredicColor = 'red'
    #for simple predict
    SimpleIDPredic = helper.SimpleClassifier(BUID_df)
    print("Result from simple predict: ", SimpleIDPredic)
    print("Result from knn when k=5: ",IDPredicColor)