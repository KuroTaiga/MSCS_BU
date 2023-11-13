#####################
## Section 01
#####################

##basic R types

42 + 1 * 2^4
1 + 7 != 7

mynumber <- 483
typeof(mynumber)
myint <- as.integer(mynumber)
typeof(myint)

mean(x = 1:5) # Does NOT save values in x
x
mean(x <- 1:5) # Does save values in x
x  # Print x # 1 2 3 4 5

#The vector is the most important one
#dimension data structure
my.vec <- c(1, 2, 67, -8)
#get structure properties
str(my.vec)
#number of values in a vector
length(my.vec)
#access element(s) with []
my.vec[3]
my.vec[c(3,4)]
#can do assignment too
my.vec[5] <- 41.2

##set and get work directory
setwd("")
getwd()

##help and summary
help(summary)
args(summary)
?cos
help(cos)
example(cos)

help.start()  # help in HTML format

??trigonometric # when don't remember exact function name
# find all functions related to a subject of interest
help.search("trigonometric") 

##demonstrations
demo() #List of demos
demo(lm.glm)  #linear modelling examples 
demo(graphics)  #multiple graphics examples

##functions
example(matrix) #examples of a function use
apropos("matrix") #list all function names that include the text matrix


ls() #list all the objects in the current workspace
objects() 
ls.str() #List Objects and their Structure

rm(a, b) #remove objects from the current workspace
rm(list=ls())

# Save content of the current workspace into .Rdata file
save.image()
save.image(file = "all.Rdata")
# Save some objects of the current workspace into the file
save(a, b, file = "part.Rdata")

##quit R
q()

##load the workspace or delete the workspace file
load("all.Rdata")
unlink("all.Rdata") #delete a file

# Install a package (only need to do it once)
# It will recognize dependencies between packages and install required sub packages
#install.packages("ggplot2") 
library(ggplot2) # Access the package
           
library() # view a list of installed packages
library(help="ggplot2") #see the documentation for a particular package
help(package="ggplot2")

##loaded libraries
search() # a list of packages that are currently loaded int memory
library("ggplot2")
search()
detach("package:ggplot2")
search()

#learn R in R
install.packages("swirl")
library(swirl)
swirl()

#display the commands history           
history()

#####################
## Section 02
#####################

## Qualitative data summaries
# Example 1.1 CEO Education Level
data <- read.csv("ceo.csv", header = F)
colnames(data)[1]<-"Education"
summary(data)
head(data)
dim(data)

#Frequencies:
table(data$Education)

summary(data$Education)
class(data$Education)

# Convert education to factor
edu <- factor(data$Education)
edu
summary(edu)

# Convert education to ordered factor
edu_ordered <- ordered(data$Education, 
                       levels = c("High School", 
                                  "College", "Master", "Other"))
edu_ordered 
#Frequency
table(edu_ordered)

#Relative frequencies:
table(data$Education)/nrow(data)
summary(edu)/nrow(data)

#Graphical summary
pie(table(data$Education)) 

slice.labels <- levels(edu)
slice.percents <- round(table(data$Education)/nrow(data)*100)
slice.labels <- paste(slice.labels, slice.percents)
slice.labels <- paste(slice.labels, "%", sep="")
slice.labels
pie(table(data$Education), 
    labels = slice.labels, 
    col=c("red", "green", "yellow", "blue"))

barplot(table(data$Education)/nrow(data))
barplot(table(data$Education), 
        main="CEO education levels", 
        xlab="Education level", ylab="Frequency")

barplot(table(edu_ordered), 
        main="CEO education levels", col = "pink",
        xlab="Education level", ylab="Frequency")

#####################
## Section 03
#####################

## Quantitative data summaries 
#Example 1.8 Employee age
employee <- read.csv("age_of_employees.csv")
mean(employee$Age)
median(employee$Age)
var(employee$Age)
sd(employee$Age)
quantile(employee$Age)
summary(employee$Age)

hist(employee$Age, breaks=20)
boxplot(employee$Age)

# Dealing with NA
age <- c(employee$Age, NA)
mean(age)
median(age)
var(age)
sd(age)
quantile(age)
summary(age)
mean(age, na.rm=TRUE)

#Data with outliers: Example 1.10
earning <- c(35, 40, 145, 33, 30, 42, 32, 32, 25)
summary(earning)
boxplot(earning)

#####################
## Section 04
## Exercises ETC.
#####################

###############
# Exercise 1
###############

# Read in data from file "diamond1000.csv"
# We are interested in the variable cut, which describes quality of 
# the cut (Fair, Good, Very Good, Premium, Ideal)

#1 How many of the diamonds are in ideal cut? 

dia <- read.csv("diamond1000.csv")
len <- nrow(dia)
table(dia$cut)

#2 What is the percentage of diamonds in ideal cut? 

class(dia$cut)
cut_ordered <- ordered(dia$cut, levels=c("Fair", 
                                         "Good", "Very Good", "Premium", "Ideal"))
f <- table(cut_ordered)
f

rf <- table(cut_ordered) / len
rf

slice.labels <- levels(cut_ordered)
slice.percents <- round(rf*100)
slice.percents

#3 Graphically summarize the diamond cut data. 

slice.labels <- paste(slice.labels, slice.percents)
slice.labels <- paste(slice.labels, "%", sep="")
slice.labels
pie(rf, labels = slice.labels)

barplot(table(cut_ordered), col = "pink",
        main="Diamond", xlab="Cut", ylab="Frequency")

###############
# Exercise 2
###############

# Data set Nile contains measurements of the annual flow of the river Nile 
# at Aswan 1871-1970

#1 How many measurements are there in the data set? 

Nile <- read.csv("Nile.csv")
nrow(Nile)

#2 What is the average annual flow of Nile from 1871 to 1970? 

mean(Nile$value)

#3 What is the median annual flow of Nile from 1871 to 1970? 

median(Nile$value)

#4 Calcuatel variance and standard deviation of the measurements. 

var(Nile$value)
sd(Nile$value)

#5 Graphically summarize the data. 
quantile(Nile$value)
hist(Nile$value)

par(mfrow=c(2,2)) # 2 by 2 panels
hist(Nile$value, breaks=6)
hist(Nile$value, col = "green", border = "red")
hist(Nile$value, breaks=14)
boxplot(Nile$value)
par(mfrow=c(1,1)) # Go back to single graph mode
