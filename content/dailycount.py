import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk
# import matplotlib as mpl
# mpl.use('tKagg')
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

import matplotlib.style as style

sns.set()
style.use('seaborn-poster')
style.use('bmh')

file = "../data/reg_origshow.csv"
df = readChunk(file, sep = '\t')
df.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)

file3 = "../data/reg_origmovie.csv"
df3 = readChunk(file3, sep = '\t')
df3.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)

df = pd.concat([df, df3])
print(df.head())

df.drop_duplicates(subset = ['USERID', 'DATE'], inplace = True)

label = pd.read_csv("../data/customer_feature_matrix.csv", usecols = ["userid", "label"])
label.columns = label.columns.str.upper()

print(len(df))

label = label.loc[label.LABEL == 'ACTIVE']
df = df.merge(label, how = 'left', on = 'USERID')
print(len(df))

new_df = df.groupby(['DATE', 'DAYOFWEEK'])['USERID'].count().to_frame()
print(new_df.head())
new_df.reset_index(inplace = True)

new_df['DATE'] = pd.to_datetime(new_df['DATE'])
# new_df['DATE'] = new_df['DATE'].dt.date


def line_format(label):
	month = label.strftime("%b")[:3]
	day = label.day

	return month+str(day)

new_df['MONTH'] = new_df.DATE.apply(lambda x: x.strftime("%b")[:3])
new_df.sort_values('DATE', inplace = True)
new_df.set_index('DATE', inplace = True)

for i in new_df.MONTH.unique():
	temp = new_df.loc[new_df.MONTH == i]
	xcoords = temp.loc[(temp.DAYOFWEEK == '1') | (temp.DAYOFWEEK == '7')].index
	print(xcoords)
	temp = temp[['USERID']]
	plot = temp.plot(kind = 'bar', legend = False)
	plot.set_xlabel('DATE')
	plot.set_ylabel('NUMBER OF CUSTOMERS')
	plot.set_xticklabels(map(lambda x: line_format(x), temp.index))
	plot.set_ylim(0,90000)
	for xc in xcoords:
		plt.axvline(x = xc, color = 'red', linestyle = '--')
	plt.show()


