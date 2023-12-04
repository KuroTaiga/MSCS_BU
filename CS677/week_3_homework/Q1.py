"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Answers for Q1
"""
import helper
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
def statCal(DataSet):
    colName = ["f1","f2","f3","f4"]
    meanLs = []
    sdLS = []
    for i in range(0,4):
        currColumn = DataSet.loc[:,colName[i]]
        meanLs.append(np.round(np.mean(currColumn),2))
        sdLS.append(np.round(np.std(currColumn),2))
    print("Mean values: ",meanLs)
    print("Standard diviations: ",sdLS)
    return meanLs,sdLS

if __name__ == "__main__":
    DataSet = helper.constructDF("data_banknote_authentication.txt")
    
    
    print("For green (class 0): ")
    
    meanLsG, sdLSG = statCal(DataSet[DataSet['color']=="green"])

    print("For red (class 1): ")
    meanLsR, sdLSR = statCal(DataSet[DataSet['color']=="red"])
    print("For overall: ")
    meanLs, sdLS = statCal(DataSet)
    


