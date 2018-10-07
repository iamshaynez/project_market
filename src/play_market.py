# -*- coding: utf-8 -*-

from prepare_data import prepareExampleAsOfDay
import pandas as pd
from global_env import DATA_FOLDER
import datetime
import util
import load_data

TRAINING_EXAMPLES = 'Data'

REPORT_NAME_PD = 'daily_report.xlsx'
REPORT_NAME_NEW = 'daily_report_newday.xlsx'

def getScore(df_matrix, y):
    return df_matrix[y] * 25

def init():
    #df = prepareExampleAsOfDay(0,'000001','2018-09-21')
    #print(df)
    asOfDay = '2018-09-27'
    loader = load_data.tdx_loader()
    
    print('load model...', datetime.datetime.now())
    model = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_model_mkm.pickle')
    score_matrix = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_df_mean.pickle')
    #print(score_matrix)
    print('load sec list...', datetime.datetime.now())
    df_sec = pd.read_csv(DATA_FOLDER + 'mysec.csv',dtype={'code': 'str', 'market':'int'} )
    df_sec = df_sec.set_index('code')
    
    print(df_sec)
    
    df_result = df_sec.copy()
    df_result[asOfDay] = -1.000
             
    for index, row in df_sec.iterrows():
        try:
            df = prepareExampleAsOfDay(row['market'],index ,asOfDay, loader)
            groups = model.predict(df['X'].tolist())
        
            group =groups[0]
            score = getScore(score_matrix, group)
        except:
            df_result[asOfDay][index] = -1
            print('%s,%s,%f' % (index,row['name'], -1))
        else:
            df_result[asOfDay][index] = score
            print('%s,%s,%f' % (index,row['name'], score))
    
    writer = pd.ExcelWriter(DATA_FOLDER + REPORT_NAME_PD)
    df_result.to_excel(writer,'Report')
    writer.save()

def delta():
    asOfDay = '2018-09-28'
    loader = load_data.tdx_loader()
    
    print('load model...', datetime.datetime.now())
    model = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_model_mkm.pickle')
    score_matrix = util.pickle_load(DATA_FOLDER + TRAINING_EXAMPLES + '_df_mean.pickle')
    
    print('load sec list...', datetime.datetime.now())
    df_sec = pd.read_excel(DATA_FOLDER + REPORT_NAME_PD, converters={'code': str, 'market':int})
    #print(df_sec)
    df_sec = df_sec.set_index('code')
    
    df_result = df_sec.copy()
    df_result[asOfDay] = -1.000
             
    for index, row in df_sec.iterrows():
        try:
            df = prepareExampleAsOfDay(row['market'],index ,asOfDay, loader)
            groups = model.predict(df['X'].tolist())
        
            group =groups[0]
            score = getScore(score_matrix, group)
        except:
            df_result[asOfDay][index] = -1
            print('%s,%s,%f' % (index,row['name'], -1))
        else:
            df_result[asOfDay][index] = score
            print('%s,%s,%f' % (index,row['name'], score))
    
    writer = pd.ExcelWriter(DATA_FOLDER + REPORT_NAME_NEW)
    df_result.to_excel(writer,'Report')
    writer.save()

if __name__ == "__main__":
    delta()
    