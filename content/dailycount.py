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

def getFile(file1, file2 = None):
	df = readChunk(file1, sep = '\t')
	df.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)

	if file2:
		df2 = readChunk(file2, sep = '\t')
		df3.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)

		df = pd.concat([df, df2])
	
	print(df.head())
	df.drop_duplicates(subset = ['USERID', 'DATE'], inplace = True)

	label = pd.read_csv("../data/customer_feature_matrix.csv", usecols = ["userid", "label"])
	label.columns = label.columns.str.upper()

	label = label.loc[label.LABEL == 'ACTIVE']
	df = df.merge(label, how = 'left', on = 'USERID')
	return df

def getNumberofCustomers(df):
	new_df = df.groupby(['DATE', 'DAYOFWEEK'])['USERID'].count().to_frame()
	print(new_df.head())
	new_df.reset_index(inplace = True)

	new_df['DATE'] = pd.to_datetime(new_df['DATE'])

	new_df['MONTH'] = new_df.DATE.apply(lambda x: x.strftime("%b")[:3])
	new_df.sort_values('DATE', inplace = True)
	new_df.set_index('DATE', inplace = True)

def plot(new_df, ylim = None):
	fig, axes = plt.subplots(2,4)
	x = 0
	y = 0
	for i in new_df.MONTH.unique():
		temp = new_df.loc[new_df.MONTH == i]
		xcoords = temp.loc[(temp.DAYOFWEEK == '1') | (temp.DAYOFWEEK == '7')].index
		print(xcoords)
		temp = temp[['USERID']]
		axes[x, y] = temp.plot(kind = 'bar', legend = False)
		axes[x, y].set_xlabel('DATE')
		axes[x, y].set_ylabel('NUMBER OF CUSTOMERS')
		axes[x, y].set_xticklabels(map(lambda z: line_format(z), temp.index))
		if ylim:
			axes[x, y].set_ylim(0,90000)
		y = y + 1
		if y == 4:
			y = 0
			x = x + 1
	plt.show()

if __name__ == '__main__':
	df = getFile("../data/reg_origshow.csv", "../data/reg_origmovie.csv")
	df = getNumberofCustomers(df)
	plot(df, 90000)

