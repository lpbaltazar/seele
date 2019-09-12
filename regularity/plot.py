import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk
import matplotlib as mpl
mpl.use('tKagg')
from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib.style as style

sns.set()
style.use('seaborn-poster')
style.use('bmh')

def plotRegularityFreq():
	file = "results/feb3_regularity.csv"
	df = readChunk(file, header = None)
	df.rename(columns = {0:'WEEK', 8:'RWEEK', 9:'USERID'}, inplace = True)
	df['RWEEK'] = df['RWEEK'].astype(int)
	plot = sns.distplot(a = df['RWEEK'].values, kde = False, bins = 7)
	new_df = df.groupby('USERID')['RWEEK'].mean().to_frame()
	new_df['RWEEK'] = round(new_df['RWEEK'])

	plot = sns.distplot(a = new_df['RWEEK'].values, kde = False, bins = 7)
	plt.show()

def plotRegularityTenure():
	file = 'results/tenure.csv'
	df = readChunk(file)
	df['RWEEK'] = df['RWEEK'].astype(float)
	df['TENURE'] = df['TENURE'].astype(float)

	for i in df.RWEEK.unique():
		temp = df.loc[df.RWEEK == i]
		plot = sns.distplot(a = temp['TENURE'].values, kde = False)
		plt.show()

if __name__ == '__main__':
	plotRegularityTenure()
