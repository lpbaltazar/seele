import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk, toCSV

file = "../data/year_week.csv"
df = readChunk(file, sep = "\t")

print(df.head())
df.WEEK = df.WEEK.astype(int)
df.sort_values('WEEK', inplace = True)
print(len(df))
df.drop_duplicates(subset = ['USERID'], keep = 'first', inplace = True)
print(len(df))

df.rename(columns = {'WEEK':'INCEPTION_WEEK'}, inplace = True)
toCSV(df[['USERID', 'INCEPTION_WEEK']], "inception_week.csv", index = False)


