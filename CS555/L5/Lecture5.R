#########################
## L05
#########################

library(ggplot2)

###################
## Section 01
###################

## study hour example ###############
student <- read.csv("students.csv")
student
attach(student)

# basic scatterplot
plot(student$hours, score)

# fancier scatterplot
plot(student$hours, score, 
     main="Scatterplot of exam score vs. hours of study", 
     xlab="Hours of study", 
ylab="Score", xlim=c(0,10), 
ylim=c(40,100), pch=18, col="red", cex.lab=1.5)

###################
## Section 02
###################

#calculate sample correlation
cor(student$hours, score)
cor(score, student$hours)

## What if one has missing data: NA
h <- c(study.hours, NA)
s <- c(score, 100)
cor(h, s)
cor(h, s, use="complete.obs")

## Inference about Population Correlation Coefficient
qt(0.975, df=29)
cor.test(study.hours, score)

###################
## Section 03
###################

my.model <- lm(score~study.hours)

# print the linear Values
print(my.model)

# Add regression line to the scatterplot
plot(study.hours, score, 
     main="Scatterplot of exam score vs. hours of study", 
     xlab="Hours of study", 
     ylab="Score", xlim=c(0,10), 
     ylim=c(40,100), pch=18, col="red", cex.lab=1.5)

abline(my.model)
abline(my.model, lty=15, col="blue")
abline(my.model, lty="dotted", col="blue")

# Calculate Confidence Intervals for Model 
# Parameters
confint(my.model)

?confint

# default level is .95
confint(my.model, level = .90)

# report a summary of my model 
summary(my.model)

# ggplot2
ggplot(student, aes(study.hours, score)) + 
        geom_point(color="red") +
        ggtitle("Scatterplot of exam score vs. hours of study") +
        xlab("Hours of study")

### Unemployment example ##############
unemployment <- read.csv("national_unemployment_rate.csv")
unemployment
attach(unemployment)

## xbar and sx
xbar <- mean(male.unemployment.rate)
xbar
sx <- sd(male.unemployment.rate)
sx

## ybar and sy
ybar <- mean(female.unemployment.rate)
ybar
sy <- sd(female.unemployment.rate)
sy

## r
r <- cor(male.unemployment.rate, female.unemployment.rate)
r

## beta1: Slope
## beta0: Intercept
beta1 <- r*sy/sx
beta1

beta0 <- ybar - beta1*xbar
beta0

## scatterplot with regression line
plot(male.unemployment.rate, female.unemployment.rate)
abline(a=beta0, b=beta1)

## run lm function to validate hand calculation beta0 and beta1
lm(female.unemployment.rate~male.unemployment.rate)

## Another example
## Relationship between height and bodymass
height <- c(176, 154, 138, 196, 132, 176, 181, 169, 150, 175)
bodymass <- c(82, 49, 53, 112, 47, 69, 77, 71, 62, 78)

# Create a scotterplot 
plot(bodymass, height)

# A better scotterplot
plot(bodymass, height, pch = 16, 
     cex = 1.3, col = "blue", 
     main = "HEIGHT PLOTTED AGAINST BODY MASS", 
     xlab = "BODY MASS (kg)", 
     ylab = "HEIGHT (cm)")

# Correlation 
cor(bodymass, height)
cor(height, bodymass)

# A simple linear regression
lm(height ~ bodymass)

# A line on the past plot
abline(98.0054, 0.9528)

# A better approach is to use variables and pass data to other functions 
m <- lm(height ~ bodymass)

# better would be to do this - No hard coding of data values.
abline(m)


###################
## Addtional Ex
###################
#The cars dataset contains two columns, speed and dist. 
#1) Draw scatter plot and describe the association between 
# the 2 variables based on the scatterplot. 
#2) Calculate the correlation coefficient between the 2 variables. 
#3) Are the correlation significant at alpha=0.05 ? 
#4) What is the confidence interval of the correlation coefficient? 
#5) Write the simple linear regression equation.
#6) fit the regression line in the scatterplot. 









##############
## Answer

plot(cars)
cor(cars)
cor.test(cars$speed, cars$dist)


(m <-lm(cars$dist~cars$speed))
abline(m)
