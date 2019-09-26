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

diverse = pd.read_csv("results/diverse/diverse_1.txt", header = None)
diverse.rename(columns = {0:'USERID'}, inplace = True)
print(len(diverse))

current = readChunk("../../data/reg_current.csv", sep = '\t')
current.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
current = current.merge(diverse, how = 'right', on = 'USERID')
old = readChunk("../../data/reg_old.csv", sep = '\t')
old.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
old = old.merge(diverse, how = 'right', on = 'USERID')
origshow = readChunk("../../data/reg_origshow.csv", sep = '\t')
origshow.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
origshow = origshow.merge(diverse, how = 'right', on = 'USERID')
origmovie = readChunk("../../data/reg_origmovie.csv", sep = '\t')
origmovie.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
origmovie = origmovie.merge(diverse, how = 'right', on = 'USERID')
movie = readChunk("../../data/reg_movie.csv", sep = '\t')
movie.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)
movie = movie.merge(diverse, how = 'right', on = 'USERID')

current = pd.concat([current, old, origmovie, origshow, movie])

current['WEEK'] = pd.to_datetime(current['DATE'])
current['WEEK'] = current['WEEK'].apply(lambda x: x.strftime("%U"))
print(current['WEEK'])