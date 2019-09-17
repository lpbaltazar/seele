import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import csv
import time
import pandas as pd
import numpy as np

file = "../data/yearweek_correct.csv"
df = readChunk(file, header = None, nrows = 10000)
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
		new_df = pd.DataFrame(index = i, data = 0, columns = list(range(5, 35)))

		for j in range(len(temp)):
			week = temp.iloc[j]['YEARWEEK']
			new_df.loc[i][int(week)] = 1

		writer.writerow(new_df)