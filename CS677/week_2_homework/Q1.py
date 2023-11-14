"""
Jiankun DOng
Class: CS 677
Date: 11/13/2023
Homework Problem #Q1
Description of Problem (just a 1-2 line summary!):
Question 1: adding the True label column to the df, compute probaerbilities for some scenarios
"""
import pandas as pd
import numpy as np
import helper


def pStar(df):
    #calculate the probability of "+" 
    result = sum(df["True_Label"]=="+")/df.shape[0]
    return result



if __name__ == "__main__":
    #Q1.1, adding the trule label column to the df
    D_df = helper.constructDF("./D.csv")
    D_df.to_csv("./D_Q1.csv",index=False)
    SPY_df = helper.constructDF("./SPY.csv")
    SPY_df.to_csv("./SPY_Q1.csv",index=False)
    print("Head of Data frame for D: ", D_df.head())
    print(" Head of Data frame for SPY: ",SPY_df.head())
    D_df_Train = D_df.loc[D_df["Date"]<"2019"]
    D_df_Test = D_df.loc[D_df["Date"]>="2019"]
    SPY_df_Train = SPY_df.loc[SPY_df["Date"]<"2019"]
    SPY_df_Test = SPY_df.loc[SPY_df["Date"]>="2019"]
    #Q1.2, calculate the possibility of + p* for D and SPY based on first 3 years:
    PStar_D = pStar(D_df_Train)
    print("P star for D is: ",PStar_D)
    PStar_SPY = pStar(SPY_df_Train)
    print("P star for SPY is: ",PStar_SPY)

    #Q1.3
    
    print("After seeing all down days: ")
    print("For stock D: ")
    for k in range(1,4):
        #eg, k=1, pattern -+ = 2
        allDown = helper.countDays(k,D_df_Train,0)
        pattern = 2**(k)
        seeUp = helper.countDays(k,D_df_Train,pattern)
        #print(allDown,seeUp,k)
        print("For k = : ",k)
        print("The probability of seeing a upday over a downday is: ", seeUp/(allDown+seeUp))
    print("For stock SPY: ")
    for k in range(1,4):
        allDown = helper.countDays(k,SPY_df_Train,0)
        pattern = 2**(k)
        seeUp = helper.countDays(k,SPY_df_Train,pattern)
        #print(allDown,seeUp,k)
        print("For k = : ",k)
        print("The probability of seeing a upday over a downday is: ", seeUp/(allDown+seeUp))
    #Q1.4
    print("After seeing all up days: ")
    print("For stock D: ")
    for k in range(1,4):
        seeDownPat = 0
        for i in range(0,k):
            seeDownPat += (2**i)
        allUpPat = seeDownPat+2**(k)
        allUp = helper.countDays(k,D_df_Train,allUpPat)
        seeDown = helper.countDays(k,D_df_Train,seeDownPat)
        #print(allDown,seeUp,k)
        print("For k = : ",k)
        print("The probability of seeing a upday over a downday is: ", allUp/(seeDown+allUp))
    print("For stock SPY: ")
    for k in range(1,4):
        seeDownPat = 0
        for i in range(0,k):
            seeDownPat += (2**i)
        allUpPat = seeDownPat+2**(k)
        
        allUp = helper.countDays(k,SPY_df_Train,allUpPat)
        seeDown = helper.countDays(k,SPY_df_Train,seeDownPat)
        #print(allDown,seeUp,k)
        print("For k = : ",k)
        print("The probability of seeing a upday over a downday is: ", allUp/(seeDown+allUp))