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
label = channel2.merge(label, how = 'right', on = 'USERID')
movie = pd.read_csv('results/movie.csv')
label = movie.merge(label, how = 'right', on = 'USERID')
origmovie = pd.read_csv('results/origmovie.csv')
label = origmovie.merge(dflabel2, how = 'right', on = 'USERID')
origshow = pd.read_csv('results/origshow.csv')
label = origshow.merge(label, how = 'right', on = 'USERID')

print(label.head())