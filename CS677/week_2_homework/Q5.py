"""
Jiankun Dong
Class: CS 677
Date: 11/13/2023
Description of Problem (just a 1-2 line summary!):
ploting
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import helper 
if __name__ == "__main__":
    #read the csv generated from Q1:
    D_df = pd.read_csv("D_Q1.csv")
    D_df_Train = D_df.loc[D_df["Date"]<"2019"]
    D_df_Test = D_df.loc[D_df["Date"]>="2019"].reset_index()
    D_TrueResult = D_df_Test["True_Label"].tolist()

    with open('D_ensemble') as f:
        DEnsemble = f.read()
    DEnsemble = list(DEnsemble)
    #print(DEnsemble)
    
    with open('bestW') as f2:
        bestW = f2.read()
    bestW = list(bestW)
    #print(bestW)
    valueBestW = [100]
    valueEnsemble = [100]
    valueHold = [100]
    startVal = 100
    for i in range(0,D_df_Test.shape[0]):
        valueHold.append(valueHold[i]*(1+D_df_Test["Return"][i]))
        if DEnsemble[i] == "+":
            valueEnsemble.append(valueEnsemble[i]*(1+D_df_Test["Return"][i]))
        else:
            valueEnsemble.append(valueEnsemble[i])
        if bestW[i] == "+":
            valueBestW.append(valueBestW[i]*(1+D_df_Test["Return"][i]))
        else:
            valueBestW.append(valueBestW[i])
    plt.plot( valueHold, color = 'r')
    plt.plot(valueBestW,color = 'b')
    plt.plot(valueEnsemble,color = 'g')
    plt.show()
        
