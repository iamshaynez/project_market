#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:19:33 2018

@author: xiaowen
"""

import load_data



def normalize(df, *cols):
    for col in cols:
        tmp_max = abs(df[col].max())
        tmp_min = abs(df[col].min())
        tmp = tmp_max if tmp_max >= tmp_min else tmp_min
        df[col + '_NML'] = df[col] / tmp
    return df


