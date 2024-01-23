"""
Jiankun Dong
Class: CS 677
Date: 12/12/2023
Using Random Forest
Predict customer satisfaction (satisfied as pos, else as neg)
"""
import helper
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
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

predictionMatrix = []
all_error_rate = []
for d in range(1,6):
    predictionLS = []
    error_rate = []
    for n in range(1,11):
        NB_classifier = RandomForestClassifier(n_estimators =n, max_depth =d,criterion ='entropy',random_state=50).fit(Xtrain,Ytrain)
        prediction = NB_classifier.predict(Xtest)
        predictionLS.append(prediction)
        accuracy = 1-np.mean(prediction!=Ytest)
        error_rate.append(1-accuracy)
        all_error_rate.append(1-accuracy)
    predictionMatrix.append(predictionLS)
    plt.plot(list(range(1,11)),error_rate, label = "D="+str(d))
plt.xlabel("N value")
plt.ylabel("Error rate")
plt.legend() 
plt.show()

print("The highest accuracy for random forest is:", 1-min(all_error_rate))
## The best D and N combination is N=10, D=5 for randome_state = 50 
tn, fp, fn, tp = confusion_matrix(Ytest,predictionMatrix[4][9]).ravel()
print("tn: {0}, tp: {1}, fn: {2}, fp: {3}".format(tn,tp,fn,fp))

cm = np.array([[tn,fp],[fn,tp]])
disp=ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
print("TPR :{0}, TNR: {1}".format(cm[1,1]/(cm[1,1]+cm[1,0]),cm[0,0]/(cm[0,0]+cm[0,1])))
