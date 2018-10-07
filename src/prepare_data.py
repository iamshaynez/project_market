#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:19:33 2018

@author: xiaowen
"""

import load_data
from global_env import SEC_FILE,PARAMETER_K_SIZE_S, PARAMETER_K_SIZE_L, LOAD_SEC_START, LOAD_SEC_END
import pandas as pd
from logic import trainingExample
import datetime

def prepareExamples(start, end):
    loader = load_data.tdx_loader()
    rng = pd.date_range(end=datetime.date.today() - datetime.timedelta(7) , periods = 1000, freq='1B')
    rng = rng.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    
    df_train = pd.DataFrame(columns=['code','date','X','y'])
    
    df_sec = pd.read_csv(SEC_FILE,dtype={'code': 'str', 'market':'int'})
    for index, row in df_sec[start:end].iterrows():
        # load short mins K data
        df_short = loader.load(row['market'], row['code'], load_data.TDX_KTYPE_MAP['15'])
        
        # load long mins K data
        df_long = loader.load(row['market'], row['code'], load_data.TDX_KTYPE_MAP['60'])
        
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
                if len(X_values) == PARAMETER_K_SIZE_S * 3 + PARAMETER_K_SIZE_L * 3:
                    df_train = df_train.append({'code':row['code'], 'date':date, 'X':X_values, 'y':score}, ignore_index=True)
                    
        
        print(row['code'], ' - all done - ', index, datetime.datetime.now())
        
    return df_train


def prepareExampleAsOfDay(market, code, date, loader):
    
    # load short mins K data
    df_short = loader.load(market, code, load_data.TDX_KTYPE_MAP['15'])
        
    # load long mins K data
    df_long = loader.load(market, code, load_data.TDX_KTYPE_MAP['60'])
        
    # load daily K data
    df_day = loader.load(market, code, load_data.TDX_KTYPE_MAP['Day'])
    
    X_values, score = trainingExample(df_long, df_short, df_day, date)
    df_train = pd.DataFrame(columns=['code','date','X','y'])
    df_train = df_train.append({'code':code, 'date':date, 'X':X_values, 'y':score}, ignore_index=True)
    
    return df_train
    
    
if __name__ == "__main__":
    #X, y = prepareExamples(LOAD_SEC_START,LOAD_SEC_END)
    #print(len(X), len(y))
    #print(X[0:1])
    df = pd.DataFrame(columns=['code','date','X','y','group','score'])
    X = [1,2,3]
    y = 0
    code = '000001'
    date = '20180908'
    df = df.append({'code':code, 'date':date, 'X':X, 'y':y}, ignore_index=True)
    print(df)
    
    






