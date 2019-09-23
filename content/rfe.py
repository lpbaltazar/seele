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

file = "../data/freq_fastcut.csv"
df = readChunk(file, sep = '\t')
df.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "EXTRACT(YEAR_MONTH FROM MIN(MODIFIEDDATE))":'MONTH', "YEARWEEK(MIN(MODIFIEDDATE))":'WEEK', "COUNT(DISTINCT SESSIONID)":'FREQUENCY'}, inplace = True)

print(df.head())
print('getting frequency')
df.FREQUENCY = df.FREQUENCY.astype(int)
freq = df.groupby('USERID')["FREQUENCY"].sum().to_frame()
print(freq.head(10))
print(len(freq))

print('getting recency')
df.DATE = pd.to_datetime(df.DATE)
df.sort_values("DATE", inplace = True)
df.drop_duplicates(subset = ['USERID'], keep = 'last', inplace = True)
recency = []
for i in range(len(df)):
	recency.append((pd.to_datetime('2019-09-01') - df.iloc[i]["DATE"]).days)
df["RECENCY"] = recency
print(df.head(10))
print(len(df))
df = df[['USERID', 'RECENCY']]

print('getting engagement')
file2 = "../data/eng_fastcut.csv"
df2 = readChunk(file2, sep = '\t')
df2.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "EXTRACT(YEAR_MONTH FROM MIN(MODIFIEDDATE))":'MONTH', "YEARWEEK(MIN(MODIFIEDDATE))":'WEEK', "TIMESTAMPDIFF(MINUTE, MIN(SESSION_STARTDT), MAX(SESSION_ENDDT))":'ENGAGEMENT'}, inplace = True)
df2.ENGAGEMENT = df2.ENGAGEMENT.astype(int)
eng = df2.groupby('USERID')['ENGAGEMENT'].sum().to_frame()
print(eng.head(10))
print(len(eng))

df = df.merge(freq, how = 'left', on = 'USERID')
df = df.merge(eng, how = 'left', on = 'USERID')
print(len(df))

toCSV(df, 'results/fastcut.csv', index = False)