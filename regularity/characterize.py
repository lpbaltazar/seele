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
		for k in ['PRESENT', 'LOST']:
			temp3 = df.loc[df.CUSTOMERTYPE == k]
			print(k)
			for j in df.RWEEK.unique():
				lower = 0
				upper = 30
				all_bins = []
				temp = temp3.loc[temp3.RWEEK == j]
				total = len(temp)
				print(total)
				if total == 0: continue
				for i in range(10):
					bins = {}
					bins['bin'] = '[' +str(lower)+', '+str(upper)+')'
					temp2 = temp.loc[(temp.TENURE >= lower) & (temp.TENURE < upper)]
					bins['percent'] = (len(temp2)/total)*100
					all_bins.append(bins)
					lower = lower + 30
					upper = upper + 30
				new_df = pd.DataFrame(all_bins)
				# new_df.sort_values('percent'ter, inplace = True)
				new_df.to_csv('results/'+k+'_tenureRegularityCorrespondence_percent_'+str(j)+'.csv')

def countCustomerTypePerRegularity():
	file = 'results/tenure.csv'
	df = pd.read_csv(file)
	print(df.head())

	temp = df.loc[df.CUSTOMERTYPE == 'PRESENT']
	new_df = temp.groupby(['RWEEK', 'WEEK'])['USERID'].count().to_frame()
	new_df.rename(columns = {'USERID':'PRESENT'}, inplace = True)

	temp = df.loc[df.CUSTOMERTYPE == 'LOST']
	new_df = new_df.merge(temp.groupby(['RWEEK', 'WEEK'])['USERID'].count().to_frame(), how = 'left', on = 'RWEEK')
	new_df.rename(columns = {'USERID':'LOST'}, inplace = True)

	new_df.to_csv('results/countCustomerTypePerRegularity.csv')

if __name__ == '__main__':
	# countPerRegularity()
	tenureRegularityCorrespondence('percentage')
	# countCustomerTypePerRegularity()