######################
## L11
######################

#################
## Section 01
## One Proportion
#################

# One Sample Tests for a Proportion
# See the manual page for prop.test() function 
?prop.test

# The procedure gives a chi-square statistic which is 
# equal to the square of the z-statistic.
# http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/R/R-Manual/R-Manual13.html 

#####################
## The first example
## Infants Walk
#####################

# We want to know if 50% infants started warlking by 12 month. 
# Let's test the null hypothesis that 50% of infants start walking 
# by 12 months of age. 
# By default, R will perform a two-tailed test. 
# The variable 'walk' that takes on the value of 1 for infants 
# who walked by 1 year of age, 
# and 0 for infants who did not start walking until 
# after they were a year old. 
walkby12 <- read.csv("walkby12.csv")
head(walkby12)

walkby12$Walk1 = factor(walkby12$Walk)
table(walkby12$Walk1)
# In this sample, 36/50=.72 of the infants walked by 1 year. T

# prop.test( ) will perform the z-test comparing 
# this proportion to the hypothesized value; 
# input for the prop.test is the number of events (36), 
# the total sample size (50), 
# the hypothesized value of the proportion under the null 
# (p=0.50 for a null value of 50%). 

prop.test(36,50,p=0.5,correct=FALSE)
prop.test(36,50,p=0.5,correct=TRUE)

# Specifying 'correct=TRUE' tells R to use the small sample 
# correction when calculating the 
# confidence interval (a slightly different formula), 
# and specifying 'correct=FALSE' tells R 
# to use the usual large sample formula 
# for the z-test for a proportion 
# (since categorical data are not normally 
# distributed, the usual 
# z-statistic formula for the 
# confidence interval for a proportion is only 
# reliable with large samples).

#####################
## The second example
#####################

# We are interested in estimating the proportion of children in the
# county that are vaccinated for COVID. We suspect that it may be
# as low as 80%. A random sample is taken of 100 children from the
# county. Of those sampled, only 70 were vaccinated. Formally test
# if the proportion of vaccinated children is different than 80%.
prop.test(70, 100, p=0.8, conf.level=0.95, correct=FALSE) 
prop.test(70, 100, p=0.8, conf.level=0.95, correct=TRUE) 

#################
## Section 02
## Two Proportions
## Confidence Interval
## and Significance Test
#################

#####################
## The first example
## Preschool
#####################

# Two Sample Tests for Proportions
# When using prop.test() with vectors, 
# the first vector has to be 
# the number of successes, and the second 
# number has to be the total 
# number of cases.
prop.test(c(49, 38), c(61, 62), 
          conf.level=0.95, correct=FALSE) 
prop.test(c(49, 38), c(61, 62), 
          conf.level=0.95, correct=TRUE) 

#####################
## The second example
## Marriage
#####################
#Researchers asked randomly selected students in college in the south 
# whether they would 
# marry a person from a lower social class than their own. 
# Of the 149 men asked this 
# question, 91 responded yes while 117 women of the 
# 236 asked responded positively. 
#Calculate the 99% confidence interval comparing 
# the proportion of males versus 
# females who would marry someone from a lower social class.

prop.test(c(91, 117), c(149, 236), conf.level=0.99, correct=FALSE) 
(0.611-0.496)-2.576*sqrt(0.611*(1-0.611)/149+0.496*(1-0.496)/236)
(0.611-0.496)+2.576*sqrt(0.611*(1-0.611)/149+0.496*(1-0.496)/236)

#####################
## The third example
## Seat belt
#####################
#https://www.dummies.com/programming/r/how-to-test-data-proportions-with-r/
#In a hospital in North Carolina, the doctors registered the patients 
#who were involved in a car accident and whether they used seat belts. 
#The following matrix represents the number of survivors and 
#deceased patients in each group:

survivors <- matrix(c(1781,1443,135,47), ncol=2)
colnames(survivors) <- c('survived','died')
rownames(survivors) <- c('no seat belt','seat belt')
# When using prop.test() with a two-dimensional table (or matrix) with 2 columns, 
# giving the counts of successes and failures, respectively.
(result.prop <- prop.test(survivors))

#################
## Section 03
## risk difference, risk ratio, and odds ratio
#################

# For example, we have two groups of individuals:
# Group A with lung cancer: n = 500, 490 smokers, 
# Group B, healthy individuals: n = 500, 400 smokers, 
# In this setting, we want to know, 
# whether the proportions of smokers 
# are the same in the two groups of individuals?

prop.test(c(490, 400), c(500, 500), conf.level=0.95, correct=FALSE) 

# Calculate risk difference, risk ratio, and odds ratio

p1 <- 490/500
p2 <- 400/500
rd <- p1-p2
rr <- p1/p2
or <- ((p1/(1-p1))/(p2/(1-p2)))

#################
## Additional EX
#################

#Exercise 1
#Chicago cubs played 20 games and won 11 of them.
#Fans are "very confident" that the Cubs will win 
# more than half of the time. H0: p=0.5; H1: p>0.5.

prop.test(11, 20, p=0.5, alternative="greater") 

#Exercise 2
#A researcher is studying the coronavirus pandemic and wants
#to know what proportion of the population has been infected
#with the virus and has developed antibodies. They sample N = 200 
#individuals and perform a serum antibody test. 77 out of the 200
#individuals have antibodies. We expect that 50% of the population 
# has antibodies. Does this data support that theory?

phat <- 77/200
p <- 0.5
z <- (phat-p)/sqrt(p*(1-p)/200)
z

prop.test(77, 200, p=0.5) 



