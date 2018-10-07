#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:19:33 2018

@author: xiaowen
"""

import pandas as pd
import numpy as np
import datetime
from global_env import PARAMETER_K_SIZE_S, PARAMETER_K_SIZE_L, PARAMETER_RESULT_WITHIN_DAYS

'''
MACD: Short term line
MACDsignal: Longer term line
MACDhist: Green and Red bar
-----
Translate the relationship between 3 indices into one dimensional data
>>


'''
def trainingExample(df_long, df_short, df_day, date):
    no_data_flag = False
    strDate = getDateTimeWithEndMarketHour(date)
    # short term
    cur_index_short = df_short.loc[df_short['datetime'] == strDate].index
    if len(cur_index_short) == 0:
        no_data_flag = True
    
    # long term
    cur_index_long = df_long.loc[df_long['datetime'] == strDate].index
    if len(cur_index_long) == 0:
        no_data_flag = True
    
    if no_data_flag == False:
        # pull one set of K bar data
        df_X_short = df_short.loc[cur_index_short[0]-PARAMETER_K_SIZE_S+1:cur_index_short[0]].copy()
        df_X_long = df_long.loc[cur_index_long[0]-PARAMETER_K_SIZE_L+1:cur_index_long[0]].copy()
        
        # normalize K bar data
        df_X_short = normalize(df_X_short)
        df_X_long = normalize(df_X_long)

        
        # prepare X
        X_short = dfToExample(df_X_short)
        X_long = dfToExample(df_X_long)
        
        X_final = X_short + X_long
        
        # validation again
        df_X_values = pd.DataFrame(X_final)
        
        if df_X_values.shape[0] > 0:
            if not np.isfinite(df_X_values[0]).all():
                return None, None
        
    
        # result
        #print('single4 ', datetime.datetime.now())
        score = getScore(df_day, date, PARAMETER_RESULT_WITHIN_DAYS)
        #print('single5 ', datetime.datetime.now())
        return X_final, score
    else:
        return None, None

'''
dfToExample
----
Create a Example list X from a dataframe
'''
def dfToExample(df):
    X = df['close_NML'].tolist() + df['MACD_NML'].tolist() + df['MACDhist_NML'].tolist()
    return X


'''
getScore
----
Mark the score based on next few days performance
'''
def getScore(df_day, date, afterDays = 3):
    profit, lose = getHighestAndLowestPct(df_day, date, afterDays)
    if profit >= 0.07:
        return 4
    elif profit >= 0.03 and profit < 0.07:
        return 3
    elif profit < 0.03 and lose > -0.03:
        return 2
    elif profit < 0.03 and lose > -0.06:
        return 1
    else:
        return 0
'''
normalize
----
normalize data

USE avg of MACD and MACDsignal
NML with MACDhist

USE max close price
NML with close

assuming the df is with MACD, MACDsignal, MACDhist - all 3 columns
'''
def normalize(df):
    df['MACD2'] = (df['MACD'] + df['MACDsignal'])/2
    tmp_max = abs(df['MACD2'].max())
    tmp_min = abs(df['MACD2'].min())
    tmp = tmp_max if tmp_max >= tmp_min else tmp_min
    df['MACD_NML'] = df['MACD2'] / tmp
    df['MACDhist_NML'] = df['MACDhist']/tmp
    #df['MACDfinal'] = df['MACD2_NML'] * (abs(df['MACDhist_NML']) + 0.5)
    
    tmp_max = abs(df['close'].max())
    df['close_NML'] = df['close'] / tmp_max
    
    return df


#===================================================
#
# Utility functions
#
#===================================================
'''
getHighestAndLowestPct
----
Get the highest % and lowest % in the next <afterDays> days
'''
def getHighestAndLowestPct(df_day, date, afterDays = 3):
    profit, lose = getHighestAndLowestPrice(df_day, date, afterDays)
    price = getCurrentPrice(df_day, date)
    #print('Calculating...', date, price, profit, lose)
    return profit/price -1, lose/price - 1

'''
getHighestAndLowestPrice
----
Get the highest price and lowest price in the next <afterDays> days
'''
def getHighestAndLowestPrice(df_day, date, afterDays = 3):
    af_dt = getDateTimeWithEndMarketHour(date)
    index = df_day.loc[df_day['datetime'] == af_dt].index
    return df_day[index[0]+1:index[0] + afterDays]['high'].max(),df_day[index[0]+1:index[0] + afterDays]['low'].min()


'''
getCurrentPrice
----
df_day -> daily dataframe
date -> as of date
...
return
ending price as of day
'''
def getCurrentPrice(df_day, date):
    af_dt = getDateTimeWithEndMarketHour(date)
    return df_day.loc[df_day['datetime'] == af_dt]['close'].values[0]

'''
getDateTimeWithEndMarketHour
----
date -> a date
return -> date + 15:00:00 as the market close time
'''
def getDateTimeWithEndMarketHour(date):
    return str(pd.Timestamp(date) + datetime.timedelta(15/24))[:-3]

