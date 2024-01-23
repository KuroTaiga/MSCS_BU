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
import warnings
warnings.filterwarnings("ignore")

X_train, X_test, Y_train, Y_test = helper.constructDF("seeds_dataset.csv")
# Naive Bayesian
NB_classifier = GaussianNB().fit(X_train,Y_train)
prediction = NB_classifier.predict(X_test)
NB_accuracy = NB_classifier.score(X_test,Y_test)
print("Accuracy of Naive Bayesian is {0}".format(NB_accuracy))
print("Confusion matrix for Naive Bayesian")
tp, fp, tn, fn = helper.get_confusion(Y_test,prediction)