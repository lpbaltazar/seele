import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import csv
import time
import pandas as pd
import numpy as np

from utils import readChunk, toCSV
file = "../data/regularity_cleaned_ordered.csv"
df = readChunk(file, header = None)
df.rename(columns = {0:'USERID', 1:'SESSIONID', 2:'MONTH', 3:'WEEK', 4:'DATE', 5:'DAY_OF_WEEK'}, inplace = True)
print(len(df))

file2 = "../data/weekly_feb3_noreg.txt"
df2 = readChunk(file2, header = None)
df2.rename(columns = {0:'USERID'}, inplace = True)
print(len(df2))

df = df.merge(df2, how = 'right', on = 'USERID')
print(len(df))

df.WEEK = df.WEEK.astype(int)
df.DAY_OF_WEEK = df.DAY_OF_WEEK.astype(int)
binary = []
count = 0
with open("feb3_weekly_regularity.csv", "a") as f:
	writer = csv.writer(f, delimiter = ',')
	for i in df.USERID.unique():
		print(count,'/', len(df.USERID.unique()))
		temp = df.loc[df.USERID == i]
		bin_df = pd.DataFrame(index = list(temp.WEEK.unique()), data = 0, columns = list(range(1,8))) 
		bin_df.index.name = 'WEEK'
		for j in temp.WEEK.unique():
			temp2 = temp.loc[temp.WEEK == j]
			for k in range(len(temp2)):
				bin_df.loc[int(j)][int(temp2.iloc[k]['DAY_OF_WEEK'])] = 1

		bin_df['RWEEK'] = bin_df[1]+bin_df[2]+bin_df[3]+bin_df[4]+bin_df[5]+bin_df[6]+bin_df[7]	
		bin_df['USERID'] = i
		bin_df.reset_index(inplace = True)
		print(bin_df)
		count = count+1
		for j in range(len(bin_df)):
			writer.writerow(bin_df.iloc[j][:])
