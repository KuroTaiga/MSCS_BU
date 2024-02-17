import numpy as np
from numpy import polyfit, polyval
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy
import time
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures

from sklearn.metrics import mean_squared_error, r2_score,accuracy_score

import warnings
warnings.filterwarnings('ignore') 


# referred to https://zerowithdot.com/polynomial-regression-in-python/
## for finding out how to do polynormial regression with python

# function to generate multimodel gaussian distribution data
# default:
## seed = 0, 500 daatapoints for each segments, 3 segments

def createMultimodelGaussian(segments = 3, seed = 0, seg_dataCount = 500):
    rng = np.random
    rng.seed(seed)
    result = []
    means = []
    vars = []
    density = []
    
    for i in range(0,segments):
        #generate each segments
        mean = np.random.random()*100+i*50 
        means.append(mean)
        var = np.random.random()*10
        vars.append(var)
        result +=list(rng.normal(mean,var,seg_dataCount))
    x_range = np.linspace(min(result), max(result), seg_dataCount*segments)
    density = np.zeros_like(x_range)
    for i in range(3):
        density += norm.pdf(x_range,means[i], vars[i])

    return np.array(result),means,vars,density

# naive function of choosing the knot
# we pick the mid points of 2 means
def choose_knots(sectionMeans):
    knots = []
    for i in range(len(sectionMeans)-1):
        knots.append((sectionMeans[i]+sectionMeans[i+1])/2)
    return knots



# plot function
def plotDistribution(distribution):
    plt.hist(distribution, bins=100, density=True, alpha=0.6, color='g')
    plt.title('Multi-Modal Gaussian Distribution')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()

# from book, f test code
## turns the f stat and corresponding p value
def f_test(x, y):
    x = np.array(x)
    y = np.array(y)
    f = np.var(x, ddof=1)/np.var(y, ddof=1) #calculate F test statistic
    dfn = x.size-1 #define degrees of freedom numerator
    dfd = y.size-1 #define degrees of freedom denominator
    p = 1 - scipy.stats.f.cdf(f, dfn, dfd) #find p-value of F test statistic
    return f, p

# function for fitting the piecewise linear regression 
def fit_piecewise_linear(x,y, knots):
    modelList = []
    # find index of each knots
    
    startIndexPtr = 0
    predictions = np.zeros_like(y)
    # first to the one before last section
    for endIndex in knots:
        #prepare currX and reshape
        currX = x[startIndexPtr:endIndex][:,np.newaxis]
        currY = y[startIndexPtr:endIndex]
        model = LinearRegression().fit(currX,currY)
        modelList.append(model)
        predictions[startIndexPtr:endIndex] = model.predict(currX)
        startIndexPtr = endIndex
    # last section
    currX = x[startIndexPtr:][:,np.newaxis]
    currY = y[startIndexPtr:]
    model = LinearRegression().fit(currX,currY)
    modelList.append(model)
    predictions[startIndexPtr:] = model.predict(currX)

    return modelList,predictions

# function for fitting the piecewise polynomial regression
def fit_piecewise_poly(x,y, knots, degree = 3):
    modelList = []
    # find index of each knots
    
    startIndexPtr = 0
    predictions = np.zeros_like(y)
    # first to the one before last section
    for endIndex in knots:
        #prepare currX and reshape
        currX = x[startIndexPtr:endIndex][:,np.newaxis]
        currY = y[startIndexPtr:endIndex]
        poly = PolynomialFeatures(degree=degree)
        polyX = poly.fit_transform(currX)
        model = LinearRegression().fit(polyX,currY)
        modelList.append(model)
        predictions[startIndexPtr:endIndex] = model.predict(polyX)
        # currX = x[startIndexPtr:endIndex]
        # model = polyfit(currX,currY,deg=degree)
        # modelList.append(model)
        # predictions[startIndexPtr:endIndex] = polyval(model,currX)

        startIndexPtr = endIndex
    # last section
    currX = x[startIndexPtr:][:,np.newaxis]
    currY = y[startIndexPtr:]
    poly = PolynomialFeatures(degree=degree)
    polyX = poly.fit_transform(currX)
    model = LinearRegression().fit(polyX,currY)
    modelList.append(model)
    predictions[startIndexPtr:] = model.predict(polyX)
    # currX = x[startIndexPtr:]
    # model = polyfit(currX,currY,deg=degree)
    # modelList.append(model)
    # predictions[startIndexPtr:] = polyval(model,currX)
    return modelList,predictions
# function for fitting a single polynomial regression
def fit_poly(x, y, degree=3):
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x[:, np.newaxis])
    model = LinearRegression().fit(x_poly, y)
    predictions = model.predict(x_poly)
    # model = polyfit(x,y,deg=degree)
    # predictions = polyval(model,x)
    return  predictions

if __name__ == "__main__":
    BUID = 89
    poly_degree = 10
    ## 1) generating Multimodel Gaussian distribution

    distribution,means,vars,density = createMultimodelGaussian(segments=3,seed=BUID)
    # distribution would be y value and x would be indices value in this case
    x = np.array(list(range(len(distribution))))
    sorted_indices = np.argsort(distribution)
    sorted_distribution = distribution[sorted_indices]
    # ploting the distribution
    plotDistribution(distribution)
    # Choose knots
    yknots = choose_knots(means)
    xknots = [499,999]
    # f_test for each knots
    distribution_1 = sorted_distribution[0:500]
    distribution_2 = sorted_distribution[500:1000]
    distribution_3 = sorted_distribution[1000:]
    f_12,p_12 = f_test(distribution_1,distribution_2)
    f_13,p_13 = f_test(distribution_1,distribution_3)
    f_23,p_23 = f_test(distribution_2,distribution_3)
    print("F values of 12,13 and 23:",f_12,f_13,f_23)
    print("P values of 12,13 and 23:", p_12,p_13,p_23)

    # 6) keep in mind that we need to record the time for task 2 3 and 5
    ## 2) Piecewise Linear Regression w/ plot of splines and knots
    start_time = time.time()
    models, predictions = fit_piecewise_linear(x, distribution, xknots)
    execution_time_linear = time.time() - start_time

    plt.figure(figsize=(10, 6))
    plt.scatter(x, distribution[sorted_indices], alpha=0.3, label='Data')
    plt.scatter(x, predictions, color='red', label='Piecewise Linear Regression')
    plt.hlines(yknots, xmin=0, xmax=1500, linestyle='dashed', colors='k', label='Knots_Y')
    plt.vlines(xknots,ymin=min(predictions),ymax=max(predictions), linestyle='dashed', colors='k', label='Knots_X')
    plt.title('Piecewise Linear Regression with Splines and Knots')
    plt.xlabel('Indices')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

    mse_linear = mean_squared_error(distribution, predictions)
    r2_linear = r2_score(distribution, predictions)
   
    ## 3) Piecewise polynomial regression w/ plot of splines and knots

    start_time = time.time()
    models, predictions_piecewise_poly = fit_piecewise_poly(x, distribution, xknots,
                                                            degree=poly_degree)
    execution_time_piecewise_poly = time.time() - start_time

    plt.figure(figsize=(10, 6))
    plt.scatter(x, distribution[sorted_indices], alpha=0.3, label='Data')
    plt.scatter(x, predictions_piecewise_poly, color='red', label='Piecewise Poly Regression')
    plt.hlines(yknots, xmin=0, xmax=1500, linestyle='dashed', colors='k', label='Knots_Y')
    plt.vlines(xknots,ymin=min(predictions),ymax=max(predictions), linestyle='dashed', colors='k', label='Knots_X')
    plt.title('Piecewise Poly Regression with Splines and Knots')
    plt.xlabel('Indices')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
    mse_piecewise_poly = mean_squared_error(distribution, predictions_piecewise_poly)
    r2_piecewise_poly = r2_score(distribution, predictions_piecewise_poly)
    
    ## 4)
    print("For Linear: ")
    print("RSME: ", np.sqrt(mse_linear).round(4))
    print("R^2: ", r2_linear.round(4))

    print("For Pieciewise Poly: ")
    print("RSME: ", np.sqrt(mse_piecewise_poly).round(4))
    print("R^2: ", r2_piecewise_poly.round(4))

    ## 5) single polynomial
    start_time = time.time()
    predictions_single_poly = fit_poly(x, distribution, degree=poly_degree)
    execution_time_single_poly = time.time() - start_time

    # Plot the result
    plt.figure(figsize=(10, 6))
    plt.scatter(x, distribution[sorted_indices], alpha=0.3, label='Data')
    plt.plot(x, predictions_single_poly, color='red', label='Single Polynomial Regression')
    plt.title('Single Polynomial Regression')
    plt.xlabel('Value')
    plt.ylabel('Predicted Value')
    plt.legend()
    plt.show()
    mse_single_poly = mean_squared_error(distribution, predictions_single_poly)
    r2_single_poly = r2_score(distribution, predictions_single_poly)

    print("For Single Poly: ")
    print("RSME: ", np.sqrt(mse_single_poly).round(4))
    print("R^2: ", r2_single_poly.round(4))

    # Timings:
    print("Running time for piecewise linear: ", execution_time_linear)
    print("Running time for piecewise poly: ", execution_time_piecewise_poly)
    print("Running time for single poly: ", execution_time_single_poly)

    ## 7) applying ridge and LASSO
    poly = PolynomialFeatures(degree=poly_degree)
    x_poly = poly.fit_transform(x[:, np.newaxis])
    
    ridge = Ridge(alpha=100) 

    lasso = Lasso(alpha=100) 


    ridge.fit(x_poly,distribution)
    lasso.fit(x_poly, distribution)
    predictions_ridge = ridge.predict(x_poly)
    predictions_lasso = lasso.predict(x_poly)
    
    mse_ridge = mean_squared_error(distribution, predictions_ridge)
    r2_ridge = r2_score(distribution, predictions_ridge)
    mse_lasso = mean_squared_error(distribution, predictions_lasso)
    r2_lasso = r2_score(distribution, predictions_lasso)

    ridge_params = ridge.coef_
    lasso_params = lasso.coef_
    print("For Ridge: ")
    print("RMSE: ", np.sqrt(mse_ridge))
    print("R^2 ",r2_ridge)
    print("Coef: ", ridge_params)
    print("For Lasso: ")
    print("RMSE: ", np.sqrt(mse_lasso))
    print("R^2 ",r2_lasso)
    print("Coef: ", lasso_params)


    print("Lasso brought 2 highest degree of coeffiencient to 0, 2 less than ridge and basic polynomial")
    print("Ridge brought the hightest degree of coeffient CLOSE to 0")
    print("Ridge has better RMSE and R^2 of the 3, with Lasso having better RMSE and R^2 than basic polynomial")