################
################
## L04
################
################

################
## Section 01
## functions related to t dist.
################

# calculate t value given probability
?qt
qt(0.9, df=9)
# [1] 1.383029

# calculate probability given a t value
?pt
pt(1.383, df=9)
# [1] 0.8999957

################
## Section 02
################

# Shark length example
# A scientist wishes to test the claim that great white sharks average 20 feet in length. 
# To test this, he measures 10 great white sharks. 
shark_len <- c(18.1, 23.4, 23.9, 24.1, 22.5, 19, 25.4, 23.1, 16.5, 26.7)
xbar <- mean(shark_len)
s <- sd(shark_len)
n <- length(shark_len)

##H0: mu = 20
##H1: mu > 20
##alpha = 0.1

###############
#critical value approach
###############

# calculate the t statistic 
t <- (xbar-20)/(s/sqrt(n))

(critical <- qt(0.9, df=12))

###############
#p value approach
###############

# calculate the t statistic 
t <- (xbar-20)/(s/sqrt(n))

# calculate the p-value , we are doing a one-sided greater t-test 
(p <- 1 - pt(t, df=n-1))

###############
#CI approach
###############

lb <- xbar - critical*s/sqrt(n)

###############
#t.test gives you all
###############

# read the manual of t-test function 
?t.test 

# Using the t.test function directly
# Please note that conf.level in the t.test function is used 
# only to calculate the confidence intervals
results<-t.test(shark_len, mu=20, alternative="greater", conf.level = 0.9)
# You can use 
names(results)

############
## Exercise
############

## Biologists studying the healing skin wounds
## measured by the rate at which new cells closed 
## a razor cut made in the skin of a newt.

## In another experiment, the researchers used the same 
## 18 newts and measured the healing rate after applying a 
## topical therapy that was developed to help speed up healing rates.
## The difference between the healing rate for each newt with and 
## without the topical treatment were calculated where positive 
## numbers indicated an increase in the healing rate.

## The resulting mean of the differences in the sample was 3.2 and 
## the standard deviation of the differences in the sample was 4.5.
## Test whether or not the topical treatment changed the healing 
## rate of the newts at the 𝛼 = 0.10 level of significance.

##CV approach
qt(0.05, 17, lower.tail = F)

##p value approach
pt(3.02, 17, lower.tail = F)*2

################
## Section 03
## Two sample independent test
################

# polyester decay example
# In order to assess how quickly polyester decays over time in landfills, 
# a researcher buried strips of the material in the soil
# for different lengths of time and then tested the force required 
# to break them (as a measure of 8decay). Lower breaking strength 
# is indicative of decay

# Test whether or not the breaking strengths of polyester strips buried 
# for 2 weeks is greater than the breaking strengths of
# those buried for 16 weeks. 

# Perform the test at the alpha=0.10 level of significance.

# First read the data as a dataframe into your R memory 
decay = read.csv("./decay.csv")

# Print out a summary of the data for the 2 weeks sample data 
summary(decay$strength[decay$weeks==2])
# Print out a summary of the data for the 16 weeks sample data 
summary(decay$strength[decay$weeks==16])

# Or you can do 
aggregate(decay$strength, by =list(as.factor(decay$weeks)), FUN=summary)
aggregate(decay$strength, by =list(as.factor(decay$weeks)), FUN=sd)


## H0: mu2w = mu16w
## H1: mu2w > mu16w
## alpha = 0.1

##CV approach
n <- nrow(decay)/2
t <- (mean(decay$strength[decay$weeks==2])-mean(decay$strength[decay$weeks==16]))/
sqrt(sd(decay$strength[decay$weeks==2])^2/n+sd(decay$strength[decay$weeks==16])^2/n)

qt(0.1, n-1, lower.tail = F)

##p value approach
p <- 1-pt(t, df=n-1)

# Compute the test t statistic and the associated p-value
# Fail to reject H0 since p-value is greater than ??
t.test(decay$strength[decay$weeks==2], decay$strength[decay$weeks==16], 
       alternative="greater", conf.level=0.9)

################
## Section 04
## Some additional R 
## This is not related to the one-sided test example
################

#install.packages("gplots")
library(gplots)
attach(decay)

m <- aggregate(strength, by=list(weeks), mean)
s <- aggregate(strength, by=list(weeks), sd)

## side by side boxplots
boxplot(strength~weeks)

## tapply function
(means <- tapply(strength, weeks, mean))

##How to use tapply to apply a user defined function "a"
##to data "strength" by "weeks"
##step1
##pick lower bound of confidence interval as
##an example
(t.test(strength)$conf.int[1])

##step2
##Define a user defined function "a"
##apply to strength by weeks
##We get the lowerbound for 2 week and 16 week respectively.
a <- function(v)
{
  t.test(v)$conf.int[1]
}

tapply(strength, weeks, a)

# step3
##This is the combined version of step2
##Everything in one line. 
##Also we added upperbound as well
(lower <- tapply(strength, weeks, function(v) t.test(v)$conf.int[1]))
(upper <- tapply(strength, weeks, function(v) t.test(v)$conf.int[2]))

##barplot2: An enhancement of the standard barplot() function.
##regular barplot
barplot(means, plot.ci=TRUE, ci.l=lower, ci.u=upper, 
        names.arg=c("2 weeks", "16 weeks"))
##see what is the difference using barplot2.
barplot2(means, plot.ci=TRUE, ci.l=lower, ci.u=upper, 
         names.arg=c("2 weeks", "16 weeks"))
abline(h=0)

################
## Additional Exs
################

#Exercise 1
#Are the average test scores of male and female students significally different? 
score <- read.csv("students_test_score.csv")

attach(score)
aggregate(Score, by=list(Gender), mean)
aggregate(Score, by=list(Gender), sd)

boxplot(Score~Gender)

t.test(Score[Gender=="F"], Score[Gender=="M"], alternative="two.sided", conf.level=0.95)
t.test(Score[Gender=="F"], Score[Gender=="M"], alternative="greater", conf.level=0.95)


means <- tapply(Score, Gender, mean)

lower <- tapply(Score, Gender, function(v) t.test(v)$conf.int[1])
upper <- tapply(Score, Gender, function(v) t.test(v)$conf.int[2])

barplot2(means, plot.ci=TRUE, ci.l=lower, ci.u=upper, names.arg=c("Female", "Male"))
abline(h=0)

#Exercise 2
# A teacher wants to know the appropriate number of questions to put in a quiz. 
# She sampled a group of students (n = 5) and ask them. The students respond with (3,2,2,5,0). 
# Calculate the 95% two-sided confidence interval for the population mean, given these responses. 

x <- c(3, 2, 2, 5, 0) 
xbar <- mean(x)
xbar
s <- sd(x)
s
se <- s/sqrt(5)
se
ci <- c(xbar-qt(0.975, 4)*se, xbar+qt(0.975, 4)*se)
ci


