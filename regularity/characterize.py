import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

def countPerRegularity():
	file = 'results/tenure.csv'
	df = pd.read_csv(file)
	new_df = df.groupby(['RWEEK'])['USERID'].count().to_frame()
	new_df.rename(columns = {'USERID':'COUNT'}, inplace = True)

	new_df.to_csv('results/count_per_regularity.csv')

def tenureRegularityCorrespondence(corr_type = 'mean'):
	file = 'results/tenure.csv'
	df = pd.read_csv(file)
	if corr_type == 'mean':
		new_df = df.groupby(['RWEEK'])['TENURE'].mean().to_frame()
		new_df.to_csv('results/tenureRegularityCorrespondence.csv')
	if corr_type == 'percentage':
		total = len(df)
		for j in df.RWEEK.unique():
			lower = 0
			upper = 14
			all_bins = []
			temp = df.loc[df.RWEEK == j]
			total = len(temp)
			for i in range(31):
				bins = {}
				bins['bin'] = '[' +str(lower)+', '+str(upper)+')'
				temp2 = temp.loc[(temp.TENURE >= lower) & (temp.TENURE < upper)]
				bins['percent'] = (len(temp2)/total)*100
				all_bins.append(bins)
				lower = lower + 14
				upper = upper + 14
			new_df = pd.DataFrame(all_bins)
			# new_df.sort_values('percent'ter, inplace = True)
			new_df.to_csv('results/tenureRegularityCorrespondence_percent_'+str(j)+'.csv')

def countCustomerTypePerRegularity():
	file = 'results/tenure.csv'
	df = pd.read_csv(file)

	temp = df.loc[df.CUSTOMERTYPE == 'PRESENT']
	new_df = temp.groupby(['RWEEK'])['USERID'].count().to_frame()
	new_df.rename(columns = {'USERID':'PRESENT'}, inplace = True)

	temp = df.loc[df.CUSTOMERTYPE == 'LOST']
	new_df = new_df.merge(temp.groupby(['RWEEK'])['USERID'].count().to_frame(), how = 'left', on = 'RWEEK')
	new_df.rename(columns = {'USERID':'LOST'}, inplace = True)

	new_df.to_csv('results/countCustomerTypePerRegularity.csv')

if __name__ == '__main__':
	# countPerRegularity()
	tenureRegularityCorrespondence('percentage')
	# countCustomerTypePerRegularity()