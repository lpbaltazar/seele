import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk

file = "../data/regularity_cleaned_ordered.csv"
df = readChunk(file, header = None)
df.rename(columns = {0:'USERID', 1:'SESSIONID', 2:'MONTH', 3:'WEEK', 4:'DATE', 5:'DAY_OF_WEEK'}, inplace = True)

df = df[['USERID', 'DATE', 'WEEK']]

df['DATE'] = pd.to_datetime(df['DATE'])
df.sort_values('DATE', inplace = True)
weekly_first = df.groupby(['USERID', 'WEEK']).first()
print(weekly_first.head(10))
weekly_last = df.groupby(['USERID', 'WEEK']).last()
print(weekly_last.head(10))

weekly_first = weekly_first.merge(weekly_last, how = 'left', on = ['USERID', 'WEEK'])
print(weekly_first)
weekly_first.to_csv("results/weekly_first_last_transaction.csv")