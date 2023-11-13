##########################
## Lecture09
##########################

####################
## Section 01
####################

####################
## Example 01
## Golf Ball
####################

# Golf ball travel distance example
golf <- read.csv("golfball_C.csv")
golf
attach(golf)
aggregate(dist, by=list(brand), summary)
aggregate(dist, by=list(brand), var)
m = mean(dist)
m # x..
sb2 <- (5*(285-m)^2+5*(260-m)^2+5*(290-m)^2)/2 #mean square between
sw2 <- ((5-1)*62.5+(5-1)*62.5+(5-1)*62.5)/(15-3)
F <- sb2/sw2
qf(df1=2, df2=12, 0.95)

# Global Test
g <- aov(dist~brand, data=golf)
summary(g)
# T test
pairwise.t.test(dist, brand, p.adj='none') 
pairwise.t.test(dist, brand, p.adj='bonferroni')
TukeyHSD(g)
plot(TukeyHSD(g), cex.axis=.7)

####################
## Example 02
## SBP and Smoking
####################

### SBP by smoking status example
data <- read.csv("smoking_SBP.csv")
data
is.factor(data$group)
is.factor(data$grpnum)
data$grpnum1 <- factor(data$grpnum, levels=c(0,1,2,3))

# Calculate mean, SD of SBP by groups
a <- aggregate(data$SBP, by=list(data$group), summary)
b<-aggregate(data$SBP, by=list(data$group), var)
m = mean(data$SBP)
sb2 <- (4*(a$x[1,4]-m)^2+5*(a$x[2,4]-m)^2+4*(a$x[3,4]-m)^2+6*(a$x[4,4]-m)^2)/(4-1) #mean square between
sw2 <- ((4-1)*b$x[1]+(5-1)*b$x[2]+(4-1)*b$x[3]+(6-1)*b$x[4])/(19-4)
F <- sb2/sw2

boxplot(SBP~group, data=data, main="SBP by smoking status", xlab="group", 
ylab="SBP", ylim=c(100, 160))
boxplot(SBP~grpnum, data=data, main="SBP by smoking status", xlab="group", 
        ylab="SBP", ylim=c(100, 160))

# wrong example
mtest<- aov(SBP~grpnum, data=data)
summary(mtest)
# correct example
m<- aov(SBP~group, data=data)
summary(m)
qf(.95, df1=3, df2=15)

####################
## Section 02
####################

#pairwise comparison
pairwise.t.test(data$SBP, data$group, p.adj='none') 
# pairwise t test with bonferroni adjustment 
pairwise.t.test(data$SBP, data$group, p.adj='bonferroni') 

is.factor(data$grpmum)
data$fnum = factor(data$grpnum)
data$fnum
m1<- aov(data$SBP~data$grpnum1, data=data)

# Compute Tukey Honest Significant Differences
?TukeyHSD

# pairwise test with TukeyHSD
TukeyHSD(m1)
plot(TukeyHSD(m1), cex.axis=.7)

###################
## Additional Ex
###################

#Exercise 1 (Data set from the below book)
#Armitage P, Berry G. Statistical Methods in Medical Research (3rd edition). Blackwell 1994.
#The data represent the numbers of worms isolated from the GI tracts of four groups of rats 
#in a trial. These four groups were the control (untreated) groups.
#We want to know if there is difference in mean worm counts across the four groups. 
worm <- read.csv("GI_tract_experiment.csv")
worm
attach(worm)

# 1. What is SST (total sum of squares) - the sum of the between and within variation? 
# 2. What is SSB (variation in the data between the samples)? What is MSB? 
# 3. What is SSW (variation in the data from each individual sample)? What is MSW? 
# 4. What is F statistic? Are there differnece in mean worm counts across the groups at alpha = 0.05?  

library(plyr)
ddply(worm, "Experiment", summarise,
             N    = length(numbers.of.worms),
             mean = mean(numbers.of.worms),
             sd   = sd(numbers.of.worms) )

#1
(xbar <- mean(numbers.of.worms))
(sst <- sum((numbers.of.worms-xbar)^2))

#2
(sample.mean <- aggregate(numbers.of.worms, by=list(Experiment), mean))
(ssb <- 5*sum((sample.mean$x-xbar)^2))
(msb <- ssb/(4-1))

#3
(sample.var <- aggregate(numbers.of.worms, by=list(Experiment), var))
(ssw <- (5-1)*sum(sample.var$x))
(msw <- ssw/(nrow(worm)-4))

#4
(f <- msb/msw)
# Obtain the Critical Value
(c <- qf(df1=4-1, df2=nrow(worm)-4, 0.95))

# since f<c, we fail to reject H0 at alpha = 0.05. 
# That is, we do not have evidence that the mean worm cournts
# in the 4 experiments are different.

# Global Test
g <- aov(numbers.of.worms~Experiment, data=worm)
summary(g)