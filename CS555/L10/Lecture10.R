##########################
## Lecture10
##########################
####################
## Section 01
####################

# Golf ball travel distance example
golf <- read.csv("golfball_C.csv")
head(golf)
golf$brand <- as.factor(golf$brand)
summary(golf)

attach(golf)
## runing one-way anova using aov function
g <- aov(dist~brand, data=golf)
summary(g)

## pairwise t test to find which two 
## are different
pairwise.t.test(dist, brand, p.adj='none') 
pairwise.t.test(dist, brand, p.adj='bonferroni')
TukeyHSD(g)

##Define dummy variables
##g0 is Callaway
##g1 is Nike
##g2 is Titleist
golf$g0 <- ifelse(brand=='Callaway', 1, 0)
golf$g1 <- ifelse(brand=='Nike', 1, 0)
golf$g2 <- ifelse(brand=='Titleist', 1, 0)

##g0 is Callaway (Middle 285)
##g1 is Nike (Lowest 260)
##g2 is Titleist (Highest 290)
##g0 is the reference group
m0 <- lm(dist~g1+g2, data=golf)
##if use dummy variable, use anova, not aov
anova(m0) ##anova table
#############################
## This is for comparison
#############################
## runing one-way anova using aov function
## one way anova is like a combined version 
## of dummy variable anova
g <- aov(dist~brand, data=golf)
summary(g)

## t test to compare means between groups
summary(m0) ##display coefs


##g0 is Callaway (Middle 285)
##g1 is Nike (Lowest 260)
##g2 is Titleist (Highest 290)
##g1 is the reference group
m1 <- lm(dist~g0+g2, data=golf)
anova(m1)
summary(m1)

##g0 is Callaway (Middle 285)
##g1 is Nike (Lowest 260)
##g2 is Titleist (Highest 290)
##g2 is the reference group
m2 <- lm(dist~g0+g1, data=golf)
anova(m2)
summary(m2)

####################
## Section 02
####################
### SBP by smoking status example
data <- read.csv("smoking_SBP.csv")
data
summary(data)
data$group <- as.factor(data$group)
summary(data) ##Do you see the difference?

aggregate(data$SBP, by=list(data$group), mean)
aggregate(data$SBP, by=list(data$group), sd)
boxplot(SBP~group, data=data, main="SBP by smoking status", xlab="group", 
        ylab="SBP", ylim=c(100, 160))

# wrong example
## treat group as if a continuous variable
mtest<- aov(SBP~grpnum, data=data)
summary(mtest)
# correct example
# Run a one-way ANOVA 
# (without adjustment for age).
# The global F-test showed that 
# mean SBP differed by smoking
# category (F=21.49 on 3 and 15 
# degrees of freedom, p < 0.001).
m1<- aov(SBP~group, data=data)
summary(m1)
qf(.95, df1=3, df2=15)

#pairwise comparison
pairwise.t.test(data$SBP, data$group, 
                p.adj='none') 
pairwise.t.test(data$SBP, data$group, 
                p.adj='bonferroni') 
TukeyHSD(m1)
plot(TukeyHSD(m1), cex.axis=.7)

## Dummy Variable version
data$g0 <- ifelse(data$group=='Current heavy smoker', 1, 0)
data$g1 <- ifelse(data$group=='Current light smoker', 1, 0)
data$g2 <- ifelse(data$group=='Former smoker', 1, 0)
data$g3 <- ifelse(data$group=='Never smoker', 1, 0)
# g3 is the reference
m2 <- lm(data$SBP~data$g0+data$g1+data$g2, data=data)
summary(m2)

# g0 is the reference
m3 <- lm(data$SBP~data$g1+data$g2+data$g3, data=data)
summary(m3)

# g1 is the reference
m4 <- lm(data$SBP~data$g0+data$g2+data$g3, data=data)
summary(m4)

# g2 is the reference
m5 <- lm(data$SBP~data$g0+data$g1+data$g3, data=data)
summary(m5)

# Use with caution! 
# First group is always the reference group
# match the results of g0 as the reference
mg <- lm(data$SBP~data$group, data=data)
summary(mg)
anova(mg) ##match summary(m1)

##aov results differs when predictors
##are in different order
# aov should not be used for ANCOVA
summary(aov(data$SBP~data$age+data$group, data=data))
summary(aov(data$SBP~data$group+data$age, data=data))

# ANCOVA
library(car)
## What do you find by adjusting for age?
Anova(lm(data$SBP~data$group+data$age, data=data), type=3)
#https://mcfromnz.wordpress.com/2011/03/02/anova-type-iiiiii-ss-explained/

# can also use Anova for one-way ANOVA
Anova(lm(data$SBP~data$group, data=data))
summary(aov(data$SBP~data$group, data=data))

#Least square means
# also called Estimated marginal means (EMMs)
# emmeans is the replacement for the lsmeans 
# library, so if you see code referring to 
# lsmeans, it is conceptually doing the same 
# thing as what emmeans will do. emmeans is 
# being developed; lsmeans is now deprecated. 
install.packages("emmeans")
library(emmeans)

install.packages("lsmeans")
library(lsmeans)

options('contrasts')
# contr.treatment is for non-ordered: eg. male vs female
#mostly we treat it as undered
#http://www.dummies.com/programming/r/how-to-set-the-contrasts-for-your-data-with-r/
X <- factor(c('A','B','C'))
contr.treatment(X)

##Notice that we need to enter two contrast settings. 
## The first handles unordered categorical variables, 
## the second, ordered.
## The setting is done by an options statement.
## The "constrasts" set in your R environment 
## determine how categorical variables are handled 
## in your models. The most common scheme in regression 
## is called "treatment contrasts": with treatment contrasts, 
## the first level of the categorical variable is assigned 
## the value 0, and then other levels measure the change 
## from the first level.
## Polynomial contrasts are useful for 
## handling ordered variables, that is, variables whose 
## levels are naturally ordered. 
## In this case, we put here just for demo purpose.

options(contrasts=c("contr.treatment", "contr.poly"))
m6 <- lm(data$SBP~data$group+data$age,data=data)
(m6.rg1 <- ref.grid(m6)) ##rgl: reference group level
# the continuous var displayed is the mean. That's the value used when comparing categorical var
# for this example, when comparing, says, Never smoker and Current heavy smoker, the age is taken into account
# and fixed at 37.316

#The emmeans() function creates the least square means 
# object from a fitted lm() object
# The 1st argument is the fitted lm object; 
# The 2nd is the variable we want 
# to work with. It must be one of the 
# variables in the fitted model.
# The function produces a table with estimated 
# means, standard errors and 
# confidence intervals for each mean. 
# To get something other than 95% confidence 
# intervals, use 
# summary( , level=0.90) to specify 
# the coverage you want
(m6.emm <- emmeans(m6, 'group'))
summary(m6.emm, level=0.90)

# The pairs() function computes all 
# pairwise differences.
# By default, pairs() uses a Tukey 
# adjustment for multiple comparisons.
# The adjust= argument changes that.
# adjust can also be adjust = "bonferroni";
# adjust = "scheffe"; or adjust = "none"; and
# so on.
pairs(m6.emm)
pairs(m6.emm, adjust = "bonferroni")
# After adjusting for age, we failed 
# to find significant difference in SBP 
# among groups

####################
## Section 03
####################
# Exercise example
exercise <- read.csv("exercise.csv")
exercise
attach(exercise)

#Test interactions
# Energy as the response
model <- lm(Energy~PreStretch+AnkleWeights+
              PreStretch*AnkleWeights, 
            data=exercise)
summary(model)
Anova(model, type=3)

# Speed as the response
model1 <- lm(Speed~PreStretch+AnkleWeights
             +PreStretch*AnkleWeights, 
             data=exercise)
summary(model1)
Anova(model1, type=3)

# Oxygen as the response
model2 <- lm(Oxygen~PreStretch+AnkleWeights
             +PreStretch*AnkleWeights, 
             data=exercise)
summary(model2)
Anova(model2, type=3)

# Generate interaction plots
interaction.plot(PreStretch, AnkleWeights, 
                 Energy, col=1:2)
interaction.plot(PreStretch, AnkleWeights, 
                 Speed, col=1:2)
interaction.plot(PreStretch, AnkleWeights, 
                 Oxygen, col=1:2)

#If interaction is significant, need to 
# stratify (by one of the two factors) 
# Since the interaction term is not significant, 
# this is just for demo.
stretch <- exercise[which(PreStretch=='Stretch'),]
nostretch <- exercise[which(PreStretch=='No stretch'),]
summary(aov(Energy~AnkleWeights, data=stretch))
summary(aov(Energy~AnkleWeights, data=nostretch))

# The other two response variables
summary(aov(Speed~AnkleWeights, data=stretch))
summary(aov(Speed~AnkleWeights, data=nostretch))
summary(aov(Oxygen~AnkleWeights, data=stretch))
summary(aov(Oxygen~AnkleWeights, data=nostretch))

####################
## Section 04
## Additional Ex
####################

#(Data set from http://www.statlab.uni-heidelberg.de/data/ancova/cholesterol.story.html)
#The purpose of the study was to estimate the effect of the agricultural weed yarrow on 
#the yield of white clover. It was anticipated that the clover yield would decrease as 
#the density of the yarrow increased. 
#Three areas A,B,C were selected in the clover seed crop. 
#Ten quadrats were positioned within each area using random coordinates on a 20x20 grid. 
#In each quadrat the clover seed was harvested and weighted, and the density of yarrow assessed 
#by counting the number of yarrow flower stems. 
c <- read.csv("clover.csv")
c
attach(c)

# 1. Nuemrically and graphically summarize clover yield by areas. 
# 2. What is F statistic? Are there differnece in mean clover yield across the areas at alpha = 0.05?  
# 3. Does the conclusion change after taking into consideration of Yarrow stems? 

#1
aggregate(Clover.yield, by=list(Area), summary)
boxplot(Clover.yield~Area, data=c, main="Clover yield", xlab="Area", 
          ylab="Yield", ylim=c(0, 90))

#2
m<- aov(Clover.yield~Area, data=c)
summary(m)
qf(.95, df1=2, df2=27)
# We failed to reject H0. 

#3
m1 <- lm(Clover.yield~Area+Yarrow.stems, data=c)
Anova(m1, type=3)
m1.emm <- emmeans(m1, 'Area')
pairs(m1.emm)

# No, the conclusion does not change. 