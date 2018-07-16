#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:19:33 2018

@author: xiaowen
"""

import pandas as pd
import numpy as np
import datetime

PARAMETER_K_SIZE = 60
RESULT_WITHIN_DAYS = 3

def trainingData(df_long, df_short, df_day, date):
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
        df_X_short = df_short.loc[cur_index_short[0]-PARAMETER_K_SIZE+1:cur_index_short[0]].copy()
        df_X_long = df_long.loc[cur_index_long[0]-PARAMETER_K_SIZE+1:cur_index_long[0]].copy()
       
        df_X_short = normalize(df_X_short,'MACD','MACDhist')
        df_X_long = normalize(df_X_long,'MACD','MACDhist')
        
        
        # not working from here
        X_values = df_X_short['MACD_NML'].tolist()
        #X_values2 = df_X['MACDhist_NML'].tolist()
        
        df_X_values = pd.DataFrame(X_values)
        
        if df_X_values.shape[0] > 0:
            if not np.isfinite(df_X_values[0]).all():
                return None, None, None, None
    
        # result
        #print('single4 ', datetime.datetime.now())
        score = getScore(df_day, date, RESULT_WITHIN_DAYS)
        #print('single5 ', datetime.datetime.now())
        return X_values, score
    else:
        return None, None




'''
getScore
----
Mark the score based on next few days performance
'''
def getScore(df_day, date, afterDays = 3):
    profit, lose = getHighestAndLowestPct(df_day, date, afterDays)
    if lose < -0.1 and profit < 0.05:
        return 0
    elif profit > 0.06 and lose > -0.05:
        return 2
    else:
        return 1
'''
normalize
----
normalize data
'''
def normalize(df, *cols):
    for col in cols:
        tmp_max = abs(df[col].max())
        tmp_min = abs(df[col].min())
        tmp = tmp_max if tmp_max >= tmp_min else tmp_min
        df[col + '_NML'] = df[col] / tmp
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

