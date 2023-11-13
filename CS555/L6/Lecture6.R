######################
# Lecture 6 code
######################

library(ggplot2)

##################
## Section 01
##################

student <- read.csv("students.csv")
head(student)
attach(student)

xbar <- mean(study.hours)
xbar
sx <- sd(study.hours)
sx

ybar <- mean(score)
ybar
sy <- sd(score)
sy

r <- cor(study.hours, score)
r

beta1 <- r*sy/sx
beta1

beta0 <- ybar - beta1*xbar
beta0

(m <- lm(score~study.hours))
fitted(m) ##y_hat
resid(m)  ##residual

# ggplot2
ggplot(student, aes(study.hours, score)) + 
  geom_point(color="red") +
  geom_smooth(method=lm, #Add linear regression line
              se=F,      #don't add shaded confidence region 
              fullrange=T) +  #Extend regression lines
  ggtitle("Scatterplot of exam score vs. hours of study") +
  xlab("Hours of study")

##F distribution Example
pf(18.51, 1, 2) ##Area to the left
pf(18.51, 1, 2, lower.tail = F) ##Area to the right
qf(0.95, 1, 2) ##getting F value given prob

# Get important overall summary information on the model
anova(m)
qf(.95,df1=1,df2=29)

# Each predictor
# t test
# Fstat = tstat^2
summary(m)
qt(0.975, df=29)
confint(m, level=0.95)

###### Age example #############
age <- read.csv("age.csv")
head(age)
plot(age$wife.age, age$husband.age)

xbar <- mean(age$wife.age)
xbar
sx <- sd(age$wife.age)
sx

ybar <- mean(age$husband.age)
ybar
sy <- sd(age$husband.age)
sy

r <- cor(age$wife.age, age$husband.age)
r

beta1 <- r*sy/sx
beta1

beta0 <- ybar - beta1*xbar
beta0
abline(a=beta0, b=beta1)
m <- lm(age$husband.age~age$wife.age)

abline(m)
anova(m)
qf(.95,df1 = 1,df2 = 3)
summary(m)
confint(m, level=0.95)

### Unemployment example ##############
unemployment <- read.csv("national_unemployment_rate.csv")
head(unemployment)
attach(unemployment)

xbar <- mean(male.unemployment.rate)
xbar
sx <- sd(male.unemployment.rate)
sx

ybar <- mean(female.unemployment.rate)
ybar
sy <- sd(female.unemployment.rate)
sy

r <- cor(male.unemployment.rate, female.unemployment.rate)
r

beta1 <- r*sy/sx
beta1

beta0 <- ybar - beta1*xbar
beta0

beta0+beta1*xbar

plot(male.unemployment.rate, female.unemployment.rate)
abline(a=beta0, b=beta1)
m <- lm(female.unemployment.rate~male.unemployment.rate)

anova(m)
summary(m)

##################
## Additional Ex
##################

#Exercise 1
#The cars dataset contains two columns, speed and dist. 
#Is there a linear relationship between speed and stopping distance? 
#1) Calculate the Residual, Regression, and Total Sum of Squares 
#   along with the R2 value for the model.
#2) Perform F test at the alpha=0.02 level.
#3) Perform T test at the alpha=0.02 level.






#answer to 1)
cars <- read.csv("cars.csv")
dim(cars)
# n is 50

(m <-lm(cars$dist~cars$speed))
a <- anova(m)
str(a)

(Reg.SS <- a$`Sum Sq`[1])
(Res.SS <- a$`Sum Sq`[2])
(Total.SS <- Reg.SS + Res.SS)
(R2 <- Reg.SS/Total.SS)

#answer to 2)

# df1 = 1; df2 = 50-1-1=48
qf(.98,df1=1,df2=48)

# Decision Rule: Reject H0 if F>=5.791633
# Otherwise, do not reject H0

anova(m)
# F=MS Reg SS/ MS Res SS = 89.567 > 5.791633
# We have significant evidence at the alpha=0.02  level 
# that beta1 does not equal to 0. 
# There is evidence of a significant linear 
# association between speed and stop distance.

#3) Perform T test at the alpha=0.02 level.
# df = n-2=48
qt(.99,df=48)  #2.406581
summary(m)
t <- 3.9324/0.4155 # 9.46426 > 2.406581
confint(m, level=0.98)
#Reject H0 since 9.46426 > 2.406581. We have significant evidence 
#at the alpha=0.02 level that beta0 != 0. There is evidence of a 
# significant inear association between speed and stopping distance. 
# We are 98% confident that the true value of beta1is between 
#2.93 and 4.93.



