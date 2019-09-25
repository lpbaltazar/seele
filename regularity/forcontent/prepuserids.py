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

diverse = pd.read_csv("../../content_type/results/customer_feature_matrix_active.csv")
diverse = diverse.loc[diverse.CONTENT_TYPE_WATCHED == 'DIVERSE']
diverse = diverse[['USERID', 'CONTENT_TYPE_WATCHED']]
uniquecust = diverse.USERID.unique()
uniquecust.savetxt('results/diversecustomers.txt', delimiter = ',', fmt = "%s")

first50k = pd.read_csv('results/diversecustomers.txt', header = None, nrows = 50000)
print(first50k)
print(len(first50kx))