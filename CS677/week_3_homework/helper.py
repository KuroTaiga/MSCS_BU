
"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Commenly used function for HW3
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
def getColorLabel(df):
    if df["class"]:
        return "red"
    return "green"

def constructDF(filePath):
    # commpn function used to get the data into df w/ the true value column
    # convert the default str type to float for Return
    result = pd.read_csv(filePath)
    result.columns =  ["f1","f2","f3","f4","class"]
    result["color"] = result.apply(getColorLabel,axis = 1) 
    #result["True_Label"] = result.apply(getTrueLabel,axis =1)
    return result

def SimpleClassifier(df):
    #return false ("good") if coondition met, simple comparison method 
    #this is based on the pairplot
    if (df['f1']>0 and df['f2']>5 and df['f3'] >0):
        return "green"
    else:
        return "red"

#ls1 is the true value, this is for df format input
def getTruePos(ls1,ls2):
    result = []
    for i in ls1.index:
        if ls1[i] == "green" and ls2[i] == "green":
            result.append(True)
        else:
            result.append(False)
    return result
def getTrueNeg(ls1,ls2):
    result = []
    for i in ls1.index:
        if ls1[i] == "red" and ls2[i] == "red":
            result.append(True)
        else:
            result.append(False)
    return result
def getFalsePos(ls1,ls2):
    result = []
    for i in ls1.index:
        if ls1[i] == "red" and ls2[i] == "green":
            result.append(True)
        else:
            result.append(False)
    return result
def getFalseNeg(ls1,ls2):
    result = []
    for i in ls1.index:
        if ls1[i] == "green" and ls2[i] == "red":
            result.append(True)
        else:
            result.append(False)
    return result

def compareResult(ls1,ls2):
    result = []
    for i in ls1.index:
        if ls1[i] == ls2[i]:
            result.append(True)
        else:
            result.append(False)
    return result

# for np.arrray type input:
def getResultTable(truth_labels,y_prediction):
    # positive is green - class 0, therefore we need to flip the 0 and 1
    tp = np.sum(np.logical_and(y_prediction == 0, truth_labels == 0))
    tn = np.sum(np.logical_and(y_prediction == 1, truth_labels == 1))
    fp = np.sum(np.logical_and(y_prediction == 0, truth_labels == 1))
    fn = np.sum(np.logical_and(y_prediction == 1, truth_labels == 0))
    tpr = tp/(tp+fn)
    tnr = tn/(tn+fp)
    return (tp,tn,fp,fn,tpr,tnr)
def getAccuracy(ls):
    return sum(ls)/len(ls)