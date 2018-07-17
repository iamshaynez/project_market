#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:19:33 2018

@author: xiaowen
"""

import load_data
from global_env import SEC_FILE,PARAMETER_K_SIZE
import pandas as pd
from logic import trainingExample
import datetime

def prepareExamples():
    loader = load_data.tdx_loader()
    rng = pd.date_range(end=datetime.date.today() - datetime.timedelta(7) , periods = 400, freq='1B')
    rng = rng.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    lst_X = []
    lst_y = []
    
    df_sec = pd.read_csv(SEC_FILE,dtype={'code': 'str', 'market':'int'})
    for index, row in df_sec[0:2].iterrows():
        # load short mins K data
        df_short = loader.load(row['market'], row['code'], load_data.TDX_KTYPE_MAP['5'])
        
        # load long mins K data
        df_long = loader.load(row['market'], row['code'], load_data.TDX_KTYPE_MAP['30'])
        
        # load daily K data
        df_day = loader.load(row['market'], row['code'], load_data.TDX_KTYPE_MAP['Day'])
        
        # if inception day later than 100 days ago
        # not count into the model
        if df_day.shape[0] < 100:
            print('%s only has %i daily records, will pass it.' % (row['code'], df_day.shape[0]))
            continue
        
        # add into training example set
        for date in rng:
            X_values, score = trainingExample(df_long, df_short, df_day, date)
            if X_values is not None:
                if len(X_values) == PARAMETER_K_SIZE:
                    lst_X.append(X_values)
                    lst_y.append(score)
        
        print(row['code'], ' - all done - ', index, datetime.datetime.now())
    
    return lst_X, lst_y

if __name__ == "__main__":
    X, y = prepareExamples()
    print(len(X), len(y))
    print(y)