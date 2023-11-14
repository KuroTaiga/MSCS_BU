"""
Jiankun Dong
Class: CS 677
Date: 11/13/2023
Description of Problem (just a 1-2 line summary!):
ensemble learning
"""
import helper
import pandas as pd

if __name__ == "__main__":
    #read the csv generated from Q1:
    D_df = pd.read_csv("D_Q1.csv")
    SPY_df = pd.read_csv("SPY_Q1.csv")
    D_df_Train = D_df.loc[D_df["Date"]<"2019"]
    D_df_Test = D_df.loc[D_df["Date"]>="2019"].reset_index()
    SPY_df_Train = SPY_df.loc[SPY_df["Date"]<"2019"]
    SPY_df_Test = SPY_df.loc[SPY_df["Date"]>="2019"].reset_index()
    D_TrueResult = D_df_Test["True_Label"].tolist()
    SPY_TrueResult = SPY_df_Test["True_Label"].tolist()
    D_predict = []
    SPY_predict = []
    for w in range(2,5):
        currD_predict = helper.predictDays(w,D_df_Train,D_df_Test,False)
        D_predict.append(currD_predict)
    for w in range(2,5):
        currSPY_predict = helper.predictDays(w,SPY_df_Train,SPY_df_Test,True)
        SPY_predict.append(currSPY_predict)
    D_ensembled = helper.ensemble(D_predict[0],D_predict[1],D_predict[2])
    SPY_ensembled = helper.ensemble(SPY_predict[0],SPY_predict[1],SPY_predict[2])

    D_ensembled_TNeg = sum(helper.getTrueNeg(D_TrueResult,D_ensembled))
    D_ensembled_TPos = sum(helper.getTruePos(D_TrueResult,D_ensembled))
    D_ensembled_FNeg = sum(helper.getFalseNeg(D_TrueResult,D_ensembled))
    D_ensembled_FPos = sum(helper.getFalsePos(D_TrueResult,D_ensembled))
    SPY_ensembled_TNeg = sum(helper.getTrueNeg(SPY_TrueResult,SPY_ensembled))
    SPY_ensembled_TPos = sum(helper.getTruePos(SPY_TrueResult,SPY_ensembled))
    SPY_ensembled_FNeg = sum(helper.getFalseNeg(SPY_TrueResult,SPY_ensembled))
    SPY_ensembled_FPos = sum(helper.getFalsePos(SPY_TrueResult,SPY_ensembled))
    D_otherTN = []
    D_otherTP = []
    D_otherFN = []
    D_otherFP = []
    SPY_otherTN = []
    SPY_otherTP = []
    SPY_otherFN = []
    SPY_otherFP= []
    wls=[2,3,4]
    for i in range(0,3):
        print("when w is :",wls[i])
        currTN = sum(helper.getTrueNeg(D_TrueResult,D_predict[i]))
        currTP = sum(helper.getTruePos(D_TrueResult,D_predict[i]))
        currFN = sum(helper.getFalseNeg(D_TrueResult,D_predict[i]))
        currFP = sum(helper.getFalsePos(D_TrueResult,D_predict[i]))
        D_otherTN.append(currTN)
        D_otherTP.append(currTP)
        D_otherFN.append(currFN)
        D_otherFP.append(currFP)
        print("For D")
        print("True neg: ", currTN)
        print("True Pos: ", currTP)
        print("False neg: ", currFN)
        print("False Pos: ", currFP)
        print("TPR: ", currTP/(currTP+currFN))
        print("TNR: ",currTN/(currTN+currFP))
        print("Accuracy: ",  100*sum(helper.compareResult(D_TrueResult,D_predict[i]))/len(D_TrueResult))
        currTN = sum(helper.getTrueNeg(SPY_TrueResult,SPY_predict[i]))
        currTP = sum(helper.getTruePos(SPY_TrueResult,SPY_predict[i]))
        currFN = sum(helper.getFalseNeg(SPY_TrueResult,SPY_predict[i]))
        currFP = sum(helper.getFalsePos(SPY_TrueResult,SPY_predict[i]))
        SPY_otherTN.append(currTN)
        SPY_otherTP.append(currTP)
        SPY_otherFN.append(currFN)
        SPY_otherFP.append(currFP)
        print("For SPY")
        print("True neg: ", currTN)
        print("True Pos: ", currTP)
        print("False neg: ", currFN)
        print("False Pos: ", currFP)
        print("TPR: ", currTP/(currTP+currFN))
        print("TNR: ",currTN/(currTN+currFP))
        print("Accuracy: ",  100*sum(helper.compareResult(SPY_TrueResult,SPY_predict[i]))/len(SPY_TrueResult))
    #ensembly
    print("For D")
    currTN = sum(helper.getTrueNeg(D_TrueResult,D_ensembled))
    currTP = sum(helper.getTruePos(D_TrueResult,D_ensembled))
    currFN = sum(helper.getFalseNeg(D_TrueResult,D_ensembled))
    currFP = sum(helper.getFalsePos(D_TrueResult,D_ensembled))
    print("True neg: ", currTN)
    print("True Pos: ", currTP)
    print("False neg: ", currFN)
    print("False Pos: ", currFP)
    print("TPR: ", currTP/(currTP+currFN))
    print("TNR: ",currTN/(currTN+currFP))
    currTN = sum(helper.getTrueNeg(SPY_TrueResult,SPY_ensembled))
    currTP = sum(helper.getTruePos(SPY_TrueResult,SPY_ensembled))
    currFN = sum(helper.getFalseNeg(SPY_TrueResult,SPY_ensembled))
    currFP = sum(helper.getFalsePos(SPY_TrueResult,SPY_ensembled))
    print("For SPY")
    print("True neg: ", currTN)
    print("True Pos: ", currTP)
    print("False neg: ", currFN)
    print("False Pos: ", currFP)
    print("TPR: ", currTP/(currTP+currFN))
    print("TNR: ",currTN/(currTN+currFP))