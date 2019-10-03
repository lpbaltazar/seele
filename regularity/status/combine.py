import warnings
warnings.filterwarnings("ignore")

import sys
sys.pah.append("../../")

import os
import time
import pandas as pd
import numpy as np

data_dir = "results/monthly"
dfs = []
for f in sorted(os.listdir(data_dir)):
	if f.endswith(".csv"):
		dfs.append(pd.read_csv(os.path.join(data_dir, f), header = None))
		
dfs = pd.concat(dfs)
dfs.rename(columns = {0:'MONTH', 32:'RMONTH', 33:'USERID'}, inplace = True)
dfs.to_csv("results/regularity_combined_monthly.csv")