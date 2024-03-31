from sklearn.datasets import load_iris,load_digits,load_wine
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier  # To approximate C4.5
from sklearn.utils import resample


from xgboost import XGBClassifier
from catboost import CatBoostClassifier, Pool
import lightgbm as lgb
import numpy as np
import time

#loading datasets
RANDOM_STATE = 0
TEST_SIZE = 0.3
iris = load_iris()
digits = load_digits()
wine = load_wine()
# 70-30 split of train and test
X_iris, y_iris = iris.data, iris.target
X_digits, y_digits = digits.data, digits.target
X_wine, y_wine = wine.data, wine.target
# Change to do train-test split later
#X_iris_train, X_iris_test, Y_iris_train, Y_iris_test = train_test_split(X_iris,y_iris,test_size=TEST_SIZE,random_state=RANDOM_STATE)
#X_digits_train, X_digits_test, Y_digits_train, Y_digits_test = train_test_split(X_digits,y_digits,test_size=TEST_SIZE,random_state=RANDOM_STATE)
#X_wine_train, X_wine_test, Y_wine_train, Y_wine_test = train_test_split(X_wine,y_wine,test_size=TEST_SIZE,random_state=RANDOM_STATE)
datasetNames = ["Iris","Digits","Wine"]
all_data = {"Iris":(X_iris,y_iris),"Digits":(X_digits,y_digits),"Wine":(X_wine,y_wine)}
#all_train = {"Iris":(X_iris_train,Y_iris_train),"Digits":(X_digits_train,Y_digits_train),"Wine":(X_wine_train,Y_wine_train)}
#all_test= {"Iris":(X_iris_test,Y_iris_test),"Digits":(X_digits_test,Y_digits_test),"Wine":(X_wine_test,Y_wine_test)}


# set weak learners to use
knn = KNeighborsClassifier()
svm = SVC()
naive_bayes = GaussianNB()
cart = DecisionTreeClassifier()  # CART
c45 = RandomForestClassifier(max_depth=5, n_estimators=1, max_features=1)  # Approximation of C4.5
models = [knn, svm, naive_bayes, cart, c45]
model_names = ['kNN', 'SVM', 'Naïve Bayes', 'CART', 'C4.5 (approx)']

xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
cat = CatBoostClassifier(verbose = 0)
#cat =  CatBoostClassifier(iterations=2,
                        #    depth=2,
                        #    learning_rate=1,
                        #    loss_function='Logloss',
                        #    verbose=True)
lgb_model = lgb.LGBMClassifier(verbose = -1)
booster_model = {'xgb':xgb,'cat':cat,'lgb':lgb_model}
booster_names = booster_model.keys()

def score_model(model, x, y):
    #10 fold validation
    scores = cross_val_score(model,x,y, cv=10)
    return np.mean(scores).round(4)
def aug_dataset(X,Y,n):
    # n is the number of times additional datas should be added
    X_new, Y_new = resample(X,Y,n_samples=int(X.shape[0]*(n-1)),replace=True, random_state=RANDOM_STATE)
    
    return np.vstack((X, X_new)), np.hstack((Y, Y_new))

iris_scores = {}
iris_acc = {}
digits_scores = {}
digits_acc = {}
wine_scores = {}
wine_acc = {}
all_scores = {"Iris":iris_scores,"Digits":digits_scores,"Wine":wine_scores}
all_acc = {"Iris":iris_acc,"Digits":digits_acc,"Wine":wine_acc}
for model, name in zip(models, model_names):
    for currDataset in datasetNames:
        (X,Y) = all_data[currDataset]
        if name =='kNN' or name=='SVM':
            # these 2 models need normailization
            transformer = Normalizer().fit(X)
            X = transformer.transform(X)
        # same random state ensures same train test split result
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=TEST_SIZE,random_state=RANDOM_STATE)
        model = model.fit(X_train,Y_train)
        score = score_model(model,X_train,Y_train)
        all_scores[currDataset][name] = score 
        all_acc[currDataset][name] = model.score(X_test,Y_test).round(4)
print("Cross-validation (10fold) scores:")
print("Iris:",iris_scores)
print("Digits: ",digits_scores)
print("Wine: ",wine_scores)
print("Model scores on testing set:")
print("Iris:",iris_acc)
print("Digits: ",digits_acc)
print("Wine: ",wine_acc)

# 3) do new datasets
# using iris and wine
X_iris2, y_iris2 =  aug_dataset(X_iris, y_iris, 2)
X_iris3, y_iris3 =  aug_dataset(X_iris, y_iris, 3)
X_iris4, y_iris4 =  aug_dataset(X_iris, y_iris, 4)
X_iris5, y_iris5 =  aug_dataset(X_iris, y_iris, 5)
iris_bundle = [(X_iris,y_iris),(X_iris2,y_iris2),(X_iris3,y_iris3),
               (X_iris4,y_iris4),(X_iris5,y_iris5)]
X_wine2, y_wine2 = aug_dataset(X_wine, y_wine, 2)
X_wine3, y_wine3 = aug_dataset(X_wine, y_wine, 3)
X_wine4, y_wine4 = aug_dataset(X_wine, y_wine, 4)
X_wine5, y_wine5 = aug_dataset(X_wine, y_wine, 5)
wine_bundle = [(X_wine,y_wine),(X_wine2,y_wine2),(X_wine3,y_wine3),
               (X_wine4,y_wine4),(X_wine5,y_wine5)]

# using XGBoost, CATBoost and LightGBM on all 5(10) datasets

def do_booster_models(model,X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    start_time = time.time()
    model.fit(X_train, y_train)
    test_score = model.score(X_test, y_test).round(4)
    execution_time_test = time.time() - start_time
    print("Execution time:",round(execution_time_test,4))
    print("acc",test_score)
    return {"time":execution_time_test,"acc":test_score}

for model_name in booster_names:
    print(model_name.upper())
    curr_model = booster_model[model_name]
    for i in range(5):
        print("Iris dataset number ",i)
        (X,Y) = iris_bundle[i]
        do_booster_models(curr_model,X,Y)
for model_name in booster_names:
    print(model_name.upper())
    curr_model = booster_model[model_name]
    for i in range(5):
        print("Wine dataset number ",i)
        (X,Y) = wine_bundle[i]
        do_booster_models(curr_model,X,Y)