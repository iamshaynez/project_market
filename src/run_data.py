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


TRAINING_EXAMPLES = 'default'

if __name__ == "__main__":
    X, y = pda.prepareExamples(env.LOAD_SEC_START, env.LOAD_SEC_END)
    util.pickle_dump(X, DATA_FOLDER + TRAINING_EXAMPLES + '_X.pickle')
    util.pickle_dump(y, DATA_FOLDER + TRAINING_EXAMPLES + '_y.pickle')
    X, y = pda.prepareExamples(env.TEST_SEC_START, env.TEST_SEC_END)
    util.pickle_dump(X, DATA_FOLDER + TRAINING_EXAMPLES + '_X_test.pickle')
    util.pickle_dump(y, DATA_FOLDER + TRAINING_EXAMPLES + '_y_test.pickle')


