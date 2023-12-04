"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Answers for Q2
"""
import helper
import seaborn as sb
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
if __name__ == "__main__":
    DataSet = helper.constructDF("data_banknote_authentication.txt")
    featureList = ["f1","f2","f3","f4"]
    resultList = ['class','color']
    X = DataSet[featureList].values
    Y = DataSet[resultList].values
    #Xtrain,Xtest,Ytrain,Ytest = train_test_split(X,Y,test_size=.5,random_state=0)
    train = DataSet.sample(frac=.5,random_state=0)
    Xtrain = train.loc[:,featureList]
    Ytrain = train.loc[:,resultList]
    test = DataSet.drop(train.index)
    Xtest = test.loc[:,featureList]
    Ytest = test.loc[:,resultList]
    sb.pairplot(train[train['color']=='green'],hue="color")
    plt.savefig("good_bills.pdf", format='pdf')
    sb.pairplot(train[train['color']=='red'],hue="color")
    plt.savefig("fake_bills.pdf", format='pdf')
    sb.pairplot(train,hue="color")#putting the 2 graphs together
    plt.savefig("both_goodandfake_bills.pdf", format='pdf')
    Ytest['prediction'] = Xtest.apply(helper.SimpleClassifier,axis=1)
    TP = sum(helper.getTruePos(Ytest['color'],Ytest['prediction']))
    TN = sum(helper.getTrueNeg(Ytest['color'],Ytest['prediction']))
    FP = sum(helper.getFalsePos(Ytest['color'],Ytest['prediction']))
    FN = sum(helper.getFalseNeg(Ytest['color'],Ytest['prediction']))
    TPR = TP/(TP+FN)
    TNR = TN/(TN+FP)
    Accuracy = helper.getAccuracy(helper.compareResult(Ytest['color'],Ytest['prediction']))
    print("TP: ",TP)
    print("TN: ",TN)
    print("FP: ",FP)
    print("FN: ",FN)
    print("TPR: ",TPR)
    print("TNR: ",TNR)
    print("Accuracy: ",Accuracy)
    
    
    

