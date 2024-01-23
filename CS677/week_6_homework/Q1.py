"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Q1 SVM with linear, gaussian and polynomial kernel 
"""

import pandas as pd
import helper
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

X_train, X_test, Y_train, Y_test = helper.constructDF("seeds_dataset.csv")
# lienar kernal
svm_classifier = svm.SVC(kernel='linear')
svm_classifier.fit(X_train,Y_train)
predicted = svm_classifier.predict(X_test)
linear_accuracy = svm_classifier.score(X_test,Y_test)
print("Accuracy of linear kernel is {0}".format(linear_accuracy))
print("Confusion matrix for linear kernel")
tp, fp, tn, fn = helper.get_confusion(Y_test,predicted)

# gaussian kernal
svm_classifier = svm.SVC(kernel='rbf')
svm_classifier.fit(X_train,Y_train)
predicted = svm_classifier.predict(X_test)
gauss_accuracy = svm_classifier.score(X_test,Y_test)
print("Accuracy of gaussian kernel is {0}".format(gauss_accuracy))
print("Confusion matrix for gaussian kernel")
tp, fp, tn, fn = helper.get_confusion(Y_test,predicted)

# Polynomial kernal (degree = 3)
svm_classifier = svm.SVC(kernel='poly',degree=3)
svm_classifier.fit(X_train,Y_train)
predicted = svm_classifier.predict(X_test)
poly_accuracy = svm_classifier.score(X_test,Y_test)
print("Degree is 3")
print("Accuracy of polynomial kernel is {0}".format(poly_accuracy))
print("Confusion matrix for polynomial kernel")
tp, fp, tn, fn = helper.get_confusion(Y_test,predicted)