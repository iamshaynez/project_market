#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 23:19:35 2018

@author: xiaowen
"""

import model as md
import util
from global_env import DATA_FOLDER
from sklearn import preprocessing 

TRAINING_EXAMPLES = 'default'

def load_training_data():
    X = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_X.pickle')
    y = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_y.pickle')
    return X, y

def load_test_data():
    X = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_X_test.pickle')
    y = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_y_test.pickle')
    return X, y

def run():
    print('loading training data...')
    X, y = load_training_data()
    #min_max_scaler = preprocessing.MinMaxScaler()
    #X = min_max_scaler.fit_transform(X)
    
    util.count(y)
    print('loading data completed.')
    print('loading models...')
    models = md.getClassifiers()
    
    print('training models...')
    md.train(models, X, y)
    print('training models completed...')
    
    print('loading test data...')
    X_test, y_test = load_test_data()
    #min_max_scaler = preprocessing.MinMaxScaler()
    #X_test = min_max_scaler.fit_transform(X_test)
    
    util.count(y_test)
    print('loading test data completed...')
    
    print('eval models...')
    md.evaluate(models, X_test, y_test)
    print('eval models completed...')
    
if __name__ == "__main__":
    run()
    