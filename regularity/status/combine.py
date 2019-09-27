import warnings
warnings.filterwarnings("ignore")

import sys
sys.pah.append("../../")

import os
import time
import pandas as pd
import numpy as np

data_dir = "results/regularity"
dfs = []
for f in sorted(os.listdir(data_dir):
	if f.endswith(".csv"):
		dfs.append(pd.read_csv(os.path.join(data_dir, f), header = None))
		
dfs = pd.concat(dfs)
dfs.rename(columns = {0:'WEEK', 8:'RWEEK', 9:'USERID'}, inplace = True)
dfs.to_csv("results/regularity_combined.csv")