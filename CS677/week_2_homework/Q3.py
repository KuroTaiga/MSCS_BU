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
        print("When w is: ",w)
        print("Predicted for D :",currD_predict)
    for w in range(2,5):
        currSPY_predict = helper.predictDays(w,SPY_df_Train,SPY_df_Test,True)
        SPY_predict.append(currSPY_predict)
        print("When w is: ",w)
        print("Predicted for SPY :",currSPY_predict)
    D_ensembled = helper.ensemble(D_predict[0],D_predict[1],D_predict[2])
    SPY_ensembled = helper.ensemble(SPY_predict[0],SPY_predict[1],SPY_predict[2])
    #Q3.1 and 2
    print("Ensembled for D: ",D_ensembled)
    print("Ensembled for SPY: ",SPY_ensembled)
    print("Accuracy (%) for ensembled (D) :", 100*sum(helper.compareResult(D_TrueResult,D_ensembled))/len(D_TrueResult))
    
    print("Accuracy (%) for ensembled (SPY) :", 100*sum(helper.compareResult(SPY_TrueResult,SPY_ensembled))/len(SPY_TrueResult))

    #Q3.3
    Dneg_act_ensembled = sum(helper.getTrueNeg(D_TrueResult,D_ensembled))/(sum(helper.getTrueNeg(D_TrueResult,D_ensembled))+sum(helper.getFalseNeg(D_TrueResult,D_ensembled)))
    SPYneg_act_ensembled = sum(helper.getTrueNeg(SPY_TrueResult,SPY_ensembled))/(sum(helper.getTrueNeg(SPY_TrueResult,SPY_ensembled))+sum(helper.getFalseNeg(SPY_TrueResult,SPY_ensembled)))
    wls = [2,3,4]
    #for '-'
    print("For D:")
    print("Ensembled accuracy for '-': ",Dneg_act_ensembled)
    for i in range(0,3):
        print("w: ",wls[i])
        print("Accuracy predicting '-': ", sum(helper.getTrueNeg(D_TrueResult,D_predict[i]))/(sum(helper.getTrueNeg(D_TrueResult,D_predict[i]))+sum(helper.getFalseNeg(D_TrueResult,D_predict[i]))))
    print("For SPY:")
    print("Ensembled accuracy for '-': ",SPYneg_act_ensembled)
    for i in range(0,3):
        print("w: ",wls[i])
        if sum(helper.getTrueNeg(SPY_TrueResult,SPY_predict[i])) != 0 :
            print("Accuracy predicting '-': ", sum(helper.getTrueNeg(SPY_TrueResult,SPY_predict[i]))/(sum(helper.getTrueNeg(SPY_TrueResult,SPY_predict[i]))+sum(helper.getFalseNeg(SPY_TrueResult,SPY_predict[i]))))
        else:
            print("No negative predicated, acturacy = 0%")
    #Q3.4
    Dpos_act_ensembled = sum(helper.getTruePos(D_TrueResult,D_ensembled))/(sum(helper.getTruePos(D_TrueResult,D_ensembled))+sum(helper.getFalsePos(D_TrueResult,D_ensembled)))
    SPYpos_act_ensembled = sum(helper.getTruePos(SPY_TrueResult,SPY_ensembled))/(sum(helper.getTruePos(SPY_TrueResult,SPY_ensembled))+sum(helper.getFalsePos(SPY_TrueResult,SPY_ensembled)))
    wls = [2,3,4]
    #for '+'
    print("For D:")
    print("Ensembled accuracy for '+': ",Dpos_act_ensembled)
    for i in range(0,3):
        print("w: ",wls[i])
        print("Accuracy predicting '+': ", sum(helper.getTruePos(D_TrueResult,D_predict[i]))/(sum(helper.getTruePos(D_TrueResult,D_predict[i]))+sum(helper.getFalsePos(D_TrueResult,D_predict[i]))))
    print("For SPY:")
    print("Ensembled accuracy for '+': ",Dpos_act_ensembled)
    for i in range(0,3):
        print("w: ",wls[i])
        print("Accuracy predicting '+': ", sum(helper.getTruePos(SPY_TrueResult,SPY_predict[i]))/(sum(helper.getTruePos(SPY_TrueResult,SPY_predict[i]))+sum(helper.getFalsePos(SPY_TrueResult,SPY_predict[i]))))

with open('D_ensemble','w') as f:
    f.writelines(D_ensembled)



