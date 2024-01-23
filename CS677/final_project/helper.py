"""
Jiankun Dong
Class: CS 677
Date: 12/12/2023
Helper funciton for Airline Passenger Satisfaction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,MinMaxScaler
"""
This function takes a filepath
and outputs a dataframe without rows that contains NaN
"""
def constructDF(filepath):
    df = pd.read_csv(filepath)
    #check for null or NaN values
    nullMatrix = df.isnull().values
    if nullMatrix.any():
        print("In total there are {0} null values".format(sum(sum(nullMatrix))))
        print("Dropping corresponding rows")
        df = df.dropna()
    else:
        print("Dataset is free of null values")
    print("Demensions of Data frame is",df.shape)
    # because there are valriables that are not 
    return df

def mergeDFSplitTraintest(trainDF, testDF, split = 0.5, random_state=None,scale = False):
    df = pd.concat([trainDF,testDF])
    df = df.drop(columns=["id","Unnamed: 0"])
    
    ## neutral or dissatisfied is neg and satisfied is pos
    df = df.replace('satisfied',1)
    df = df.replace('neutral or dissatisfied',0)
    Y = df['satisfaction'].values
    df = df.drop(columns=['satisfaction'])
    featureList = df.columns
    continuousFeature = ['Age','Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes']
    # if the model need scaling
    # using min max scaler because data is not normal distributed
    if scale:
        scaler = MinMaxScaler()
        df[continuousFeature]= scaler.fit_transform(df[continuousFeature])
    # deal with catagorical data
    df = pd.get_dummies(df)
    
    featureList = df.columns
    X = df[featureList].values

    xtrain, xtest, ytrain, ytest = train_test_split(X,Y,train_size = split,random_state=random_state)
    return (xtrain, xtest, ytrain, ytest)