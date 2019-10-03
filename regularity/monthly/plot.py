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
	file = "../status/results/regularity_combined_monthly.csv"
	df = readChunk(file)
	print('Number of customers: ', len(df.USERID.unique()))
	print(df.head())
	df['RMONTH'] = df['RMONTH'].astype(int)
	df['MONTH'] = df['MONTH'].astype(int)
	df = df.loc[df.MONTH != 1]
	new_df = pd.DataFrame(index = list(range(1,31)), columns = ['COUNT'])
	new_df.index.name = 'REGULARITY'
	for i in range(1, 31):
		temp = df.loc[df.RMONTH == i]
		new_df.loc[i]['COUNT'] = len(temp)
	print(new_df.head())
	barPlot(new_df, 'REGULARITY', 'COUNT', 'regfreq_many.png', print_number = True, savefig = True)

	new_df = df.groupby('USERID')['RMONTH'].mean().to_frame()
	print(new_df.head())
	new_df2 = pd.DataFrame(index = list(range(1,31)), columns = ['COUNT'])
	new_df2.index.name = 'REGULARITY'
	for i in range(1, 31):
		temp = new_df.loc[new_df.RMONTH == i]
		new_df2.loc[i]['COUNT'] = len(temp)
	barPlot(new_df2, 'REGULARITY', 'NUMBER OF CUSTOMERS', 'customerregfreq_many.png', print_number = True, savefig = True)

def plotRegularityTenure():
	file = 'results/tenure.csv'
	df = readChunk(file)
	df['RWEEK'] = df['RWEEK'].astype(float)
	df['TENURE'] = df['TENURE'].astype(float)

	for i in df.RWEEK.unique():
		temp = df.loc[df.RWEEK == i]
		plot = sns.distplot(a = temp['TENURE'].values, kde = False)
		
		plot.set_ylim(0,4000)
		plt.title('Regularity = {}'.format(str(i)[0]))
		plot.set_xlabel('TENURE (days)')
		plot.set_ylabel('NUMBER OF CUSTOMERS')
		plt.savefig(str(i)+'.png', dpi = 600)
		plt.clf()

def barPlot(data, xlabel, ylabel, outfile, title = None, print_number = False, savefig = False, showfig = False):
	print('here')
	plot = data.plot(kind = 'bar', legend = False, rot = 0)
	if title: plt.title(title)
	if print_number:
		count = 0
		for i in plot.patches:
			plot.text(count, i.get_height()+.5, str(data.iloc[count]['COUNT']), horizontalalignment='center')
			count = count + 1
	plot.set_xlabel(xlabel)
	plot.set_ylabel(ylabel)
	if savefig:
		plt.savefig(outfile, dpi = 600)
	if showfig:
		plt.show()
	plt.clf()

def plotWeeklyRegularity(weekno = None, custids = None, ylim = None, outfile = None):
	df = readChunk("../status/results/regularity_combined.csv")
	print(len(df))
	if type(custids) is list:
		df = df[df['USERID'].isin(custids)]
		print('Number of customers: ', len(df.USERID.unique()))
	
	df.dropna(subset = ['RMONTH'], inplace = True)

	print('Number of customers: ', len(df.USERID.unique()))
	df['RMONTH'] = df['RMONTH'].astype(int)
	df['MONTH'] = df["MONTH"].astype(int)
	df = df.loc[df.MONTH != 1]
	df.sort_values('MONTH', inplace = True)
	fig, axes = plt.subplots(4,2, sharey = 'row', constrained_layout = True)
	x = 0
	y = 0

	for i in df.MONTH.unique():
		temp = df.loc[df.MONTH == i]
		new_df = pd.DataFrame(index = list(range(1,31)), columns = ['COUNT'])
		new_df.index.name = 'REGULARITY'
		for j in range(1,31):
			temp2 = temp.loc[temp.RMONTH == j]
			new_df.loc[j]['COUNT'] = len(temp2)
		plot = new_df.plot(kind = 'bar', legend = False, ax = axes[x, y], rot = 0)
		plot.tick_params(axis = 'both', which = 'major', labelsize = 6, pad = 2)
		plot.set_title(i, size = 6, pad = 2)
		x_axis = plot.axes.get_xaxis()
		x_label = x_axis.get_label()
		x_label.set_visible(False)
		if ylim:
			plot.set_ylim(0,ylim)
		y = y + 1
		if y == 2:
			y = 0
			x = x + 1
		new_df.to_csv('results/reqfreq/week_'+str(i)+'.csv')
	fig.delaxes(axes[7,3])
	fig.delaxes(axes[7,2])
	# outfile = "results/regfreq"+z+str(i)+'.png'
	if outfile:
		plt.savefig(outfile, dpi = 600)


def plotWeeklyRegularity2(weekno = None, custids = None, ylim = None, outfile = None, regularity_type = 'mean', mode_type = None):
	df = readChunk("../status/results/regularity_combined_monthly.csv")
	print(len(df))
	if type(custids) is list:
		df = df[df['USERID'].isin(custids)]

	print('Number of customers: ', len(df.USERID.unique()))
	

	df.dropna(subset = ['RWEEK'], inplace = True)

	print('Number of customers: ', len(df.USERID.unique()))
	df['RMONTH'] = df['RMONTH'].astype(int)
	df['MONTH'] = df["MONTH"].astype(int)
	df = df.loc[df.MONTH != 1]
	if regularity_type == 'mode':
		if mode_type == 'min':
			df = df.groupby('USERID')['RWEEK'].agg(lambda x: min(pd.Series.mode(x))).to_frame()
		elif mode_type == 'max':
			df = df.groupby('USERID')['RWEEK'].agg(lambda x: max(pd.Series.mode(x))).to_frame()
		else:
			df = df.groupby(['USERID'])['RWEEK'].agg(lambda x: pd.Series.mode(x)[0]).to_frame()
	elif regularity_type == 'mean':
			df = df.groupby('USERID')['RWEEK'].mean().to_frame()
	else:
		print('What regularity type?')
	fig, axes = plt.subplots(4,2, sharey = 'row', constrained_layout = True)
	x = 0
	y = 0
	for i in sorted(df_2.WEEK.unique()):
		temp = df_2.loc[df_2.WEEK == i]
		new_df = pd.DataFrame(index = list(range(1, 32)), columns = ['COUNT'])
		new_df.index.name = 'REGULARITY'
		for j in range(1, 32):
			temp2 = temp.loc[temp.RMONTH == j]
			new_df.loc[j]['COUNT'] = len(temp2)
			print(new_df)
		plot = new_df.plot(kind = 'bar', legend = False, ax = axes[x, y], rot = 0)

		plot.tick_params(axis = 'both', which = 'major', labelsize = 6, pad = 2)
		plot.set_title(i, size = 6, pad = 2)
		x_axis = plot.axes.get_xaxis()
		x_label = x_axis.get_label()
		x_label.set_visible(False)
		if ylim:
			plot.set_ylim(0,ylim)
		y = y + 1
		if y == 2:
			y = 0
			x = x + 1
		new_df.to_csv('results/customerregfreq/week_'+z+str(i)+'.csv')
	fig.delaxes(axes[7,3])
	fig.delaxes(axes[7,2])
	if outfile:
		plt.savefig(outfile, dpi = 600)

if __name__ == '__main__':
	plotRegularityFreq()
	plotWeeklyRegularity(outfile = "results/monthly_regfreq_many.png")
	plotWeeklyRegularity2(outfile = "results/monthly_customerregfreq_many.png")
