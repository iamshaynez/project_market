# -*- coding: utf-8 -*-

"""
Created on Thu Jul 19 23:19:35 2018

@author: xiaowen
"""

import numpy as np
import util
import pandas as pd
from global_env import DATA_FOLDER
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import MeanShift
import datetime
from sklearn.cluster import MiniBatchKMeans



TRAINING_EXAMPLES = 'Data'

def load_training_data():
    df1 = util.pickle_load(DATA_FOLDER + 'Data_0-500_df.pickle')
    print('df1.shape: ', df1.shape)
    df2 = util.pickle_load(DATA_FOLDER + 'Data_500-900_df.pickle')
    print('df2.shape: ', df2.shape)
    df3 = util.pickle_load(DATA_FOLDER + 'Data_900-1500_df.pickle')
    print('df3.shape: ', df3.shape)
    df4 = util.pickle_load(DATA_FOLDER + 'Data_1500-2000_df.pickle')
    print('df4.shape: ', df4.shape)
    
    print('Merging the DFs...')
    df = pd.concat([df1, df2, df3, df4], ignore_index=True)
    print('Merged DF shape:' , df.shape,' saving to pickle...')
    util.pickle_dump(df, DATA_FOLDER + TRAINING_EXAMPLES + '_df_all.pickle')
    
    
    return df

def load_all_training_data():
    df = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_df_all.pickle')
    print('df.shape: ', df.shape)
    return df

def load_trained_data():
    df = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_df_trained.pickle')
    
    return df


def run():
    df_trained = load_trained_data()
    df_mean = df_trained.groupby('group')['y'].mean()
    util.pickle_dump(df_mean, DATA_FOLDER + TRAINING_EXAMPLES + '_df_mean.pickle')
    
    writer = pd.ExcelWriter(DATA_FOLDER + '/_trained_.xlsx')
    df_trained.to_excel(writer,'Sheet1')
    df_mean.to_excel(writer,'Sheet2')
    writer.save()

def train():
    df_train = load_all_training_data()
    
    X_train = df_train['X'].tolist()
    #print(X_train[0])
    print('prepare the bandwidth...')
    bandwidth = estimate_bandwidth(X_train, quantile=0.004, n_samples=30000, n_jobs=-2)
    print('training...', datetime.datetime.now())

    ms = MeanShift(bandwidth=bandwidth,n_jobs=-2)
    ms.fit(X_train)
    labels = ms.labels_
    print('completed...', datetime.datetime.now())
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    print("number of estimated clusters : %d" % n_clusters_)
    
    util.pickle_dump(ms, DATA_FOLDER + TRAINING_EXAMPLES + '_model_ms.pickle')
    print('re-predict...', datetime.datetime.now())
    df_train['group'] = ms.predict(X_train)
    print('re-predict completed...', datetime.datetime.now())
    util.pickle_dump(df_train, DATA_FOLDER + TRAINING_EXAMPLES + '_df_trained.pickle')
    
    print('mean...', datetime.datetime.now())
    df_mean = df_train.groupby('group')['y'].mean()
    util.pickle_dump(df_mean, DATA_FOLDER + TRAINING_EXAMPLES + '_df_mean.pickle')
    
    print('done...', df_mean.shape, ' ', datetime.datetime.now())
    
    
    writer = pd.ExcelWriter(DATA_FOLDER + '/_mean_.xlsx')
    df_mean.to_excel(writer,'Sheet1')
    #df2.to_excel(writer,'Sheet2')
    writer.save()
    
    
    return;

def trainMB():
    print('loading data...', datetime.datetime.now())
    df_train = load_all_training_data()
    
    X_train = df_train['X'].tolist()
    
    print('training...', datetime.datetime.now())

    #mkm = MiniBatchKMeans(n_clusters=000, random_state=0, batch_size=20000, reassignment_ratio=0.00001)
    mkm = MiniBatchKMeans(n_clusters=3000, random_state=0, batch_size=20000, reassignment_ratio=0.00002)
    
    mkm.fit(X_train)
    print('completed...', datetime.datetime.now())
 
    util.pickle_dump(mkm, DATA_FOLDER + TRAINING_EXAMPLES + '_model_mkm.pickle')
    print('re-predict...', datetime.datetime.now())
    df_train['group'] = mkm.predict(X_train)
    print('re-predict completed...', datetime.datetime.now())
    util.pickle_dump(df_train, DATA_FOLDER + TRAINING_EXAMPLES + '_df_trained.pickle')
    
    print('mean...', datetime.datetime.now())
    df_mean = df_train.groupby('group')['y'].mean()
    
    
    util.pickle_dump(df_mean, DATA_FOLDER + TRAINING_EXAMPLES + '_df_mean.pickle')
    
    print('done...', df_mean.shape, ' ', datetime.datetime.now())
    
    
    writer = pd.ExcelWriter(DATA_FOLDER + '/_mean_.xlsx')
    df = pd.DataFrame(df_mean)
    df.to_excel(writer,'Sheet1')
    #df2.to_excel(writer,'Sheet2')
    writer.save()
    
    
    return;

def tmp():
    df_train = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_df_trained.pickle')
    
    df_mean = df_train.groupby('group').agg(['count','mean']).reset_index()
    
    writer = pd.ExcelWriter(DATA_FOLDER + '/_mean_.xlsx')
    df = pd.DataFrame(df_mean)
    df.to_excel(writer,'Sheet1')
    #df2.to_excel(writer,'Sheet2')
    writer.save()
    
    
def evaluate():
    df1 = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_df_trained.pickle')
    
    writer = pd.ExcelWriter(DATA_FOLDER + '/_val_.xlsx')
    df = df1[df1['group'] == 1618]
    df.to_excel(writer,'Sheet1')
    #df2.to_excel(writer,'Sheet2')
    writer.save()
    #print(df1)


if __name__ == "__main__":
    #data = {'name':['Jack', 'Tom','Mary'], 'age':[18,19,20], 'gender':['m','m','w']}
    #df = pd.DataFrame(data)
    #df_mean = df.groupby('gender').mean()
    #print(df_mean.loc['m'])
    #run()
    #load_training_data()
    #trainMB()
    #evaluate()
    #tmp()
    trainMB()
    