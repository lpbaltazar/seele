import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk

file = "status/results/regularity_combined.csv"
df = readChunk(file)
df.RWEEK = df.RWEEK.astype(int)
df.WEEK = df.WEEK.astype(int)
df = df.loc[df.WEEK != 201904]
new_df = df.groupby('USERID')['RWEEK'].agg(lambda x: pd.Series.mode(x)[0]).to_frame()
print(new_df.head())
new_df.to_csv("status/rweek.csv")

# file = "status/results/regularity_combined_monthly.csv"
# df = readChunk(file)
# df.RMONTH = df.RMONTH.astype(int)
# df.MONTH = df.MONTH.astype(int)
# df = df.loc[df.MONTH != 1]
# new_df = df.groupby('USERID')['RMONNTH'].mean().to_frame()
# print(new_df.head())
# new_df.to_csv("status/rweek.csv")