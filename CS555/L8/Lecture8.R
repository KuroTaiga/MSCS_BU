############################
## Lecture 08
############################

####################
## Section 01
####################

library(car) #  Companion to Applied Regression

## Data handling
ceo <- read.csv("CEO_salary.csv")
head(ceo)
salary1 <- ceo$salary/1000
ceo1 <- data.frame(age=ceo$age, 
                   height=ceo$height, 
                   salary_in_k=salary1)

scatterplot(ceo1$salary_in_k~ceo1$age)
scatterplot(ceo1$salary_in_k~ceo1$height)

# Fit a Multiple Linear Regression model into data.
# Variables are Salary and age and store the resulted model into a variable for further use.
m <- lm(ceo1$salary_in_k~ceo1$age+ceo1$height)
m

resid(m)
par()              #Query Graphical Parameters
current <- par()   #save current settings
par(col.lab="red") #red x and y labels

par(mfrow=c(2,2)) 
plot(fitted(m), resid(m), axes=TRUE, frame.plot=TRUE, xlab='fitted values', ylab='residue')
plot(ceo1$age, resid(m), axes=TRUE, frame.plot=TRUE, xlab='age', ylab='residue')
plot(ceo1$height, resid(m), axes=TRUE, frame.plot=TRUE, xlab='height', ylab='residue')
hist(resid(m))

options(warn=-1)
par(current) # restore to the previous setting

####################
## Section 02
####################

##outlier test
##An outlier is a point with a large residual. 
##An influential point is a point that has a large
##impact on the regression. 
##They are not the same thing. 
##A point can be an outlier
##without being influential. 
##A point can be influential without being an outlier. 
##A point can be both or neither.
outlierTest(m)

##influential test
# Option 1
b <- influence.measures(m)
c <- which(apply(b$is.inf, 1, any))
ceo1[rownames(ceo1) %in% c, ]

# Option 2
cd <- cooks.distance(m)
plot(m, which = 5)
plot(m, which = 4)

## rule of thumb
cutoff = 4/nrow(ceo1)
abline(h=cutoff,lty=2)
ceo1[cd > cutoff, ]

####################
## Section 03
## Assumptions checking
####################

#Multiple linear regression
m <- lm(salary1~age+height, data=ceo1)
summary(m)
anova(m)
confint(m, level=0.95)

par(mfrow = c(2,2))
plot(m)
plot(m, ask=F)
par(mfrow = c(1,1))
plot(m, which=1)
#which selects which plot to be displayed. 
# https://stat.ethz.ch/R-manual/R-devel/library/stats/html/plot.lm.html

# Good resource for understanding the lm plots 
# https://data.library.virginia.edu/diagnostic-plots/

# R Cookbook Page 252
qqnorm(resid(m))
qqline(resid(m))
qqPlot(m)

# Here are some advanced regression diagnostics. 
# https://www.statmethods.net/stats/rdiagnostics.html 


####################
## Section 04
## Multi-collinearity
####################

vif(m)

# scatterplot matrix
panel.cor <- function(x, y, digits = 2, prefix = "", cex.cor, ...)
{
    usr <- par("usr")
    on.exit(par(usr))
    par(usr = c(0, 1, 0, 1))
    r <- abs(cor(x, y))
    txt <- format(c(r, 0.123456789), digits = digits)[1]
    txt <- paste0(prefix, txt)
    if(missing(cex.cor)) cex.cor <- 0.8/strwidth(txt)
    text(0.5, 0.5, txt, cex = cex.cor * (1+r)/2)
}

panel.hist <- function(x, ...)
{
    usr <- par("usr"); on.exit(par(usr))
    par(usr = c(usr[1:2], 0, 1.5) )
    h <- hist(x, plot = FALSE)
    breaks <- h$breaks; nB <- length(breaks)
    y <- h$counts; y <- y/max(y)
    rect(breaks[-nB], 0, breaks[-1], y, col = "cyan", ...)
}

panel.lm <- function(x, y,col=par('col'),bg=NA, pch=par('pch'), cex=1,col.smooth='red', ...) 
{
	points(x, y, pch=pch, col=col, bg=bg, cex=cex)
	abline(stats::lm(y~x), col=col.smooth, ...)
}

options(warn=-1)
pairs(ceo1, upper.panel=panel.cor, 
      diag.panel=panel.hist, lower.panel=panel.lm)

# cex	value indicates the amount by which plotting text and 
#  symbols should be scaled relative to the default. 
# 1=default, 1.5 is 50% larger, 0.5 is 50% smaller, etc.
# cex.axis magnification of axis annotation relative to cex
# cex.lab	magnification of x and y labels relative to cex
# cex.main	magnification of titles relative to cex
# col is the default plotting color

## Multi-collinearity
## VIF = 1: There is no correlation 
## between a given predictor variable 
## and any other predictor variables in the model.
## VIF between 1 and 5: There is moderate correlation 
## between a given predictor variable and other 
## predictor variables in the model.
## VIF > 5: There is severe correlation 
## between a given predictor variable and 
## other predictor variables in the model.

vif(m)

h <- read.csv("Height_Collinearity.csv")
head(h)
summary(mvif<-lm(Height ~ Age + Grade, data = h))
vif(mvif)

####################
## Section 05
## 3D
####################

# rgl Provides medium to high level functions for 3D interactive graphics, 
# including functions 
# modelled on base graphics (plot3d(), etc.) as well as functions for constructing representations of
# geometric objects (cube3d(), etc.). Output may be on screen using OpenGL, or to various standard 
# 3D file formats including WebGL, PLY, OBJ, STL as well as 2D image formats, including PNG, 
# Postscript, SVG, PGF.
install.packages("rgl")

library(rgl)
plot3d(ceo1$age, ceo1$height, ceo1$salary1, 
       type = "s", size = .75, 
       lit=FALSE, xlab="Age", ylab="Height", 
       zlab="Annual Salary")


