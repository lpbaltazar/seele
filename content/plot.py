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

import matplotlib.style as style

sns.set()
style.use('seaborn-poster')
style.use('bmh')


def distrib_plot(file, content_type, title):
	df = pd.read_csv(file)
	print(df.head())
	for col in ['RECENCY', 'FREQUENCY', 'ENGAGEMENT']:
		plot = sns.distplot(a = df[col].values, kde = False)
		plot.set_xlabel(col)
		plot.set_title(title)
		plt.savefig('visualization/'+content_type+col+'.png', dpi = 600)
		plt.clf()

def distrib_combined():
	df2 = pd.read_csv("../data/customer_feature_matrix.csv", usecols = ["userid", "label"])
	df2.columns = df2.columns.str.upper()
	df2 = df2.loc(df2.LABEL == 'ACTIVE')
	channel2 = pd.read_csv('results/channel2.csv')
	channel2 = channel2.merge(df2, how = right, on = 'USERID')
	movie = pd.read_csv('results/movie.csv')
	movie = movie.merge(df2, how = right, on = 'USERID')
	origmovie = pd.read_csv('results/origmovie.csv')
	origmovie = origmovie.merge(df2, how = right, on = 'USERID')
	origshow = pd.read_csv('results/origshow.csv')
	origshow = origshow.merge(df2, how = right, on = 'USERID')

	for col in ['RECENCY', 'FREQUENCY', 'ENGAGEMENT']:
		plot = sns.distplot(a = channel2[col].values, kde = True, hist = False, label = 'CHANNEL 2')
		plot = sns.distplot(a = movie[col].values, kde = True, hist = False, label = 'MOVIE')
		plot = sns.distplot(a = origmovie[col].values, kde = True, hist = False, label = 'ORIGINAL MOVIE')
		plot = sns.distplot(a = origshow[col].values, kde = True, hist = False, label = 'ORIGINAL SHOW')
		plot.set_xlabel(col)
		plot.set_title(col)
		plt.tight_layout()
		plt.savefig('visualization/'+col+'.png', dpi = 600)


def scatter_plot(file, content_type, title):
	df = pd.read_csv(file)
	print(df.head())
	plot = sns.regplot('RECENCY', 'FREQUENCY', data = df, fit_reg = False)
	plot.set_xlabel('RECENCY')
	plot.set_ylabel('FREQUENCY')
	plot.set_ylim(0, 8000)
	plot.set_title(title)
	plt.savefig('visualization/scatter/'+content_type+'rf.png', dpi = 600)
	plt.clf()

	plot = sns.regplot('RECENCY', 'ENGAGEMENT', data = df, fit_reg = False)
	plot.set_xlabel('RECENCY')
	plot.set_ylabel('ENGAGEMENT')
	plot.set_ylim(0, 2000000)
	plot.set_title(title)
	plt.savefig('visualization/scatter/'+content_type+'re.png', dpi = 600)
	plt.clf()

	plot = sns.regplot('FREQUENCY', 'ENGAGEMENT', data = df, fit_reg = False)
	plot.set_xlabel('FREQUENCY')
	plot.set_ylabel('ENGAGEMENT')
	plot.set_ylim(0, 2000000)
	plot.set_title(title)
	plt.savefig('visualization/scatter/'+content_type+'fe.png', dpi = 600)
	plt.clf()

def plot_customer_segment(file, content_type, ylim1, ylim2):
	df = pd.read_csv(file)
	print(len(df))
	df2 = pd.read_csv("../data/customer_feature_matrix.csv", usecols = ["userid", "label"])
	df2.columns = df2.columns.str.upper()
	print(df2.head())
	print(len(df2))
	df = df.merge(df2, how = 'left', on = 'USERID')
	for i in ['NEW', 'ACTIVE', 'CHURNED']:
		temp = temp.loc[df.LABEL == i]
		plot = sns.regplot('RECENCY', 'FREQUENCY', data = temp, fit_reg = False)
		plot.set_xlabel('RECENCY')
		plot.set_ylabel('FREQUENCY')
		plot.set_ylim(0, ylim1)
		plot.set_title(i)
		plt.savefig('visualization/scatter_segment/'+content_type+i+'rf.png', dpi = 600)
		plt.clf()

		plot = sns.regplot('RECENCY', 'ENGAGEMENT', data = temp, fit_reg = False)
		plot.set_xlabel('RECENCY')
		plot.set_ylabel('ENGAGEMENT')
		plot.set_ylim(0, ylim2)
		plot.set_title(i)
		plt.savefig('visualization/scatter_segment/'+content_type+i+'re.png', dpi = 600)
		plt.clf()

		plot = sns.regplot('FREQUENCY', 'ENGAGEMENT', data = temp, fit_reg = False)
		plot.set_xlabel('FREQUENCY')
		plot.set_ylabel('ENGAGEMENT')
		plot.set_ylim(0, ylim2)
		plot.set_title(i)
		plt.savefig('visualization/scatter_segment/'+content_type+i+'fe.png', dpi = 600)
		plt.clf()


if __name__ == '__main__':
	# distrib_plot('results/channel2.csv', 'channel2', 'CHANNEL 2')
	# distrib_plot('results/origshow.csv', 'origshow', 'ORIGINAL SHOW')
	# distrib_plot('results/origmovie.csv', 'origmovie', 'ORIGINAL MOVIE')
	# distrib_plot('results/movie.csv', 'movie', 'MOVIE')

	# scatter_plot('results/channel2.csv', 'channel2', 'CHANNEL 2')
	# scatter_plot('results/origshow.csv', 'origshow', 'ORIGINAL SHOW')
	# scatter_plot('results/origmovie.csv', 'origmovie', 'ORIGINAL MOVIE')
	# scatter_plot('results/movie.csv', 'movie', 'MOVIE')

	# plot_customer_segment('results/channel2.csv', 'channel2', 8000, 200000)
	# plot_customer_segment('results/origshow.csv', 'origshow', 500, 35000)
	# plot_customer_segment('results/origmovie.csv', 'origmovie', 250, 17500)
	# plot_customer_segment('results/movie.csv', 'movie', 700, 50000)

	distrib_combined()