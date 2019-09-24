import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

label = pd.read_csv("../data/customer_feature_matrix.csv", usecols = ["userid", "label"])
label.columns = label.columns.str.upper()

label = label.loc[label.LABEL == 'ACTIVE']
channel2 = pd.read_csv('results/channel2.csv')
channel2['CHANNEL2'] = 1
label = channel2[['USERID', 'CHANNEL2']].merge(label, how = 'right', on = 'USERID')
movie = pd.read_csv('results/movie.csv')
movie['MOVIE'] = 1
label = movie[['MOVIE', 'MOVIE']].merge(label, how = 'right', on = 'USERID')
origmovie = pd.read_csv('results/origmovie.csv')
origmovie['ORIGMOVIE'] = 1
label = origmovie[['USERID', 'ORIGMOVIE']].merge(label, how = 'right', on = 'USERID')
origshow = pd.read_csv('results/origshow.csv')
origshow['ORIGSHOW'] = 1
label = origshow[['USERID', 'ORIGSHOW']].merge(label, how = 'right', on = 'USERID')

print(label.head())