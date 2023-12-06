
"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Q2 Naive Bayesian
"""
import pandas as pd
import helper
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# check helper for implementation
ASTV, MLTV, MAX, MEDIAN, NSP = helper.dataFormat()

data = pd.DataFrame(
    {"ASTV": ASTV,
     "MLTV": MLTV,
     "MAX":MAX,
     "MEDIAN":MEDIAN,
     "NSP":NSP},
    columns= ["ASTV","MLTV","MAX","MEDIAN","NSP"]
)
featureList = ["ASTV","MLTV","MAX","MEDIAN"]
X = data[featureList].values
Y = data["NSP"].values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,train_size=.5,random_state=0)

NB_classifier = GaussianNB().fit(X_train,Y_train)
prediction = NB_classifier.predict(X_test)
accuracy = 1-np.mean(prediction!=Y_test)
print("Accuracy is: ",accuracy)
tn, fp, fn, tp = confusion_matrix(Y_test,prediction).ravel()
print("tn: {0}, tp: {1}, fn: {2}, fp: {3}".format(tn,tp,fn,fp))