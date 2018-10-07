#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 21:17:00 2018

@author: xiaowen
"""

import prepare_data as pda
import util
from global_env import DATA_FOLDER
import global_env as env


TRAINING_EXAMPLES = 'Data_1500-2000'

if __name__ == "__main__":
    print('prepare Training data...')
    df_train = pda.prepareExamples(env.LOAD_SEC_START, env.LOAD_SEC_END)
    util.pickle_dump(df_train, DATA_FOLDER + TRAINING_EXAMPLES + '_df.pickle')
    
    print(df_train['X'].shape)
    util.count(df_train['y'].tolist())
    
    print('prepare Test data...')
    df_train = pda.prepareExamples(env.TEST_SEC_START, env.TEST_SEC_END)
    util.pickle_dump(df_train, DATA_FOLDER + TRAINING_EXAMPLES + '_df_test.pickle')
    
    print(df_train['X'].shape)
    util.count(df_train['y'].tolist())

    #print(df_train)