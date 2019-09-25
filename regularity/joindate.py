import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import csv
import time
import pandas as pd
import numpy as np

from utils import readChunk

def getWeekPresent():
	file = "../data/yearweek_correct.csv"
	df = readChunk(file, header = None)
	df.rename(columns = {0:"USERID", 1:"SESSIONID", 2:"YEARWEEK"}, inplace = True)
	df.YEARWEEK = df.YEARWEEK.astype(int)
	df.YEARWEEK = df.YEARWEEK - 201900
	df = df.loc[df.YEARWEEK != 4]
	df.drop_duplicates(subset = ["USERID", "YEARWEEK"], keep = "first", inplace = True)
	print(df.head(10))

	with open("customer_present.csv", "a") as f:
		writer = csv.writer(f, delimiter = ',')
		for i in df.USERID.unique():
			temp = df.loc[df.USERID == i]
			new_df = pd.DataFrame(index = [i], data = 0, columns = list(range(5, 35)))

			for j in range(len(temp)):
				week = temp.iloc[j]['YEARWEEK']
				new_df.loc[i][int(week)] = 1
			
			writer.writerow(new_df.reset_index().iloc[0])


def getJoinedWeek(x):
	a = x.index.values[(x == '1')]
	return(int(a[0])+4)

def addJoinedWeek():
	file = "customer_present.csv"
	df = readChunk(file, header = None)
	df.rename(columns = {0:"USERID"}, inplace = True)

	df.set_index('USERID', inplace = True)

	joined = []
	for i in range(len(df)):
		joined.append(getJoinedWeek(df.iloc[i]))
	df['joinedweek'] = joined
	print(df.joinedweek)

	df.to_csv('week_present_and_joined.csv')

if __name__ == '__main__':
	getWeekPresent()
	addJoinedWeek()