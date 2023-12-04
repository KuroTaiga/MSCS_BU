
"""
Jiankun Dong
Class: CS 677
Date: 11/27/2023
Q1 show corralation 
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn


if __name__ == "__main__":
    dataDF = pd.read_csv("heart_failure_clinical_records_dataset.csv")
    df_0 = dataDF[dataDF['DEATH_EVENT'] == 0]
    df_1 = dataDF[dataDF['DEATH_EVENT'] == 1]
    M0 = df_0.corr()
    M1 = df_1.corr()
    fig, ax = plt.subplots(figsize=(10,10))
    sn.heatmap(M0,annot=True)
    plt.savefig("M0.pdf", format="pdf")
    plt.show()
    plt.clf()
    fig, ax = plt.subplots(figsize=(10,10))
    sn.heatmap(M1,annot=True)
    plt.savefig("M1.pdf", format="pdf")
    plt.show()

