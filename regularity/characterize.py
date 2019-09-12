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
	countCustomerTypePerRegularity()