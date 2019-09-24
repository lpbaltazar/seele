import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk
# import matplotlib as mpl
# mpl.use('tKagg')
from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib.style as style

sns.set()
style.use('seaborn-poster')
style.use('bmh')

file = "../data/reg_current.csv"
df = readChunk(file, sep = '\t')
df.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)

file3 = "../data/reg_old.csv"
df3 = readChunk(file3, sep = '\t')
df3.rename(columns = {"DATE(MODIFIEDDATE)":'DATE', "DAYOFWEEK(MIN(MODIFIEDDATE))":'DAYOFWEEK'}, inplace = True)

df = pd.concat([df, df3])
print(df.head())

df.dropduplicates(subset = ['USERID', 'DATE'], inplace = True)

label = pd.read_csv("../data/customer_feature_matrix.csv", usecols = ["userid", "label"])
label.columns = label.columns.str.upper()

print(len(df))

label = label.loc[label.LABEL == 'ACTIVE']
df = df.merge(label, how = 'left', on = 'USERID')
prinnt(len(df))

new_df = df.group_by('DATE')['USERID'].count().to_frame()
print(new_df.head())
new_df.reset_index(inplace = True)

new_df['DATE'] = pd.to_datetime(new_df['DATE'])
new_df['DATE'] = new_df['DATE'].dt.date

new_df.sort_values('DATE', inplace = True)
new_df.set_index('DATE', inplace = True)

plot = new_df.plot(kind = 'bar', legend = False)
plot.set_xlabel('DATE')
plot.set_ylabel('NUMBER OF CUSTOMERS')

plt.show()
