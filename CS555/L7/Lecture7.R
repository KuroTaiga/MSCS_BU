########################
## Lecture 07
########################

##############
## Section 01
##############

##Data import
ceo <- read.csv("CEO_salary.csv")

head(ceo)

##Data handling
salary1 <- ceo$salary/1000
ceo1 <- data.frame(age=ceo$age, 
                   height=ceo$height, 
                   salary_in_k=salary1)
head(ceo1)

cor(ceo1) #correlation coefficients
pairs(ceo1) #Draw a matrix of scatter plots

##Multiple linear regression
m <- lm(ceo1$salary_in_k~ceo1$age+ceo1$height)
m
m <- lm(salary_in_k~age+height, data=ceo1)
m
coefficients(m) # model coefficients
coef(m) # same as coefficients()
summary(m)

##############
## Section 02
##############

# ANOVA table by hand
fitted(m) # vector of fitted y values
(totalss <- sum((salary1 - mean(salary1))^2))
(regss <- sum((fitted(m) - mean(salary1))^2))
(resiss <- sum((salary1-fitted(m))^2))
(fstatistic <- (regss/2)/(resiss/97))
(pvalue <- 1-pf(fstatistic, df1=2, df2=97))
(R2 <- regss/totalss)

anova(m)

# Critical value of F test
qf(0.99, df1=2, df2=97)

##############
## Section 03
##############

# Critical value of t test
# for each individual predictor
## CV approach
(su <- summary(m))
qt(0.995, df=97)
## p value approach
pt(su$coef[8], 97, lower.tail = F)
##CI for coefficients
confint(m, level=0.95)

##############
## Section 04
##############

## Residual plots and hitogram to check assumptions
resid(m) # model residuals
residuals(m) # same as resid()
par(mfrow=c(2,2)) # Split graphing window
plot(fitted(m), resid(m), axes=TRUE, 
     frame.plot=TRUE, xlab='fitted values', ylab='residue')
abline(a=0, b=0)
plot(ceo1$age, resid(m), axes=TRUE, 
     frame.plot=TRUE, xlab='age', ylab='residue')
plot(ceo1$height, resid(m), axes=TRUE, 
     frame.plot=TRUE, xlab='height', ylab='residue')
hist(resid(m)) # check for normality

##############
## Additional Ex
##############

#The crime dataset contains 7 columns.
#crime.rate = total overall reported crime rate per 1 million residents
#vio.crime.rate = reported violent crime rate per 100,000 residents
#polic.fund = annual police funding in $/resident
#over25.4yHS = % of people 25 years+ with 4 yrs. of high school
#x16.19.noHS = % of 16 to 19 year-olds not in highschool and not highschool graduates.
#x18.24.college = % of 18 to 24 year-olds in college
#over25.4yCollege = % of people 25 years+ with at least 4 years of college
#Reference: Life In America's Small Cities, By G.S. Thomas

#1) Find out the association among these variables. 
#2) Perform MLR with crime.rate being the response variable.  
#3) Perform MLR with vio.crime.rate being the response variable.  
#4) Are the models statistically significant? Are they useful? 
#     Are the coefficents significant?


data <- read.csv("crime.csv")
data


#1) Calculate correlation and plot scatterplots to learn the associaton among variables
cor(data)
pairs(data)

#2) From above results, we identified variables that 
# associates with crime.rate 
# - police.fund (0.53), X16.19.noHS (0.32), 
# X18.24.college (-0.18), and over25.4yHs (-0.14).  
#Multiple linear regression
m <- lm(crime.rate~police.fund+X16.19.noHS+over25.4yHS+X18.24.college, data=data)
summary(m)

# Alternatively only use police.fund (0.53) and 
# X16.19.noHS (0.32) to set up MLR model
m1 <- lm(crime.rate~police.fund+X16.19.noHS, data=data)
summary(m1)

#3) Similar process as in 2)
m2 <- lm(vio.crime.rate~police.fund+X16.19.noHS, data=data)
summary(m2)

#4) Yes, modle m, m1 and m2 are all statistically significant with 
# p value <= 0.001
# beta_police.fund is the only significant coefficient in all models