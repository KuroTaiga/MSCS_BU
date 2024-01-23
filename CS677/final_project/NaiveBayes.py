"""
Jiankun Dong
Class: CS 677
Date: 12/12/2023
Using Naive Bayesian classifier
Predict customer satisfaction (satisfied as pos, else as neg)
"""
import helper
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay


trainfilepath = "train.csv"
testfilepath  = "test.csv"

print("Processing training and test data")
trainDF = helper.constructDF(trainfilepath)
testDF = helper.constructDF(testfilepath)

print("Provided data has train test split is {0}:1".format(round(trainDF.shape[0]/testDF.shape[0],2)))
print("However, we want to use randomized training set")

Xtrain,Xtest,Ytrain,Ytest = helper.mergeDFSplitTraintest(trainDF,testDF,split=0.8)
NB_classifier = GaussianNB().fit(Xtrain,Ytrain)
prediction  = NB_classifier.predict(Xtest)
accuracy = 1-np.mean(prediction!=Ytest)
print("NeiveBayes has accuracy of {0}%".format(round(accuracy*100,4)))
cm=confusion_matrix(Ytest,prediction)
disp=ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
print("TPR :{0}, TNR: {1}".format(cm[1,1]/(cm[1,1]+cm[1,0]),cm[0,0]/(cm[0,0]+cm[0,1])))
