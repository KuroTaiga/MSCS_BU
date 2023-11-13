setwd("C:/BU/CSSE/CS555/HW1")
DaysRAW <- read.csv("./A01.csv",header = TRUE)
DaysPlot <- hist(DaysRAW$Days, main = "Duration of Hospital Stays", xlab = "Duration (Days)", 
                 breaks = max(DaysRAW)-min(DaysRAW)+1, xlim = c(min(DaysRAW),max(DaysRAW)+1),
                 ylim = (c(0,25)), plot = TRUE, right = F)

length(DaysRAW$Days)
median(DaysRAW$Days)# probably best as the "center" of the plot
mean(DaysRAW$Days)
var(DaysRAW$Days)
sd(DaysRAW$Days)
quantile(DaysRAW$Days)
min(DaysRAW)
max(DaysRAW)
DaysRAW$Days>=(4+1.5*(7-4))

# Question 2 --------------------------------------------------------------

MoreThanTen <- pnorm(10,5,3,lower.tail = FALSE)/pnorm(0,5,3,lower.tail = FALSE)
print(MoreThanTen)

# part b
MoreThanSix<- pnorm(6,5,7.528384,lower.tail = FALSE)/pnorm(0,5,7.528384,lower.tail = FALSE)
print(MoreThanSix)