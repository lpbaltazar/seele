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
	file = "status/results/regularity_combined.csv"
	df = readChunk(file)
	print('Number of customers: ', len(df.USERID.unique()))
	print(df.head())
	df['RWEEK'] = df['RWEEK'].astype(int)
	new_df = pd.DataFrame(index = [1,2,3,4,5,6,7], columns = ['COUNT'])
	new_df.index.name = 'REGULARITY'
	for i in range(1, 8):
		temp = df.loc[df.RWEEK == i]
		new_df.loc[i]['COUNT'] = len(temp)
	print(new_df.head())
	barPlot(new_df, 'REGULARITY', 'COUNT', 'regfreq_many.png', print_number = True, savefig = True)

	new_df = df.groupby('USERID')['RWEEK'].agg(lambda x: pd.Series.mode(x)[0]).to_frame()
	print(new_df.head())
	new_df2 = pd.DataFrame(index = [1,2,3,4,5,6,7], columns = ['COUNT'])
	new_df2.index.name = 'REGULARITY'
	for i in range(1, 8):
		temp = new_df.loc[new_df.RWEEK == i]
		new_df2.loc[i]['COUNT'] = len(temp)
	barPlot(new_df2, 'REGULARITY', 'NUMBER OF CUSTOMERS', 'customerregfreq_many.png', print_number = True, savefig = True)


	# plot = sns.distplot(a = new_df['RWEEK'].values, kde = False, bins = 7)
	# plot.set_xlabel('REGULARITY')
	# plot.set_ylabel('NUMBER OF CUSTOMERS')
	# plt.savefig('customerregfreq.png', dpi = 600)
	# plt.clf()

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
	cust_type = pd.read_csv("results/customer_type.csv", usecols = ['USERID', 'CUSTOMERTYPE'])
	df = readChunk("status/results/regularity_combined.csv")

	print(len(df))
	if type(custids) is list:
		df = df[df['USERID'].isin(custids)]
		print('Number of customers: ', len(df.USERID.unique()))
	
	print(df.columns)
	df.dropna(subset = ['RWEEK'], inplace = True)
	print('Number of customers: ', len(df.USERID.unique()))
	df['RWEEK'] = df['RWEEK'].astype(int)
	df['WEEK'] = df["WEEK"].astype(int)
	df.sort_values('WEEK', inplace = True)
	df = df.loc[df.WEEK != 201904]
	df = df.merge(cust_type, how = 'left', on = 'USERID')
	print(df.CUSTOMERTYPE)
	for x in ['ACTIVE', 'LOST']:
		df_2 = df.loc[df.CUSTOMERTYPE == x]
		fig, axes = plt.subplots(8,4, sharey = 'row', constrained_layout = True)
		x = 0
		y = 0
		print(weekno, df_2.WEEK.unique())
		for i in df_2.WEEK.unique():
			temp = df_2.loc[df_2.WEEK == i]
			new_df = pd.DataFrame(index = [1,2,3,4,5,6,7], columns = ['COUNT'])
			new_df.index.name = 'REGULARITY'
			for j in range(1, 8):
				temp2 = temp.loc[temp.RWEEK == j]
				new_df.loc[j]['COUNT'] = len(temp2)
			plot = new_df.plot(kind = 'bar', legend = False, ax = axes[x, y], rot = 0)
			# plot.set_ylabel('NUMBER OF CUSTOMERS')
			# plot.set_xlabel('REGULARITY')
			plot.tick_params(axis = 'both', which = 'major', labelsize = 6, pad = 2)
			plot.set_title(i, size = 6, pad = 2)
			x_axis = plot.axes.get_xaxis()
			x_label = x_axis.get_label()
			x_label.set_visible(False)
			if ylim:
				plot.set_ylim(0,ylim)
			y = y + 1
			if y == 4:
				y = 0
				x = x + 1
			new_df.to_csv('results/reqfreq/week_'+x+str(i)+'.png')
		fig.delaxes(axes[7,3])
		fig.delaxes(axes[7,2])
		outfile = "results/regfreq"+x+str(i)+'.csv'
		if outfile:
			plt.savefig(outfile, dpi = 600)


def plotWeeklyRegularity2(weekno = None, custids = None, ylim = None, outfile = None, regularity_type = 'mode', mode_type = None):
	cust_type = pd.read_csv("results/customer_type.csv", usecols = ['USERID', 'CUSTOMERTYPE'])
	df = readChunk("status/results/regularity_combined.csv")
	print(len(df))
	if type(custids) is list:
		df = df[df['USERID'].isin(custids)]

	print('Number of customers: ', len(df.USERID.unique()))
	
	print(df.columns)
	df.dropna(subset = ['RWEEK'], inplace = True)

	print('Number of customers: ', len(df.USERID.unique()))
	df['RWEEK'] = df['RWEEK'].astype(int)
	df['WEEK'] = df["WEEK"].astype(int)
	df = df.loc[df.WEEK != 201904]
	if regularity_type == 'mode':
		if mode_type == 'min':
			df = df.groupby('USERID')['RWEEK'].agg(lambda x: min(pd.Series.mode(x))).to_frame()
		elif mode_type == 'max':
			df = df.groupby('USERID')['RWEEK'].agg(lambda x: max(pd.Series.mode(x))).to_frame()
		else:
			df = df.groupby(['USERID', 'WEEK'])['RWEEK'].agg(lambda x: pd.Series.mode(x)[0]).to_frame()
	df.reset_index(inplace = True)
	print(df.head())
	df = df.merge(cust_type, how = 'left', on = 'USERID')
	for x in ['ACTIVE', 'LOST']:
		df_2 = df.loc[df.CUSTOMERTYPE == x]
		fig, axes = plt.subplots(8,4, sharey = 'row', constrained_layout = True)
		x = 0
		y = 0
		for i in sorted(df_2.WEEK.unique()):
			temp = df_2.loc[df_2.WEEK == i]
			new_df = pd.DataFrame(index = [1,2,3,4,5,6,7], columns = ['COUNT'])
			new_df.index.name = 'REGULARITY'
			print(len(temp))
			for j in range(1, 8):
				temp2 = temp.loc[temp.RWEEK == j]
				new_df.loc[j]['COUNT'] = len(temp2)
				print(new_df)
			plot = new_df.plot(kind = 'bar', legend = False, ax = axes[x, y], rot = 0)
			# plot.set_ylabel('NUMBER OF CUSTOMERS')
			# plot.set_xlabel('REGULARITY')
			plot.tick_params(axis = 'both', which = 'major', labelsize = 6, pad = 2)
			plot.set_title(i, size = 6, pad = 2)
			x_axis = plot.axes.get_xaxis()
			x_label = x_axis.get_label()
			x_label.set_visible(False)
			if ylim:
				plot.set_ylim(0,ylim)
			y = y + 1
			if y == 4:
				y = 0
				x = x + 1
			new_df.to_csv('results/customerregfreq/week_'+x+str(i)+'.csv')
		fig.delaxes(axes[7,3])
		fig.delaxes(axes[7,2])
		# fig.tight_layout()
		# plt.rcParams['figure.constrained_layout.use'] = True
		# plt.subplots_adjust(bottom = 0.1)
		outfile = "results/customerregfreq"+x+str(i)+'.png'
		if outfile:
			plt.savefig(outfile, dpi = 600)

def plotWeeklyRegularity3(file, file2 = None, ylim = None):
	df = readChunk(file, header = None)
	df.rename(columns = {0:'WEEK', 8:'RWEEK', 9:'USERID'}, inplace = True)
	if file2:
		df2 = readChunk(file2, header = None)
		df2.rename(columns = {0:'WEEK', 8:'RWEEK', 9:'USERID'}, inplace = True)
		df = pd.concat([df, df2])
	print(df.head())
	print('Number of customers: ', len(df.USERID.unique()))
	df['RWEEK'] = df['RWEEK'].astype(int)
	df['WEEK'] = df["WEEK"].astype(int)
	df.sort_values('WEEK', inplace = True)
	df = df.loc[df.WEEK != 201904]

	new_df = df.groupby(['RWEEK', 'WEEK'])['USERID'].count().to_frame().reset_index()
	print(new_df.head(20))

	new_df = new_df.groupby('RWEEK')['USERID'].mean().to_frame()
	new_df['USERID'] = round(new_df['USERID'])
	new_df['USERID'] = new_df['USERID'].astype(int)
	print(new_df.head(20))
	plot = new_df.plot(kind = 'bar', legend = False, rot = 0)
	for i in range(len(new_df)):
		plot.text(i, new_df.iloc[i]['USERID'], new_df.iloc[i]['USERID'], horizontalalignment = 'center')
	plot.set_xlabel('REGULARITY')
	plt.savefig("weekly_average_regularity.png", dpi = 300)

if __name__ == '__main__':
	# df = pd.read_csv('results/countCustomerTypePerRegularity.csv')
	# print(df)
	# plotRegularityFreq()
	# plotRegularityTenure()
	# plotWeeklyRegularity("status/results/regularity_combined.csv")
	# plotWeeklyRegularity2("status/results/regularity_combined.csv")
	# plotWeeklyRegularity3("results/feb3_weekly_regularity.csv", "results/feb3_regularity.csv")
	# plotWeeklyRegularity(outfile = "results/all.png", ylim = 300000)
	# plotRegularityFreq()
	plotWeeklyRegularity(outfile = "results/weekly_regfreq_many.png", ylim = 300000)
	plotWeeklyRegularity2(outfile = "results/weekly_customerregfreq_many.png", regularity_type = 'mode', ylim = 300000)
	# weeknum = sys.argv[1]
	# print(weeknum)
	# file = "../data/week"+weeknum+"_frequency_engagement.csv"
	# df = pd.read_csv(file, sep = "\t")
	# custids = list(df.userid.unique())
	# plotWeeklyRegularity(custids= custids, weekno = weeknum, outfile = "results/weekly/regfreq/week"+weeknum+".png")
	# plotWeeklyRegularity2(custids = custids, weekno = weeknum, outfile = "results/weekly/customerregfreq/week"+weeknum+".png")
