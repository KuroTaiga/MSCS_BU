# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
this scripts reads your ticker file (e.g. MSFT.csv) and
constructs a list of lines
"""
import os

ticker='SPY'
here =os.path.abspath( __file__ )
input_dir =os.path.abspath(os.path.join(here,os.pardir))

try:   
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)
    """    Please check the hw1.py file <3
    """
    
except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)
