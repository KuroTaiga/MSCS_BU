"""
Jiankun Dong
Class: CS 677
Date: 11/13/2023
Description of Problem (just a 1-2 line summary!):
Predicting labels
"""

import pandas as pd
import numpy as np
import helper

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

    #Q2.1 for W=2,3,4 computer perdict label for test set
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
    
    #Q2.2 Calculate accuracy
    print("For Stock D:")
    print("Accuracy (%) when w=2: ", 100*sum(helper.compareResult(D_TrueResult,D_predict[0]))/len(D_TrueResult))
    print("Accuracy (%) when w=3: ", 100*sum(helper.compareResult(D_TrueResult,D_predict[1]))/len(D_TrueResult))
    print("Accuracy (%) when w=4: ", 100*sum(helper.compareResult(D_TrueResult,D_predict[2]))/len(D_TrueResult))
    print("For Stock SPY:")
    print("Accuracy (%) when w=2: ", 100*sum(helper.compareResult(SPY_TrueResult,SPY_predict[0]))/len(SPY_TrueResult))
    print("Accuracy (%) when w=3: ", 100*sum(helper.compareResult(SPY_TrueResult,SPY_predict[1]))/len(SPY_TrueResult))
    print("Accuracy (%) when w=4: ", 100*sum(helper.compareResult(SPY_TrueResult,SPY_predict[2]))/len(SPY_TrueResult))

    #Q2.3
    # the best W* for D is:3
    # the best W* for SPY is: 2 or 3 they are the same
    with open('bestW', 'w') as f:
        f.writelines(D_predict[1])
    
    
    

    

