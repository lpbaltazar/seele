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

print('combining data')
label = label.loc[label.LABEL == 'ACTIVE']
channel2 = pd.read_csv('results/channel2.csv')
channel2['CHANNEL2'] = 1
label = channel2[['USERID', 'CHANNEL2']].merge(label, how = 'right', on = 'USERID')
movie = pd.read_csv('results/movie.csv')
movie['MOVIE'] = 1
label = movie[['USERID', 'MOVIE']].merge(label, how = 'right', on = 'USERID')
origmovie = pd.read_csv('results/origmovie.csv')
origmovie['ORIGMOVIE'] = 1
label = origmovie[['USERID', 'ORIGMOVIE']].merge(label, how = 'right', on = 'USERID')
origshow = pd.read_csv('results/origshow.csv')
origshow['ORIGSHOW'] = 1
label = origshow[['USERID', 'ORIGSHOW']].merge(label, how = 'right', on = 'USERID')
label.fillna(0, inplace = True)
print(label.head())
label['sum'] = label['CHANNEL2'] + label['MOVIE'] + label['ORIGSHOW'] + label['ORIGMOVIE']

def getCustomerType(row):
	if row['sum'] == 4: return "DIVERSE"
	elif row['sum'] == 3:
		if (row['CHANNEL2'] == 1) & (row['MOVIE'] == 0) & (row['ORIGSHOW'] == 1) & (row['ORIGMOVIE'] == 1): return "CHANNEL2_MOVIE"
		elif (row['CHANNEL2'] == 1) & (row['MOVIE'] == 1) & (row['ORIGSHOW'] == 0) & (row['ORIGMOVIE'] == 1): return "DIVERSE"
		elif (row['CHANNEL2'] == 1) & (row['MOVIE'] == 1) & (row['ORIGSHOW'] == 1) & (row['ORIGMOVIE'] == 0): return "DIVERSE"
	elif row['sum'] == 2:
		if (row['CHANNEL2'] == 1) & (row['MOVIE'] == 1) & (row['ORIGSHOW'] == 0) & (row['ORIGMOVIE'] == 0): return "CHANNEL2_MOVIE"
		else: return "ORIGINALS"
	elif row['sum'] == 1:
		if (row['CHANNEL2'] == 1) & (row['MOVIE'] == 0) & (row['ORIGSHOW'] == 0) & (row['ORIGMOVIE'] == 0): return "CHANNEL2"
		elif (row['MOVIE'] == 1) & (row['MOVIE'] == 1) & (row['ORIGSHOW'] == 0) & (row['ORIGMOVIE'] == 0): return "MOVIE"

print('getting customer type')
contenttype = []
for i in range(len(label)):
	contenttype.append(getCustomerType(label.iloc[i]))

label['CONTENT_TYPE_WATCHED'] = contenttype
print('done')
label.to_csv('results/customer_feature_matrix_v2.csv', index = False)