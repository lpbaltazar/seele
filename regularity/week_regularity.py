import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk, toCSV

file = "../data/regularity.csv"
df = readChunk(file, header = None)
df.rename(columns = {0:'USERID', 1:'SESSIONID', 2:'MONTH', 3:'WEEK', 4:'DATE', 5:'DAY_OF_WEEK'}, inplace = True)

df.WEEK = df.WEEK.astype(int)
df.DAY_OF_WEEK = df.DAY_OF_WEEK.astype(int)
binary = []
for i in df.USERID.unique():
	temp = df.loc[df.USERID == i]
	bin_df = pd.DataFrame(index = list(temp.WEEK.unique()), data = 0, columns = list(range(1,8))) 
	bin_df.index.name = 'WEEK'
	for j in temp.WEEK.unique():
		temp2 = temp.loc[temp.WEEK == j]
		for k in range(len(temp2)):
			bin_df.loc[j][temp2.iloc[i]['DAY_OF_WEEK']] = 1
	
	bin_df['RWEEK'] = bin_df.iloc[:, -7:].sum()
	bin_df['USERID'] = i
	binary.append(bin_df)

binary = pd.concat(binary)
toCSV(binary, "results/regularity.csv")