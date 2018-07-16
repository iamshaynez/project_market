#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:19:33 2018

@author: xiaowen
"""

import load_data
from global_env import SEC_FILE
import pandas as pd
import logic

def prepareData():
    loader = load_data.tdx_loader()
    rng = pd.date_range(end=datetime.date.today() - datetime.timedelta(7) , periods = 200, freq='1B')
    rng = rng.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    
    df_sec = pd.read_csv(SEC_FILE,dtype={'code': 'str', 'market':'int'})
    for index, row in df_sec[0:1].iterrows():
        # load 5 mins K data
        df_5 = loader.load(row['market'], row['code'], load_data.TDX_KTYPE_MAP['5'])
        
        # load daily K data
        df_day = loader.load(row['market'], row['code'], load_data.TDX_KTYPE_MAP['Day'])
        
        # if inception day later than 100 days ago
        # not count into the model
        if df_day.shape[0] < 100:
            print('%s only has %i daily records, will pass it.' % (row['code'], df_day.shape[0]))
            continue
        
        

