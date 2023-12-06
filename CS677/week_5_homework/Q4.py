
"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Q4 Random Forest
"""
import pandas as pd
import helper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
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

predictionMatrix = []
all_error_rate = []
for d in range(1,6):
    predictionLS = []
    error_rate = []
    for n in range(1,11):
        NB_classifier = RandomForestClassifier(n_estimators =n, max_depth =d,criterion ='entropy',random_state=50).fit(X_train,Y_train)
        prediction = NB_classifier.predict(X_test)
        predictionLS.append(prediction)
        accuracy = 1-np.mean(prediction!=Y_test)
        error_rate.append(1-accuracy)
        all_error_rate.append(1-accuracy)
    predictionMatrix.append(predictionLS)
    #print(error_rate)
    #print("Accuracy is: ",accuracy)
    plt.plot(list(range(1,11)),error_rate, label = "D="+str(d))
plt.xlabel("N value")
plt.ylabel("Error rate")
plt.legend() 
plt.show()

print("The highest accuracy:", 1-min(all_error_rate))
## The best D and N combination is N=7, D=5 for randome_state = 50 
tn, fp, fn, tp = confusion_matrix(Y_test,predictionMatrix[4][7]).ravel()
print("tn: {0}, tp: {1}, fn: {2}, fp: {3}".format(tn,tp,fn,fp))
