import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../../")

import os
import csv
import time
import pandas as pd
import numpy as np

from utils import readChunk, toCSV

diverse = pd.read_csv("../../content/results/customer_feature_matrix_active.csv")
diverse = diverse.loc[diverse.CONTENT_TYPE_WATCHED == 'DIVERSE']
diverse = diverse[['USERID', 'CONTENT_TYPE_WATCHED']]

print(len(diverse))
current = readChunk("../../data/reg_current.csv", sep = '\t')
current.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
current = current.merge(diverse, how = 'left', on = 'USERID')
old = readChunk("../../data/reg_old.csv", sep = '\t')
old.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
old = old.merge(diverse, how = 'left', on = 'USERID')
origshow = readChunk("../../data/reg_origshow.csv", sep = '\t')
origshow.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
origshow = origshow.merge(diverse, how = 'left', on = 'USERID')
origmovie = readChunk("../../data/reg_origmovie.csv", sep = '\t')
origmovie.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
origmovie = origmovie.merge(diverse, how = 'left', on = 'USERID')
movie = readChunk("../../data/reg_movie.csv", sep = '\t')
movie.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
movie = movie.merge(diverse, how = 'left', on = 'USERID')

current = pd.concat([current, old, origmovie, origshow, movie])
print(len(current))
current = current.loc[current.CONTENT_TYPE_WATCHED == 'DIVERSE']
print(len(current))
print(len(current.USERID.unique()))