"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Commenly used function for hw 6
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

def constructDF(filePath):
    # R = 0: class L = 1 neg class L = 2 pos
    result = pd.read_csv(filePath,sep = '\t')
    result.columns =  ["f1","f2","f3","f4","f5","f6","f7","L"]
    # drop class L = 3
    result = result[result.L != 3]
    for i in range(0,len(result.L)):
        # L = 1 neg L = 2 pos
        if result.L[i] == 1:
            result.L[i] = 0
        else:
            result.L[i] = 1
    featurelist = ["f1","f2","f3","f4","f5","f6","f7"]
    X = result[featurelist].values
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform (X)
    Y = result["L"].values
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,train_size=.5,random_state=0)
    return (X_train, X_test, Y_train, Y_test)

def get_confusion(Y_test,prediction):
    tn, fp, fn, tp = confusion_matrix(Y_test,prediction).ravel()
    print("tp: {0}, fp: {1}, tn: {2}, fn: {3}".format(tp, fp, tn, fn))
    return (tp, fp, tn, fn)