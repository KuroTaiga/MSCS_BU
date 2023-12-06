"""
Jiankun Dong
Class: CS 677
Date: 11/20/2023
Commenly used function for HW6
"""
import pandas as pd
import xlrd
def getColVal(s,coln):
    values = []
    ## skip col name and padding
    for row in range(2,s.nrows-3):
        values.append(s.cell(row,coln).value)
    return values

def dataFormat():
    CTGbook = xlrd.open_workbook("CTG.xls")
    sh = CTGbook.sheet_by_index(2)
    ## I'm in group 2, so we should be using  
    # ASTV, MLTV, Max, Median

    ASTVCol = getColVal(sh,10)
    MLTVCol = getColVal(sh,13)
    MaxCol = getColVal(sh,20)
    MedianCol = getColVal(sh,25)
    NSPCol = getColVal(sh,sh.ncols-1)

    for i in range(0,len(NSPCol)):
        if NSPCol[i] != 1:
            NSPCol[i] = 0
        else:
            NSPCol[i] = 1
    return (ASTVCol,MLTVCol,MaxCol,MedianCol,NSPCol)