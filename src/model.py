#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 21:43:53 2018

@author: xiaowen
"""


from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn import svm
#import util
import datetime
import matplotlib.pyplot as plt
import numpy as np
import itertools

def getClassifiers():
    models = {}
    model = KNeighborsClassifier(n_neighbors=4, weights='distance', algorithm='auto', 
                                 leaf_size=400, p=2, metric='minkowski', metric_params=None, n_jobs=2)
    models['KNeighborsClassifier1'] = model
          
    model = KNeighborsClassifier(n_neighbors=4, weights='distance', algorithm='auto', 
                                 leaf_size=200, p=2, metric='minkowski', metric_params=None, n_jobs=2)
    models['KNeighborsClassifier2'] = model
          
    model = svm.SVC()
    models['SVC'] = model
    
    
    return models

def train(models, X, y):
    for k in models:
        print('Start training model %s , ' % k, datetime.datetime.now())
        model = models[k]
        model.fit(X, y)
        print('End training model %s , ' % k, datetime.datetime.now())
        

def evaluate(models, X, y_true):
    class_names = [0,1,2]
    for k in models:
        print('Start eval model %s , ' % k, datetime.datetime.now())
        model = models[k]
        y_predict = model.predict(X)
        cnf_matrix = confusion_matrix(y_true, y_predict)
        plt.figure()
        plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=False,
                      title='Normalized confusion matrix')

        plt.show()

        print('End eval model %s , ' % k, datetime.datetime.now())
        
'''
plot_confusion_matrix
------
plot confusion matrix
copied from sklearn
'''
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
