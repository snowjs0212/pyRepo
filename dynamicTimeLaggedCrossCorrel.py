# -*- coding: utf-8 -*-
"""
Created on Tue May 18 23:54:45 2021

@author: KevinJoonsoo
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

class dynamicTLCC():  
    """
    By Joonsoo Kim
    
    Summary:
        
        This operator allows users to run Time Lagged Cross Correlation across 
        all possible time intervals in a given data set. Also this allows users
        to modify the size of each time interval (n) and lag (L) to add 
        flexibility on the analysis of a pared time series data sets.
    
    Arguments:
        
        wd: working directory
        filename: file that contains time series data
        includeWknd: to include weekend for running model
        n: size of each time interval
        date_col: the name of column that contains 'date' field
        x1: first time series array (column) name
        x1: second time series array (column) name
        L: lag between 'X1' and 'X2'

    """
    def __init__(self, wd, filename):
        self.df = pd.read_excel(wd + filename)
        
    def filterWeekend(self, includeWknd):
        if includeWknd == 'Y':
            self.df = self.df
        elif includeWknd == 'N':
            self.df = self.df[self.df.WkendWkDay=='Weekday'].reset_index()
        else:
            self.df = None
            print("Error: Select 'Y' or 'N' for 'includeWknd' argument.")

    def parseDate(self, n, date_col):
        self.n = n
        self.date_col = date_col
        df_date = self.df[date_col]
        
        iterators = list(itertools.tee(df_date, n))
        for pos, iterator in enumerate(iterators):
            next(itertools.islice(iterator, pos, pos), None) 
        date_zip_ = zip(*iterators)
        self.date_list = [i for i in date_zip_]

    def tlcc(self, x1, x2, L=0):
        date_list = self.date_list
        df = self.df
        date_col = self.date_col
        
        start_date = []
        correl = []
        for date in date_list:
            start_d = min(date).strftime('%d-%b-%Y')
            df_ = df[df[date_col].isin(date)].reset_index()
            start_date.append(start_d)
            correl.append(df_[x1].corr(df_[x2].shift(L)))
        self.output = dict(zip(start_date, correl))
        
        return(self.output)

        
## Sample Run
# Parameters
wd_ = 'YOUR WD LOCATION'
filename_ = 'factCOVID+Ggle+Traffic.xlsx'
date_col_ = 'Date'
x1_ = 'Deaths_NormZ'
x2_ = 'TrafficPeakTotal_NormZ'

# Rendering functions
run = dynamicTLCC(wd = wd_, filename = filename_)
run.filterWeekend(includeWknd='N')
run.parseDate(n=10, date_col=date_col_)
result = run.tlcc(x1=x1_, x2=x2_)
result

# Exporting to csv for validation
df_export = pd.DataFrame(result, index=[0]).T.reset_index()
df_export.columns = ['Start_Date', 'Correlation']
df_export.to_csv('sample_output.csv', index=False)