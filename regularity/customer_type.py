import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk, toCSV

def transactionDates():
	file = "../data/regularity.csv"
	transact = readChunk(file, header = None)
	transact.rename(columns = {0:'USERID', 1:'SESSIONID', 2:'MONTH', 3:'WEEK', 4:'DATE', 5:'DAY_OF_WEEK'}, inplace = True)

	transact['DATE'] = pd.to_datetime(last_transact['DATE'])
	transact.sort_values('DATE', ascending = True)
	last_transact = transact.drop_duplicates(subset = ['USERID'], keep = 'last')
	last_transact = last_transact[['USERID', 'DATE']]
	last_transact.rename(columns = {'DATE':'LAST_TRANSACTION'}, inplace = True)
	first_transact = transact.drop_duplicates(subset = ['USERID'], keep = 'first')
	first_transact = first_transact[['USERID', 'DATE']]
	first_transact.rename(columns = {'DATE':'FIRST_TRANSACTION'}, inplace = True)

	first_transact = first_transact.merge(last_transact, how = 'left', on = 'USERID')
	print(first_transact.head())
	toCSV(first_transact, 'results/transaction_dates.csv')


def averageRegularity():
	file = 'results/regularity.csv'
	df = readChunk(file)

	df['RWEEK'] = df['RWEEK'].astype(int)
	new_df = df.groupby('USERID')['RWEEK'].mean().to_frame()
	print(new_df.head())
	toCSV(new_df, 'results/average_regularity.csv')

def getCustomerType():
	transact = readChunk('results/transaction_dates.csv')
	aver = readChunk('results/average_regularity.csv')

	transact = transact.merge(aver, how = 'left', on = 'USERID')
	transact['LAST_TRANSACTION'] = pd.to_datetime(transact['LAST_TRANSACTION'])
	transact['RWEEK'] = transact['RWEEK'].astype(float)
	transact['INACTIVITY_DAYS'] = (transact['LAST_TRANSACTION'] - pd.to_datetime('2019-08-31')).days
	transact['CUSTOMERTYPE'] = transact[['INACTIVITY_DAYS', 'RWEEK']].apply(lambda x: 'PRESENT' if x[0] <= x[1] else 'LOST')
	print(transact.head())
	toCSV(transact, 'results/customer_type.csv')



if __name__ == '__main__':
	transactionDates()
	averageRegularity()
	getCustomerType()