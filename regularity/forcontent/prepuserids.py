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

diverse = pd.read_csv("../../data/customer_feature_matrix.csv")
diverse.columns = diverse.columns.str.upper()
diverse = diverse.loc[diverse.FREQUENCY != 1]
diverse = diverse.loc[diverse.LABEL != 'NEW']
diverse = diverse[['USERID', 'LABEL']]
uniquecust = diverse.USERID.unique()
print(len(uniquecust))
# np.savetxt('results/diversecustomers.txt', uniquecust, delimiter = ',', fmt = "%s")
file = "../../data/regularity_cleaned_ordered.csv"
df = readChunk(file, header = None)
df.rename(columns = {0:'USERID', 1:'SESSIONID', 2:'MONTH', 3:'WEEK', 4:'DATE', 5:'DAY_OF_WEEK'}, inplace = True)
print(len(df))

old = 0
for i in range(1, 63):
	new = 50000*i
	print(old, new)
	temp = uniquecust[old:new]
	temp2 = df[df['USERID'].isin(temp)]
	print(len(temp2))
	toCSV(temp2, 'results/all/'+str(i)+'.csv', index = False)
	# np.savetxt('results/all/'+str(i)+'.txt', temp, delimiter = ',', fmt = "%s")
	old = new + 1