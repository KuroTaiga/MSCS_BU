"""
Jiankun Dong
Class: CS 677
Date: 11/13/2023
Commenly used function for HW2
"""
import os
import pandas as pd


def getTrueLabel(dataframe):
    returnVal = dataframe["Return"]
    if returnVal>=0:
        return '+'
    else:
        return'-'

def constructDF(filePath):
    # commpn function used to get the data into df w/ the true value column
    # convert the default str type to float for Return
    result = pd.read_csv(filePath)
    result["True_Label"] = result.apply(getTrueLabel,axis =1)
    return result

def countDays(k, df, pattern):
    #function for finding number of patten matches
    # this is kinda slow, but it's the ez implementation
    # k is the k value from the question(1-3), we are checking for the pattern len = k+1
    matchCount = 0
    trueLabel = df["True_Label"] == "+"
    totalCount = len(trueLabel)-k
    for i in range(0,totalCount):
        currLS = trueLabel[i:i+k+1]
        currLS = currLS.reset_index()
        curr = 0
        for j in range(0,k+1):
            curr += currLS["True_Label"][j]*(2**(j))
            
        if curr == pattern:
            matchCount+=1
            #print("match! pattern val and curr val: ", pattern, curr)
    return matchCount

def calPattern(ls):
    pattern = 0
    # map the pattern to a unique value
    # eg --+ = 2*0+2^2*0+2^3 = 8
    for i in range(0,len(ls)):
        pattern += (ls[i]=="+")*(2**(i))
    #print("pattern: ",pattern)
    return pattern

def predictDays(w,df_train, df_test,spy_flag):
    #we know all possible value of the pattern given w, max is 2^(w_max+1)-1 = 31
    # shorted patterns doesn't care about having longer pattern in the dict
    # from Q1, only for dataset SPY, when w=3, the predicted is "-" (default value),
    # all other default value are always "+"
    patls = list(range(32))
    predictLS = []
    patDic = {}
    #find count of all possible patterns and build disctionary
    for pat in patls:
        curr = countDays(w,df_train,pat)
        patDic[pat] = curr
    #calculate pattern for each day
    for i in range(0,df_test.shape[0]):
        currls = []
        if i<w:
        #the pattern is at least partially in the training set
            currls+=df_train.iloc[df_train.shape[0]-(w-i):]["True_Label"].tolist()
            currls+=df_test.iloc[0:i]["True_Label"].tolist()
        else:
            currls+=df_test.iloc[i-w:i]["True_Label"].tolist()
        currpat = calPattern(currls)
        #print(currls,currpat)
        NPospat = calPattern(currls+["+"])
        NNegCount = patDic[currpat]
        NPosCount = patDic[NPospat]
        #print(NNegCount,NPosCount)
        if NNegCount>NPosCount:
            predictLS.append("-")
        elif NNegCount<NPosCount:
            predictLS.append("+")
        else:
            if spy_flag and (NPospat==31):
                predictLS.append("-") #the only case from Q1 that defaults to "-"
            else:
                predictLS.append("+")
    return predictLS

def ensemble(ls1,ls2,ls3):
    #takes 3 predictedLists and calculate the emsembled list output
    result = []
    for i in range(0,len(ls1)):
        curr = (ls1[i]=="+")+(ls2[i]=="+")+(ls3[i]=="+")
        if curr >=2:
            result.append("+")
        else:
            result.append("-")
    return result

def compareResult(l1,l2):
    l3 = []
    for i in range(0,len(l1)):
        if l1[i]==l2[i]:
            l3.append(True)
        else:
            l3.append(False)
    return l3
#ls1 is the true value
def getTruePos(ls1,ls2):
    result = []
    for i in range(0,len(ls1)):
        if ls1[i] == "+" and ls2[i] == "+":
            result.append(True)
        else:
            result.append(False)
    return result
def getTrueNeg(ls1,ls2):
    result = []
    for i in range(0,len(ls1)):
        if ls1[i] == "-" and ls2[i] == "-":
            result.append(True)
        else:
            result.append(False)
    return result
def getFalsePos(ls1,ls2):
    result = []
    for i in range(0,len(ls1)):
        if ls1[i] == "-" and ls2[i] == "+":
            result.append(True)
        else:
            result.append(False)
    return result
def getFalseNeg(ls1,ls2):
    result = []
    for i in range(0,len(ls1)):
        if ls1[i] == "+" and ls2[i] == "-":
            result.append(True)
        else:
            result.append(False)
    return result