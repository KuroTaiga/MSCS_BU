## DATA PREPARATION
library(car)
# Read in the climbing dataset
df <- read.csv('climber_df.csv')
attach(df)

# Select subset of columns
df <- data.frame(df$sex, df$age, df$weight, df$height, df$years_cl, df$grades_max)

# Describe the data
df$df.sex <- as.factor(df$df.sex)
sex <- as.factor(sex)
summary(df)

# Check for NA
sum(is.na(df))
## there’s no NA for the current data, run the following line if there’s NA
# df <- na.omit(df)
length(df$df.sex)

hist(age)
summary(age)

hist(height)
summary(height)

hist(weight)
summary(weight)

hist(years_cl)
summary(years_cl)

hist(grades_max)
summary(grades_max)

## BUILDING MODEL
m <- lm(grades_max~age+sex+height+weight+years_cl, data=df)
coef(m)

## STATISTICAL ANALYSIS

# Global F-test
summary(m)
qf(0.95, df1=5, df2=10921)

#pairwise t-tests
summary(m)

## CHECK ASSUMPTIONS
## Residual plots, check for linearity, equal variance
par(mfrow = c(2,2))
plot(m)
## histogram of residuals, check for normality
hist(resid(m))
## Independent: plot residual vs index 
plot(resid(m), main = "Residual vs Index")

## Check for outliers
outlierTest(m)
## Check for influence point
b <- influence.measures(m)
c <- which(apply(b$is.inf, 1, any))
cd <- cooks.distance(m)
par(mfrow=c(1,1))
plot(m, which = 4)

## rule of thumb
cutoff = 4/nrow(df)
abline(h=cutoff,lty=2)
