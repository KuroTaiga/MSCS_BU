
"""
Jiankun Dong
Class: CS 677
Date: 11/27/2023
Q2, fit data with different models
"""

import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

import matplotlib.pyplot as plt
def TrainFitModel(x_train, y_train, x_test, y_test):
    for degree in range(1,4):
        print("Degree:",degree)
        weights = np.polyfit(x_train,y_train, degree)
        print("Weights:",weights)
        model = np.poly1d(weights)
        # for plotting 
        sorted_x_test = sorted(x_test)
        sorted_predict = model(sorted_x_test)
        predicted = model(x_test)
        sse = mean_squared_error(y_test, predicted)*len(y_test)
        print("sse",sse)
        #rmse = np.sqrt(mean_squared_error(y_test, predicted))
        #print("rmse",rmse)
        #r2 = r2_score(y_test, predicted)
        #print("r2:",r2)
        plt.scatter(x_test,y_test,color = 'blue',marker = "o", s = 10)
        plt.plot(sorted_x_test,sorted_predict,color='green',lw=1)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
    print("y=a*log(x)+b: ")
    weights = np.polyfit(np.log(x_train), y_train, 1)
    print("Weights:",weights)
    predicted = weights[0]*np.log(x_test)+weights[1]
    sse = mean_squared_error(y_test, predicted)*len(y_test)
    print("sse",sse)
    #rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse",rmse)
    #r2 = r2_score(y_test, predicted)
    #print("r2:",r2)
    sorted_x_test = sorted(x_test)
    sorted_predict = weights[0]*np.log(sorted_x_test)+weights[1]
    plt.scatter(x_test,y_test,color = 'blue',marker = "o", s = 10)
    plt.plot(sorted_x_test,sorted_predict,color='green',lw=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    print("log(y) = a*log(x)+b: ")
    weights = np.polyfit(np.log(x_train), np.log(y_train), 1)
    print("Weights:",weights)
    predicted = np.exp(weights[0]*np.log(x_test)+weights[1])
    sse = mean_squared_error(y_test, predicted)*len(y_test)
    print("sse",sse)
    #rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse",rmse)
    #r2 = r2_score(y_test, predicted)
    #print("r2:",r2)
    sorted_x_test = sorted(x_test)
    sorted_predict = np.exp(weights[0]*np.log(sorted_x_test)+weights[1])
    plt.scatter(x_test,y_test,color = 'blue',marker = "o", s = 10)
    plt.plot(sorted_x_test,sorted_predict,color='green',lw=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    return

def processDF(df):
    df_train = df.sample(frac=.5,random_state=0)
    CPK_train = df_train['creatinine_phosphokinase'].values
    pls_train = df_train['platelets'].values
    ss_train = df_train['serum_sodium'].values
    sc_train = df_train['serum_creatinine'].values

    df_test = df.drop(df_train.index)
    CPK_test = df_test['creatinine_phosphokinase'].values
    pls_test = df_test['platelets'].values
    ss_test = df_test['serum_sodium'].values
    sc_test = df_test['serum_creatinine'].values
    return (CPK_train,pls_train,ss_train,sc_train,CPK_test,pls_test,ss_test,sc_test)

if __name__ == "__main__":
    dataDF = pd.read_csv("heart_failure_clinical_records_dataset.csv")
    df_0 = dataDF[dataDF['DEATH_EVENT'] == 0]
    df_1 = dataDF[dataDF['DEATH_EVENT'] == 1]
    #create the train and test datasets
  
    print("For DeathEvent = 0 \n Group 1:")
    CPK_train,pls_train,ss_train,sc_train,CPK_test,pls_test,ss_test,sc_test = processDF(df_0)
    TrainFitModel(CPK_train,pls_train,CPK_test,pls_test)
    print(" Group 2:")
    TrainFitModel(pls_train,ss_train,pls_test,ss_test)
    print(" Group 3:")
    TrainFitModel(ss_train,sc_train,ss_test,sc_test)
    print(" Group 4:")    
    TrainFitModel(pls_train,sc_train,pls_test,sc_test)

    print("For DeathEvent = 1 \n Group 1:")
    CPK_train,pls_train,ss_train,sc_train,CPK_test,pls_test,ss_test,sc_test = processDF(df_1)
    TrainFitModel(CPK_train,pls_train,CPK_test,pls_test)
    print(" Group 2:")
    TrainFitModel(pls_train,ss_train,pls_test,ss_test)
    print(" Group 3:")
    TrainFitModel(ss_train,sc_train,ss_test,sc_test)
    print(" Group 4:")    
    TrainFitModel(pls_train,sc_train,pls_test,sc_test)

