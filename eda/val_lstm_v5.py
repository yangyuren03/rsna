#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 20:53:27 2019

@author: dhanley2
"""
import numpy as np
import math
import pandas as pd
import os
from sklearn.metrics import log_loss
import ast
import pickle

def dumpobj(file, obj):
    with open(file, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def loadobj(file):
    with open(file, 'rb') as handle:
        return pickle.load(handle)

label_cols = ['epidural', 'intraparenchymal', 'intraventricular', 'subarachnoid', 'subdural', 'any']
path_data = path='/Users/dhanley2/Documents/Personal/rsna/eda'
wts3 = np.array([0.6, 1.8, 0.6])


# Load up actuals
trndf = pd.read_csv(os.path.join(path_data, 'seq/v4/trndf.csv.gz'))
valdf = pd.read_csv(os.path.join(path_data, 'seq/v4/valdf.csv.gz'))
tstdf = pd.read_csv(os.path.join(path_data, 'seq/v4/tstdf.csv.gz'))

def makeSub(ypred, imgs):
    imgls = np.array(imgs).repeat(len(label_cols)) 
    icdls = pd.Series(label_cols*ypred.shape[0])   
    yidx = ['{}_{}'.format(i,j) for i,j in zip(imgls, icdls)]
    subdf = pd.DataFrame({'ID' : yidx, 'Label': ypred.flatten()})
    return subdf

# Load lstms
fname = 'seq/v8/lstmdeep_{}_emb_sz256_wt256_fold5_epoch{}.csv.gz'
lstmlssub = [pd.read_csv(os.path.join(path_data, \
                                     fname.format('sub', i)), index_col= 'ID') for i in range(1,8)]
#lstmlsval = [pd.read_csv(os.path.join(path_data, \
#                                     fname.format('val', i)), index_col= 'ID') for i in range(1,8)]
    

yactval = makeSub(valdf[label_cols].values, valdf.Image.tolist()).set_index('ID')
ysub = pd.read_csv(os.path.join(path_data, '../sub/lb_sub.csv'), index_col= 'ID')
subbst = pd.read_csv('~/Downloads/sub_pred_sz384_fold5_bag6_wtd_resnextv8.csv.gz', index_col= 'ID')

sublstm = pd.read_csv('~/Downloads/sub_lstm_emb_sz256_wt256_fold0_gepoch235.csv.gz', index_col= 'ID')
ylstmsub = sum(lstmlssub)/len(lstmlssub)
#ylstmval = sum(lstmlsval)/len(lstmlsval)
ylstmsub = ylstmsub.clip(0.0005, 0.9995)
#ylstmval = ylstmval.clip(0.0005, 0.9995)

#weights = ([1, 1, 1, 1, 1, 2] * valdf.shape[0])
#valloss = log_loss(yactval['Label'].values, ylstmval.loc[yactval.index]['Label'].values, sample_weight = weights)
#print('Epoch {} bagged val logloss {:.5f}'.format(3, valloss))


ylstmsub.Label[ylstmsub.Label>0.03].hist(bins=100)
ylstmval.Label[ylstmval.Label>0.03].hist(bins=100)
sublstm.Label[sublstm.Label>0.03].hist(bins=100)

idx = trnmdf.Image.isin([i[:12] for i in set(ylstmval.index.tolist())])
set(trnmdf[~idx].PatientID.unique().tolist()).intersection(set(trnmdf[idx].PatientID.unique().tolist()))


print(pd.concat([subbst, ylstmsub], 1).corr())
print(pd.concat([sublstm, ylstmsub], 1).corr())
print(pd.concat([subbst, ysub], 1).corr())

ylstmsub.to_csv(os.path.join(path, '../sub/sub_lstmdeep_emb_resnextv8_sz384_fold5_gepoch23456_bag4.csv.gz'), \
            compression = 'gzip')

subbag = subbst.copy()
subbag.Label = (ylstmsub.loc[subbst.index].Label + subbst.loc[subbst.index].Label )/2

ylstmsub.loc[subbst.index].Label.head()
subbst.head()
subbag.head()

subbag.to_csv(os.path.join(path, '../sub/BAG_lstm_emb_resnextv4_AND_resnextv8.csv.gz'), \
            compression = 'gzip')

subbst1 = pd.read_csv(os.path.join(path,
                            '../sub/sub_lstmdeep_emb_resnextv6_sz384_fold0_gepoch123456_bag4.csv.gz'), 
                            index_col= 'ID')
subbst2 = pd.read_csv(os.path.join(path,
                            '../sub/sub_lstmdeep_emb_resnextv8_sz384_fold5_gepoch1234567_bag4.csv.gz'), 
                            index_col= 'ID')
print(pd.concat([subbst1, subbst2], 1).corr())
subbag = subbst1.copy()
subbag["Label"] = (subbst1.Label + subbst2.loc[subbst1.index].Label)/2
print(pd.concat([subbst1, subbag], 1).corr())
print(pd.concat([subbst2, subbag], 1).corr())
subbag.to_csv(os.path.join(path, '../sub/sub_lstmdeep_emb_resnextv8_sz384_fold5_fold0_avg.csv.gz'), \
            compression = 'gzip')

