import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../../")

import os
import csv
import time
import pandas as pd
import numpy as np

from utils import readChunk, toCSV

file = sys.argv[1]
outfile = sys.argv[2]
df = readChunk(file)
# df.rename(columns = {0:'USERID', 1:'SESSIONID', 2:'MONTH', 3:'WEEK', 4:'DATE', 5:'DAY_OF_WEEK'}, inplace = True)
df['MONTH'] = df['MONTH'].apply(lambda x: x[-2:])
df['DATE'] = df['DATE'].apply(lambda x: x[-2:])
df['MONTH_DATE'] = df['MONTH']+df['DATE']
print(df.MONTH.unique())
print(df.DATE.unique())
print(len(df))
df.drop_duplicates(subset = 'MONTH_DATE', keep = 'first', inplace = True)
print(len(df))

df.MONTH = df.MONTH.astype(int)
df.MONTH_DATE = df.MONTH_DATE.astype(int)

count = 0
with open(outfile, "a") as f:
	writer = csv.writer(f, delimiter = ',')
	for i in df.USERID.unique():
		print(count,'/', len(df.USERID.unique()))
		temp = df.loc[df.USERID == i]
		bin_df = pd.DataFrame(index = list(temp.MONTH.unique()), data = 0, columns = list(range(1, 32)))
		bin_df.index.name = 'MONTH'
		for j in sorted(temp.MONTH.unique()):
			temp2 = temp.loc[temp.MONTH == j]
			for k in range(len(temp2)):
				bin_df.loc[int(j)][int(temp2.iloc[k]['DATE'])] = 1

		bin_df['RMONTH'] = bin_df.sum(axis = 1)
		bin_df['USERID'] = i
		bin_df.reset_index(inplace = True)
		print(bin_df)
		count = count+1
		for j in range(len(bin_df)):
			writer.writerow(bin_df.iloc[j][:])