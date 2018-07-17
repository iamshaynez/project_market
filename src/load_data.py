#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 18:51:56 2018

@author: xiaowen
"""
from pytdx.hq import TdxHq_API
import numpy as np
import pandas as pd
import talib
import global_env

TDX_SERVER_PORT = 7709
TDX_SERVER_IP = '119.147.212.81'
TDX_KTYPE_MAP = {'5':0,'15':1,'30':2,'Hour':3,'Day':9}



# tdx loader
# using pytdx to load market data
'''
Market data loader
----
Provide standard format dataframe of market data
Columns: open, close, high, low, vol, amount, datetime, MACD, MACDSignal, MACDhist
----
tdx loader
use pytdx to load data
'''
class tdx_loader(object):
    
    def __init__(self):
        self.api = tdx_loader.getAPI()
        tdx_loader.getAPIConnect(self.api)
    
    @classmethod
    def getAPI(self):
        return TdxHq_API(auto_retry=True)
    
    @classmethod
    def getAPIConnect(self,api):
        return api.connect(TDX_SERVER_IP, TDX_SERVER_PORT)
    
    def __del__(self):
        class_name = self.__class__.__name__
        self.api.disconnect()
        print(class_name, "Destroy...")
        
    def load(self, market, code, ktype):
        # 5 mins K data
        times = 40
        if ktype == TDX_KTYPE_MAP['Day']:
            times = 3
        
        for i in range(times):
            
            temp = self.api.to_df(self.api.get_security_bars(ktype, market, code, (times-1-i)*800, 800))
            #print('%i records loaded' % temp.shape[0])
            if i == 0:
                data = temp
            else:
                data = data.append(temp)
            # ... same codes...
        return self.formatTdxData(self.prepareMACD(data.reset_index()))

    def prepareMACD(self, df):
        close = [float(x) for x in df['close']]
        df['EMA12'] = talib.EMA(np.array(close), timeperiod=12)
        df['EMA26'] = talib.EMA(np.array(close), timeperiod=26) 
        df['MACD'],df['MACDsignal'],df['MACDhist'] = talib.MACD(np.array(close),
                                fastperiod=12, slowperiod=26, signalperiod=9) 
        return df
 

    def formatTdxData(self, df):
        return df[['index','open','close','high','low','vol','amount','datetime','MACD','MACDsignal','MACDhist']]
    

if __name__ == "__main__":
    loader = tdx_loader()
    df_sec = pd.read_csv(global_env.SEC_FILE,dtype={'code': 'str', 'market':'int'})
    df = None
    for index, row in df_sec[0:1].iterrows():
        df = loader.load(row['market'], row['code'], TDX_KTYPE_MAP['5'])
        
        #df = df[['index']]
        print(df[23740:23760], len(df))


    for index, row in df[23740:23760].iterrows():
        print(index, row['MACD']**(-row['MACDhist']))
