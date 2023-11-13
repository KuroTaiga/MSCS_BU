import os
import pandas as pd
import numpy as np

"""
This is the file for code, the answers are in JiankunDong_HW1_CS677.docx
"""
def read_data(ticker):
    # load data
    here =os.path.abspath( __file__ )
    input_dir =os.path.abspath(os.path.join(here,os.pardir))
    ticker_file = os.path.join(input_dir, ticker + '.csv')
    tidy_ticker = []
    try:   
        with open(ticker_file) as f:
            lines = f.read().splitlines()
        print('opened file for ticker: ', ticker)
        for l in lines:
            x = l.split(',')
            tidy_ticker.append(x)
        """ I made this into a read function
            see the rest of the code for assignment 1
        """
    except Exception as e:
        print(e)
        print('failed to read stock data for ticker: ', ticker)
    return tidy_ticker

def cal_aggre_table(tidy_ticker,weekday,year):
    # calculates the table entries for each weekday in a years
    currDay = []
    currR = []
    currRneg = []
    currRpos = []
    weekday_index = 4
    return_index = 13
    year_index = 1
    for l in tidy_ticker:
        if (l[weekday_index] == weekday and l[year_index]==year):
            currDay.append(l)
            if l[return_index][0] != "'":
                currReturn = float(l[return_index])
            else:
                currReturn = float(l[return_index][1:])
            currR.append(currReturn)
            if currReturn >= 0:
                currRpos.append(currReturn)
            else:
                currRneg.append(currReturn)
    result = [np.average(currR),np.std(currR),len(currRneg),np.mean(currRneg), np.std(currRneg),len(currRpos),np.mean(currRpos),np.std(currRpos)]
    #print(year,weekday,result) #test
    return result

def agg_table(tidy_data):
    # produce the table for the gived data
    weekDays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    years = ['2016','2017','2018','2019','2020']
    result = []
    for currYear in years:
        for weekday in weekDays:    
            curr = [currYear,weekday]+cal_aggre_table(tidy_data[1:],weekday,currYear)
            result.append(curr)
    return result

# Q1.1-1.2
print("Q1")
tidy_data_D = read_data('D')
print('Data for D')
D_result = agg_table(tidy_data_D)
# the following code makes it ezier for me to create the tables
output_dir = r'C:\BU\CSSE\CS677\week_1_homework'
D_file = os.path.join(output_dir, 'D_result' + '.csv')
with open(D_file, 'r+') as dfile:
    dfile.writable = True
    for line in D_result:
        currline = ','.join(str(e) for e in line)
        dfile.write(currline+'\n')
# Q1.3
negCount = posCount = 0
for e in D_result:
    negCount += e[4]
    posCount += e[7]
print('Negative return days count: ',negCount)
print('Non-genative return days count: ',posCount)
# Q1.4
# let's do some aveage across the board to see if we lose more on down day 
# or earn more on up day
ave_neg = ave_pos = 0
for e in D_result:
    ave_neg += e[5]
    ave_pos += e[8]
ave_neg = ave_neg/25
ave_pos = ave_pos/25
print('Overall ave loss on each day: ',ave_neg)
print('Overall ave gain on each day: ',ave_pos)
# Q2
"""
Please refer to the word document (as mentioned in the start of the file)
""" 
# Q3
print("Q3")
tidy_data_SPY = read_data('SPY')
print('Data for SPY')
SPY_result = agg_table(tidy_data_SPY)
# the following code makes it ezier for me to create the tables
output_dir = r'C:\BU\CSSE\CS677\week_1_homework'
SPY_file = os.path.join(output_dir, 'SPY_result' + '.csv')
with open(SPY_file, 'r+') as spyfile:
    spyfile.writable = True
    for line in SPY_result:
        currline = ','.join(str(e) for e in line)
        spyfile.write(currline+'\n')

#Q4
DMoney = 100
for l in tidy_data_D[1:]:
    currReturn = float(l[13])
    if currReturn>=0:
        DMoney += round(DMoney*currReturn,2)
print("Q4.1, my stock 'D' result: ",round(DMoney,2))

SPYMoney = 100
for l in tidy_data_SPY[1:]:
    currReturn = float(l[13])
    if currReturn>=0:
        SPYMoney += round(SPYMoney*currReturn,2)
print("Q4.2, 'SPY' result: ",round(SPYMoney,2))

#Q5
DMoney = 100
all_return_D = []
all_return_SPY = []
for l in tidy_data_D[1:]:
    currReturn = float(l[13])
    all_return_D.append(currReturn)
    DMoney += round(DMoney*currReturn,2)
print("Q5.1, my stock 'D' result: ",round(DMoney,2))
SPYMoney = 100
for l in tidy_data_SPY[1:]:
    currReturn = float(l[13])
    all_return_SPY.append(currReturn)
    SPYMoney += round(SPYMoney*currReturn,2)
print("Q5.2, 'SPY' result: ",round(SPYMoney,2))

#Q6
print("Q6")
# we got all the returns from Q5
D_a = D_b = D_c = SPY_a=SPY_b=SPY_c = 100
all_return_D.sort()
all_return_SPY.sort()

for i in range(0,len(all_return_D)-10):
    if all_return_D[i] >=0:
        D_a += round(D_a*all_return_D[i],2)
    if all_return_SPY[i] >=0:
        SPY_a += round(SPY_a*all_return_SPY[i],2)
print("Q6.1, for a, my stock: ",round(D_a,2))
print("Q6.1 for a, SPY: ",round(SPY_a,2))
for i in range(0,10):
    D_b += round(D_b*all_return_D[i],2)
    SPY_b += round(SPY_b*all_return_SPY[i],2)
for i in range(0,len(all_return_D)):
    if all_return_D[i] >=0:
        D_b += round(D_b*all_return_D[i],2)
    if all_return_SPY[i] >=0:
        SPY_b += round(SPY_b*all_return_SPY[i],2)
print("Q6.1 for b, my stock: ",round(D_b,2))
print("Q6.1 for b, SPY: ",round(SPY_b,2))

for i in range(0,5):
    D_c += round(D_c*all_return_D[i],2)
    SPY_c += round(SPY_c*all_return_SPY[i],2)
for i in range(0,len(all_return_D)-5):
    if all_return_D[i] >=0:
        D_c += round(D_c*all_return_D[i],2)
    if all_return_SPY[i] >=0:
        SPY_c += round(SPY_c*all_return_SPY[i],2)
print("Q6.1, for c, my stock: ",round(D_c,2))
print("Q6.1, for c, SPY: ",round(SPY_c,2))