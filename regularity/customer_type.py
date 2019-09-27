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
	file = "results/first_and_last_transaction_correct.csv"
	df = readChunk(file, header = None)
	df.rename(columns = {0:'USERID', 1:'FIRST_TRANSACTION', 2:'LAST_TRANSACTION'}, inplace = True)
	
	file2 = 'results/average_regularity.csv'
	df2 = readChunk(file2)

	df2 = df2.merge(df, how = 'left', on = 'USERID')
	df2.drop(['RWEEK'], axis = 1, inplace = True)
	toCSV(df2, 'results/transaction_dates.csv', index = False)


def averageRegularity(file):
	df = readChunk(file, header = None)
	df.rename(columns = {0:'WEEK', 8:'RWEEK', 9:'USERID'}, inplace = True)
	print('Number of customers: ', len(df.USERID.unique()))
	df['RWEEK'] = df['RWEEK'].astype(int)
	new_df = df.groupby('USERID')['RWEEK'].mean().to_frame()
	new_df['RWEEK'] = round(new_df['RWEEK'])
	toCSV(new_df, 'results/average_regularity.csv')

def getCustomerType():
	transact = readChunk('results/transaction_dates.csv')
	aver = readChunk('results/average_regularity.csv')
	transact = transact.merge(aver, how = 'left', on = 'USERID')
	transact['LAST_TRANSACTION'] = pd.to_datetime(transact['LAST_TRANSACTION'])
	print(transact.head())
	transact['RWEEK'] = transact['RWEEK'].astype(float)
	transact['INACTIVITY_DAYS'] = transact['LAST_TRANSACTION'].apply(lambda x: (pd.to_datetime('2019-09-01') - x).days) 
	transact['INACTIVITY_DAYS'] = transact['INACTIVITY_DAYS'].apply(lambda x: 0 if x == -1 else x).astype(float)
	transact = customerType2(transact)
	print(transact.head(10))
	toCSV(transact, 'results/customer_type.csv', index = False)

def customerType2(df):
	ctype = []
	for i in range(len(df)):
		if df.iloc[i]['INACTIVITY_DAYS'] <= df.iloc[i]['RWEEK'] + 7: ctype.append('ACTIVE')
		else: ctype.append('LOST')
	df['CUSTOMERTYPE'] = ctype
	return df

def calculateTenure():
	df = readChunk('results/customer_type.csv')
	tenure = []
	df['FIRST_TRANSACTION'] = pd.to_datetime(df['FIRST_TRANSACTION'])
	df['LAST_TRANSACTION'] = pd.to_datetime(df['LAST_TRANSACTION'])
	for i in range(len(df)):
		if df.iloc[i]['CUSTOMERTYPE'] == 'PRESENT': tenure.append((pd.to_datetime('2019-09-01') - df.iloc[i]['FIRST_TRANSACTION']).days)
		else: tenure.append((df.iloc[i]['LAST_TRANSACTION'] - df.iloc[i]['FIRST_TRANSACTION']).days)
	df['TENURE'] = tenure
	print(df.head(10))
	toCSV(df, 'results/tenure.csv', index = False)

if __name__ == '__main__':
	averageRegularity("status/results/regularity_combined.csv")
	transactionDates()
	getCustomerType()
	calculateTenure()