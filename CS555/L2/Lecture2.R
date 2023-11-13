## L02

###########################
## Section 01
##########################

#Exercise 1
#Find the area under the standard normal curve to the left of z=1.53
pnorm(1.53)

#Find the proportion of observations greater than z=-0.58.
1 - pnorm(-0.58)

#Exercise 2
# the area under the standard normal curve 
#between z=-1.25 and z=0.77.
pnorm(0.77) - pnorm(-1.25)

# The birth weights of newborns are normally distributed with a mean 
# of 3500g with a standard deviation of 500g.
# What proportion of infants weigh less than 2800g?
pnorm(2800, mean=3500, sd=500)

# What proportion of infants weigh between 3250g and 3750g?
pnorm(3750, mean=3500, sd=500) - pnorm(3250, mean=3500, sd=500)

#Exercise 3
# The distribution of SAT scores for the verbal section is approximately a normal 
# distribution with a mean of 504 and a standard deviation of 111. 
# What proportion of seniors score between 393 and 615?

pnorm(615, mean=504, sd=111) - pnorm(393, mean=504, sd=111)

#Jack got 393 and Mary got 615 in the verbal section. 
#How many standard deviation(s) away from the mean are 
#Jack and Mary's scores?

(393-504)/111
(615-504)/111

# Exercise 4
# Suppose we have selected a random sample of n=64 from a 
# population with a mean of 100 and a standard deviation of 16. 
# Find the probability that the sample mean will be between 
# 98 and 102.
mu <- 100
sigma <- 16
n <- 64
s <- sigma/sqrt(n)
s
pnorm(102, mean=mu, sd=s) - pnorm(98, mean=mu, sd = s)

#Exercise 5
# The lifespans of house cats are normally distributed. 
# The average house cat lives 14 years with the sd being 2 years.
# What is the probability of a cat living longer than 17 years. 

1 - pnorm(17, mean=14, sd=2)

######################
## Section 02
######################

## Plot Normal Distribution and shade a define area
x <- seq(from = -3, to = 3, length.out =100)
y <- dnorm(x)
plot(x, y, type="l")
plot(x, y, type="o")
#Shade an area from -1 to 1
xvalues <- x[x>=-2 & x<=1]
yvalues <- y[x>=-2 & x<=1]
region.x <- c(xvalues[1], xvalues, tail(xvalues,1))
region.y <- c(0, yvalues, 0)
polygon(region.x, region.y, col="navy", border="red")

# Another way to do it: 
## shade the region represented by P(-3 < X < -2). 
curve(dnorm(x,0,1),xlim=c(-3,3),main='Normal Density')

xvalues <- x[x>=-3 & x<=-2]
yvalues <- y[x>=-3 & x<=-2]
region.x <- c(xvalues[1], xvalues, tail(xvalues,1))
region.y <- c(0, yvalues, 0)
polygon(region.x, region.y, col="navy", border="red")


######################
## Section 03
######################

#outliers
earning <- c(35, 40, 145, 33, 30, 42, 32, 32, 25)
boxplot(earning)

iqr <- (quantile(earning, .75) - quantile(earning, .25))[[1]]
lower <- quantile(earning, .25)[[1]] - 1.5*iqr
upper <- quantile(earning, .75) [[1]]+ 1.5*iqr
outlier <- earning<lower | earning>upper
nooutlier <- earning>=lower & earning<=upper

earning[outlier]


###########
##CLT
###########


