###########################
## Lecture 03
###########################

#install.packages("asbio")
# https://cran.r-project.org/web/packages/asbio/index.html
library(asbio)

##################
## Section 01
##################

## Compute confidence intervals for population 
## mean with given conditions
## Call Center example
## Assume that population 𝜎 = 15 minutes and
## sample mean of the wait times is x_bar = 30.9 minutes.
## The parameter of interest is the population mean, 𝜇.

#Compute z*
ConfLevel <- 0.99 #Define confidence level
LeftTail <- ConfLevel+(1-ConfLevel)/2
zStar <- qnorm(LeftTail)

#Compute margin of error given
n <- 100
sigma <- 15
MarginError <- zStar*sigma/sqrt(n)

#Compute lower and upper limits of the confidence interval 
#using sample mean = 55
(Lower <- 30.9-MarginError)
(Upper <- 30.9+MarginError)

##################
## Section 02
##################

?one.sample.z
# Read the documentation and make sure you understand it. 
# Provides a one-sample hypothesis test. 
# The test assumes that the underlying population is normal and 
# furthermore that the population standard deviation is known.

# Samples from 50 water sources throughout the county are taken and 
# the levels of this chemical are measured. 
# They are interested in testing the following hypotheses:

# H0: mu=15 (the mean level of the chemical is normal)
# H1: mu != 15 (the mean level of the chemical is abnormal)
# Suppose we know that the population standard deviation is 6.2. 
# The sample mean fromthe 50 samples was 16.4 ppm.
# Calculate the value of the test statistic and the associated p-value.

one.sample.z(null.mu = 15, xbar = 16.4, sigma = 6.2, 
             n = 50, alternative = "two.sided")
(zval <- (16.4-15)/(6.2/sqrt(50)))
# One sample z-test 
# z*            P-value
# 1.596693     0.1103342

# It appears that the sample mean that we observed 
# (xbar=16.4) is moderately likely to have occurred if the true
# population mean was 15 ppm (if mu=15). 
# This means we do not have strong evidence against the null hypothesis at 5% level.

##Critical value approach
1.5967 > qnorm(0.975)

##P value approach
##replicate p value
pnorm(1.597, lower.tail = F)*2
##compare p value with alpha level
0.11 < 0.05

##CI approach
ConfLevel <- 0.95 #Define confidence level
LeftTail <- ConfLevel+(1-ConfLevel)/2
zStar <- qnorm(LeftTail)

#Compute margin of error given
n <- 50
sigma <- 6.2
MarginError <- zStar*sigma/sqrt(n)

#Compute lower and upper limits of the confidence interval using sample mean = 55
(Lower <- 16.4-MarginError)
(Upper <- 16.4+MarginError)

#################################
#### Section 03 
#### One sided
#################################
# A gym is interested in whether a 6-week weight 
# loss training program they launched has
# been successful in helping their clients lose weight. 
# To assess this, they took a sample of
# 30 participants. They are interested in testing 
# the following hypotheses:

# H_0 : mu=0 (there is no efect on weight change of program participants)
# H_1 : mu<0 (program participants lose weight on average)

gym <- read.csv("gym_program.csv")
summary(gym$weight_lost)
mean(gym$weight_lost)
sd(gym$weight_lost)
nrow(gym)

popsd <- 6   #Suppose we know that for the general population, the standard deviation of changes in weights over a six-week interval is 6 pounds.
a <- 0.05    #pre-defined significance level

# CV approach
(z <- mean(gym$weight_lost)/(popsd/sqrt(nrow(gym))))
qnorm(a)

## p value approach
pnorm(z) < a

# CI apporach
(upper <- mean(gym$weight_lost)+qnorm(1-a)*popsd/sqrt(nrow(gym)))

one.sample.z(null.mu=0, xbar=mean(gym$weight_lost), 
             sigma=popsd, n=nrow(gym), alternative="less", 
             conf=0.95)
one.sample.z(null.mu = 0, xbar = -2.98, sigma = 6, n = 30, 
             alternative = "less")

# One sample z-test 
# z*            P-value
# -2.720355  0.00326059

# This is a small P-value. reject H0 at 5% level.

#################################
#################################
####   Additional Exercises 
#################################
#################################

#Exercise A
#A sample of size n = 64 produced the sample mean 
#of xbar = 16. Assuming the population standard 
#deviation is 4, compute the 95% and 99% confidence 
#intervals for the population mean

xbar <- 16
sigma<-4
n<-64
z1 <- qnorm(0.975)
(CI1<-c(xbar-z1*sigma/sqrt(n), xbar+z1*sigma/sqrt(n)))
z2 <- qnorm(0.995)
(CI2<-c(xbar-z2*sigma/sqrt(n), xbar+z2*sigma/sqrt(n)))

#Exercise B
#Assuming the population standard deviation is 4, how large 
#should a sample be to estimate the population mean ? with 
#a margin of error not exceeding 0.5 at 95% confidence?

z <- qnorm(0.975)
sigma <- 4
m <- 0.5
n <- (z*sigma/m)^2
n

#Exercise C
#A new diet program would like to claim that their program
#results in a mean weight loss (?) of more than 10 pounds in two
#weeks. Should the null hypothesis be ?<=10. 
#Write down the alternative hypothesis to test the claim.
## H1: ? > 10

#Assume our sample size is 30, sample mean is 10.8 and the 
#population sd=1. 
#Test the hypothesis at alpha=0.05 .  

one.sample.z(null.mu=10, xbar=10.8, sigma=1, 
             n=30, alternative="greater", conf=0.95)

#Exercise D
#We are interested in measuring the annual flow of the river Nile
#at Aswan (formerly Assuan). Assume we know the population sd is 169.
#Take a random sample of size 40 from data set Nile
library(sampling)
s <- srswor(40, length(Nile))
sample <- Nile[s != 0]

#Calculate the 95% confidence interval of the population mean. 
#Assume our null hypothesis is mu=919. Test it at alpha=0.05.

sigma <- 169
(xbar <- mean(sample))

(z <- qnorm(0.975))
(cl <- c(xbar-z*sigma/sqrt(40), xbar+z*sigma/sqrt(40)))

one.sample.z(null.mu=919, xbar=xbar, sigma=169, 
             n=40, alternative="two.sided", conf=0.95)
